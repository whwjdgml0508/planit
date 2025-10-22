#!/bin/bash

# PlanIt Simple Deployment Script
# Based on professor's tutorial for direct deployment without Docker

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Configuration
PROJECT_NAME="planit"
DOMAIN="planit.boramae.club"
EC2_IP="35.163.12.109"

print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_status "Starting PlanIt deployment on EC2..."

# Update system
print_status "Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install required packages
print_status "Installing required packages..."
sudo apt install -y python3 python3-pip python3-venv python3-dev \
    postgresql postgresql-contrib nginx git curl \
    build-essential libpq-dev

# Setup PostgreSQL
print_status "Setting up PostgreSQL..."
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Create database and user
sudo -u postgres psql << EOF
CREATE DATABASE planit_db;
CREATE USER planit_user WITH PASSWORD 'planit_secure_password_2024';
ALTER ROLE planit_user SET client_encoding TO 'utf8';
ALTER ROLE planit_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE planit_user SET timezone TO 'Asia/Seoul';
GRANT ALL PRIVILEGES ON DATABASE planit_db TO planit_user;
\q
EOF

# Setup Python virtual environment
print_status "Setting up Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
print_status "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Setup environment variables
print_status "Setting up environment variables..."
cat > .env << EOF
# Django Settings
SECRET_KEY=planit-super-secret-key-for-production-2024
DEBUG=False
ALLOWED_HOSTS=$DOMAIN,www.$DOMAIN,$EC2_IP,localhost,127.0.0.1

# Database Settings
DB_NAME=planit_db
DB_USER=planit_user
DB_PASSWORD=planit_secure_password_2024
DB_HOST=localhost
DB_PORT=5432

# Static Files
STATIC_ROOT=/home/ubuntu/planit/staticfiles
MEDIA_ROOT=/home/ubuntu/planit/media
EOF

# Django setup
print_status "Setting up Django..."
export DJANGO_SETTINGS_MODULE=planit_project.settings.production
python manage.py collectstatic --noinput
python manage.py migrate

# Create superuser (interactive)
print_status "Creating Django superuser..."
python manage.py createsuperuser

# Setup Gunicorn
print_status "Setting up Gunicorn..."
pip install gunicorn

# Create Gunicorn service
sudo tee /etc/systemd/system/planit.service > /dev/null << EOF
[Unit]
Description=PlanIt Django Application
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/planit
Environment=DJANGO_SETTINGS_MODULE=planit_project.settings.production
ExecStart=/home/ubuntu/planit/venv/bin/gunicorn --workers 3 --bind 0.0.0.0:8000 planit_project.wsgi:application
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOF

# Start Gunicorn service
sudo systemctl daemon-reload
sudo systemctl enable planit
sudo systemctl start planit

# Setup Nginx
print_status "Setting up Nginx..."
sudo tee /etc/nginx/sites-available/planit << EOF
server {
    listen 80;
    server_name $DOMAIN www.$DOMAIN $EC2_IP;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        root /home/ubuntu/planit;
    }
    
    location /media/ {
        root /home/ubuntu/planit;
    }

    location / {
        include proxy_params;
        proxy_pass http://127.0.0.1:8000;
    }
}
EOF

# Enable Nginx site
sudo ln -sf /etc/nginx/sites-available/planit /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Test and restart Nginx
sudo nginx -t
sudo systemctl restart nginx
sudo systemctl enable nginx

# Setup firewall
print_status "Setting up firewall..."
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'
sudo ufw --force enable

print_success "Deployment completed!"
print_status "Your application should be available at:"
print_status "- http://$DOMAIN"
print_status "- http://$EC2_IP"
print_status "- Admin: http://$DOMAIN/admin/"

print_status "To check service status:"
echo "sudo systemctl status planit"
echo "sudo systemctl status nginx"
echo "sudo journalctl -u planit -f"
