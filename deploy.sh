#!/bin/bash

# PlanIt Django Application Deployment Script
# This script automates the deployment process on Ubuntu EC2 instance

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_NAME="planit"
PROJECT_DIR="/var/www/$PROJECT_NAME"
REPO_URL="https://github.com/whwjdgml0508/planit.git"
DOMAIN="planit.boramae.club"
EC2_IP="35.163.12.109"
DB_NAME="planit_db"
DB_USER="planit_user"

# Functions
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as root
check_root() {
    if [[ $EUID -eq 0 ]]; then
        print_error "This script should not be run as root. Please run as a regular user with sudo privileges."
        exit 1
    fi
}

# Update system packages
update_system() {
    print_status "Updating system packages..."
    sudo apt update && sudo apt upgrade -y
    print_success "System packages updated"
}

# Install required packages
install_packages() {
    print_status "Installing required packages..."
    sudo apt install -y \
        python3 \
        python3-pip \
        python3-venv \
        python3-dev \
        postgresql \
        postgresql-contrib \
        nginx \
        git \
        curl \
        supervisor \
        ufw \
        fail2ban \
        certbot \
        python3-certbot-nginx \
        build-essential \
        libpq-dev
    print_success "Required packages installed"
}

# Setup PostgreSQL
setup_database() {
    print_status "Setting up PostgreSQL database..."
    
    # Generate random password for database user
    DB_PASSWORD=$(openssl rand -base64 32)
    
    sudo -u postgres psql << EOF
CREATE DATABASE $DB_NAME;
CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';
ALTER ROLE $DB_USER SET client_encoding TO 'utf8';
ALTER ROLE $DB_USER SET default_transaction_isolation TO 'read committed';
ALTER ROLE $DB_USER SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;
\q
EOF
    
    # Save database credentials
    echo "DB_PASSWORD=$DB_PASSWORD" >> /tmp/planit_env
    print_success "PostgreSQL database configured"
}

# Clone or update project
setup_project() {
    print_status "Setting up project directory..."
    
    if [ -d "$PROJECT_DIR" ]; then
        print_warning "Project directory exists. Updating..."
        cd $PROJECT_DIR
        sudo git pull origin main
    else
        print_status "Cloning project repository..."
        sudo git clone $REPO_URL $PROJECT_DIR
    fi
    
    sudo chown -R $USER:www-data $PROJECT_DIR
    sudo chmod -R 755 $PROJECT_DIR
    print_success "Project directory configured"
}

# Setup Python virtual environment
setup_virtualenv() {
    print_status "Setting up Python virtual environment..."
    cd $PROJECT_DIR
    
    if [ ! -d "venv" ]; then
        python3 -m venv venv
    fi
    
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    print_success "Virtual environment configured"
}

# Setup environment variables
setup_environment() {
    print_status "Setting up environment variables..."
    
    # Generate Django secret key
    SECRET_KEY=$(python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')
    
    # Get database password
    DB_PASSWORD=$(grep DB_PASSWORD /tmp/planit_env | cut -d'=' -f2)
    
    # Create .env file
    cat > $PROJECT_DIR/.env << EOF
# Django Settings
SECRET_KEY=$SECRET_KEY
DEBUG=False
ALLOWED_HOSTS=$DOMAIN,www.$DOMAIN,localhost,127.0.0.1

# Database Settings
DB_NAME=$DB_NAME
DB_USER=$DB_USER
DB_PASSWORD=$DB_PASSWORD
DB_HOST=localhost
DB_PORT=5432

# Email Settings (configure as needed)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Redis Settings (if using Redis)
REDIS_URL=redis://localhost:6379/0

# Static Files
STATIC_ROOT=/var/www/$PROJECT_NAME/staticfiles
MEDIA_ROOT=/var/www/$PROJECT_NAME/media
EOF
    
    sudo chown www-data:www-data $PROJECT_DIR/.env
    sudo chmod 600 $PROJECT_DIR/.env
    
    # Clean up temporary file
    rm -f /tmp/planit_env
    
    print_success "Environment variables configured"
}

# Run Django migrations and collect static files
setup_django() {
    print_status "Setting up Django application..."
    cd $PROJECT_DIR
    source venv/bin/activate
    
    # Set production environment
    export DJANGO_SETTINGS_MODULE=planit_project.settings.production
    
    # Run migrations
    python manage.py makemigrations
    python manage.py migrate
    
    # Collect static files
    python manage.py collectstatic --noinput
    
    # Create superuser (interactive)
    print_status "Creating Django superuser..."
    python manage.py createsuperuser
    
    # Set proper permissions
    sudo chown -R www-data:www-data $PROJECT_DIR
    sudo chmod -R 755 $PROJECT_DIR
    sudo chmod -R 755 $PROJECT_DIR/staticfiles
    sudo chmod -R 755 $PROJECT_DIR/media
    
    print_success "Django application configured"
}

# Setup Gunicorn service
setup_gunicorn() {
    print_status "Setting up Gunicorn service..."
    
    # Create log directories
    sudo mkdir -p /var/log/planit
    sudo mkdir -p /var/run/planit
    sudo chown www-data:www-data /var/log/planit
    sudo chown www-data:www-data /var/run/planit
    
    # Copy service file
    sudo cp $PROJECT_DIR/planit.service /etc/systemd/system/
    
    # Reload systemd and enable service
    sudo systemctl daemon-reload
    sudo systemctl enable planit.service
    sudo systemctl start planit.service
    
    print_success "Gunicorn service configured"
}

# Setup Nginx
setup_nginx() {
    print_status "Setting up Nginx..."
    
    # Copy nginx configuration
    sudo cp $PROJECT_DIR/nginx.conf /etc/nginx/sites-available/planit
    
    # Enable site
    sudo ln -sf /etc/nginx/sites-available/planit /etc/nginx/sites-enabled/
    
    # Remove default site
    sudo rm -f /etc/nginx/sites-enabled/default
    
    # Test nginx configuration
    sudo nginx -t
    
    # Restart nginx
    sudo systemctl restart nginx
    sudo systemctl enable nginx
    
    print_success "Nginx configured"
}

# Setup SSL with Let's Encrypt
setup_ssl() {
    print_status "Setting up SSL certificate..."
    
    # Get SSL certificate
    sudo certbot --nginx -d $DOMAIN -d www.$DOMAIN --non-interactive --agree-tos --email admin@$DOMAIN
    
    # Setup auto-renewal
    sudo systemctl enable certbot.timer
    
    print_success "SSL certificate configured"
}

# Setup firewall
setup_firewall() {
    print_status "Setting up firewall..."
    
    sudo ufw default deny incoming
    sudo ufw default allow outgoing
    sudo ufw allow ssh
    sudo ufw allow 'Nginx Full'
    sudo ufw --force enable
    
    print_success "Firewall configured"
}

# Setup fail2ban
setup_fail2ban() {
    print_status "Setting up fail2ban..."
    
    sudo cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local
    
    # Configure fail2ban for nginx and ssh
    cat > /tmp/planit-jail.local << EOF
[sshd]
enabled = true
port = ssh
logpath = /var/log/auth.log
maxretry = 3
bantime = 3600

[nginx-http-auth]
enabled = true
port = http,https
logpath = /var/log/nginx/error.log
maxretry = 3
bantime = 3600

[nginx-noscript]
enabled = true
port = http,https
logpath = /var/log/nginx/access.log
maxretry = 6
bantime = 3600
EOF
    
    sudo mv /tmp/planit-jail.local /etc/fail2ban/jail.d/planit.local
    sudo systemctl restart fail2ban
    sudo systemctl enable fail2ban
    
    print_success "Fail2ban configured"
}

# Setup log rotation
setup_logrotate() {
    print_status "Setting up log rotation..."
    
    cat > /tmp/planit-logrotate << EOF
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
    
    sudo mv /tmp/planit-logrotate /etc/logrotate.d/planit
    print_success "Log rotation configured"
}

# Main deployment function
main() {
    print_status "Starting PlanIt deployment..."
    
    check_root
    update_system
    install_packages
    setup_database
    setup_project
    setup_virtualenv
    setup_environment
    setup_django
    setup_gunicorn
    setup_nginx
    
    # Ask for SSL setup
    read -p "Do you want to setup SSL certificate? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        setup_ssl
    fi
    
    setup_firewall
    setup_fail2ban
    setup_logrotate
    
    print_success "Deployment completed successfully!"
    print_status "Your application should now be available at: http://$DOMAIN"
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_status "SSL enabled. Your application is also available at: https://$DOMAIN"
    fi
    
    print_status "Next steps:"
    echo "1. Update the REPO_URL in this script with your actual repository URL"
    echo "2. Configure email settings in the .env file"
    echo "3. Review and customize the Django admin interface"
    echo "4. Set up monitoring and backup solutions"
    echo "5. Review security settings and update as needed"
}

# Run main function
main "$@"
