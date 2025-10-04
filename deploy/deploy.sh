#!/bin/bash

# PlanIt Django Application Deployment Script
# Usage: ./deploy.sh

set -e

echo "🚀 Starting PlanIt deployment..."

# Configuration
PROJECT_NAME="planit"
PROJECT_DIR="/var/www/$PROJECT_NAME"
REPO_URL="https://github.com/whwjdgml0508/cadet-learning-platform.git"
PYTHON_VERSION="3.11"
DB_NAME="planit_db"
DB_USER="planit_user"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   print_error "This script should not be run as root"
   exit 1
fi

print_status "Updating system packages..."
sudo apt update && sudo apt upgrade -y

print_status "Installing system dependencies..."
sudo apt install -y \
    python3 \
    python3-pip \
    python3-venv \
    python3-dev \
    postgresql \
    postgresql-contrib \
    nginx \
    redis-server \
    git \
    curl \
    supervisor \
    certbot \
    python3-certbot-nginx

print_status "Setting up PostgreSQL database..."
sudo -u postgres psql -c "CREATE DATABASE $DB_NAME;" || print_warning "Database might already exist"
sudo -u postgres psql -c "CREATE USER $DB_USER WITH PASSWORD 'your_secure_password';" || print_warning "User might already exist"
sudo -u postgres psql -c "ALTER ROLE $DB_USER SET client_encoding TO 'utf8';"
sudo -u postgres psql -c "ALTER ROLE $DB_USER SET default_transaction_isolation TO 'read committed';"
sudo -u postgres psql -c "ALTER ROLE $DB_USER SET timezone TO 'Asia/Seoul';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;"

print_status "Creating project directory..."
sudo mkdir -p $PROJECT_DIR
sudo chown -R $USER:www-data $PROJECT_DIR

print_status "Cloning repository..."
if [ -d "$PROJECT_DIR/.git" ]; then
    cd $PROJECT_DIR
    git pull origin main
else
    git clone $REPO_URL $PROJECT_DIR
    cd $PROJECT_DIR
fi

print_status "Setting up Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

print_status "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

print_status "Setting up environment variables..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    print_warning "Please edit .env file with your configuration"
    print_warning "Especially set SECRET_KEY, DB_PASSWORD, and EMAIL settings"
fi

print_status "Creating necessary directories..."
sudo mkdir -p /var/log/planit
sudo mkdir -p /var/run/planit
sudo chown -R www-data:www-data /var/log/planit
sudo chown -R www-data:www-data /var/run/planit

print_status "Collecting static files..."
export DJANGO_SETTINGS_MODULE=planit_project.settings.production
python manage.py collectstatic --noinput

print_status "Running database migrations..."
python manage.py migrate

print_status "Creating superuser (optional)..."
echo "Do you want to create a superuser? (y/n)"
read -r response
if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
    python manage.py createsuperuser
fi

print_status "Setting up systemd service..."
sudo cp deploy/planit.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable planit
sudo systemctl start planit

print_status "Setting up Nginx..."
sudo cp deploy/nginx_planit.conf /etc/nginx/sites-available/planit
sudo ln -sf /etc/nginx/sites-available/planit /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

print_status "Setting up SSL certificate (optional)..."
echo "Do you want to set up SSL certificate with Let's Encrypt? (y/n)"
read -r ssl_response
if [[ "$ssl_response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
    sudo certbot --nginx -d planit.boramae.club
fi

print_status "Setting up log rotation..."
sudo tee /etc/logrotate.d/planit > /dev/null <<EOF
/var/log/planit/*.log {
    daily
    missingok
    rotate 52
    compress
    delaycompress
    notifempty
    create 644 www-data www-data
    postrotate
        systemctl reload planit
    endscript
}
EOF

print_status "Setting file permissions..."
sudo chown -R www-data:www-data $PROJECT_DIR
sudo chmod -R 755 $PROJECT_DIR
sudo chmod -R 644 $PROJECT_DIR/media

print_status "Restarting services..."
sudo systemctl restart planit
sudo systemctl restart nginx
sudo systemctl restart redis-server

print_status "Checking service status..."
sudo systemctl status planit --no-pager
sudo systemctl status nginx --no-pager

print_status "🎉 Deployment completed successfully!"
print_status "Your application should be available at: http://planit.boramae.club"
print_warning "Don't forget to:"
print_warning "1. Update .env file with proper values"
print_warning "2. Set up proper database password"
print_warning "3. Configure email settings"
print_warning "4. Set up SSL certificate if not done already"
print_warning "5. Configure firewall rules"

echo ""
echo "Useful commands:"
echo "- Check logs: sudo journalctl -u planit -f"
echo "- Restart service: sudo systemctl restart planit"
echo "- Check Nginx logs: sudo tail -f /var/log/nginx/planit_error.log"
