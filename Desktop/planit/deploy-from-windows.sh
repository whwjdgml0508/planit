#!/bin/bash

# PlanIt Windows to EC2 Deployment Helper
# Run this script from Git Bash on Windows

set -e

# Configuration
EC2_IP="35.163.12.109"
EC2_USER="ubuntu"
SSH_KEY_PATH="/c/Users/User/ssh/ec2-kafa-2-key.pem"  # SSH key for EC2 authentication (Git Bash path)

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if we're in the right directory
if [ ! -f "manage.py" ]; then
    print_error "Please run this script from your Django project root directory"
    exit 1
fi

print_status "Starting deployment to EC2..."

# Prepare SSH command
if [ -n "$SSH_KEY_PATH" ] && [ -f "$SSH_KEY_PATH" ]; then
    SSH_CMD="ssh -i $SSH_KEY_PATH"
    SCP_CMD="scp -i $SSH_KEY_PATH"
    print_status "Using SSH key: $SSH_KEY_PATH"
else
    SSH_CMD="ssh"
    SCP_CMD="scp"
    print_status "Using password authentication"
fi

# Upload code to EC2
print_status "Uploading code to EC2 server..."
$SCP_CMD -r . $EC2_USER@$EC2_IP:~/planit/

if [ $? -eq 0 ]; then
    print_success "Code uploaded successfully"
else
    print_error "Failed to upload code"
    exit 1
fi

# Run deployment script on EC2
print_status "Running deployment script on EC2..."
$SSH_CMD $EC2_USER@$EC2_IP << 'ENDSSH'
cd ~/planit
chmod +x simple-deploy.sh
./simple-deploy.sh
ENDSSH

if [ $? -eq 0 ]; then
    print_success "Deployment completed successfully!"
    print_status "Your application should be available at:"
    print_status "- http://planit.boramae.club"
    print_status "- http://35.163.12.109"
else
    print_error "Deployment failed"
    exit 1
fi
