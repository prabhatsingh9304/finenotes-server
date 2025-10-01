# finenotes-server

A Node.js/Express server for the Gifco restaurant discovery platform.

## Features

- **Restaurant Management**: Add, search, and manage restaurants
- **User Authentication**: Secure user authentication with Privy
- **Follow System**: Users can follow/unfollow restaurants
- **Personal Notes**: Users can add private notes to restaurants (e.g., "this restaurant is awesome")
- **Food Tags**: Categorize and search restaurants by food type
- **Google Places Integration**: Fetch restaurant photos and details

## New Restaurant Follow & Notes API

The server now includes comprehensive follow/unfollow functionality and personal notes system:

- Follow/unfollow restaurants with toggle functionality
- Add, edit, and delete personal notes for restaurants (max 1000 characters)
- Notes are private and only visible to the user who created them
- Get followed restaurants with or without notes
- Check follow status and note existence for any restaurant

See [Restaurant Follow/Unfollow and Notes API Documentation](./docs/RESTAURANT_FOLLOW_API.md) for detailed API usage.

# Docker

```
docker build -t prabhatsingh9304/gifco-server:latest .
```

docker run -d -p 5000:5000 prabhatsingh9304/gifco-server:latest

docker push prabhatsingh9304/gifco-server:latest

# Deployment YAML

# Deployment on aws

sudo apt update && clear
sudo apt install -y nginx
sudo systemctl status nginx

## Install Docker

### Add Docker's official GPG key:

sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

### Add the repository to Apt sources:

echo \
 "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
 $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | \
 sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update

sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

### Verify installation

sudo docker run hello-world

### Add User to docker group

sudo usermod -aG docker $USER
newgrp docker
sudo systemctl restart docker

## Nginx Setup

sudo tee /etc/nginx/sites-available/default > /dev/null << EOF
server {
server_name dev.gifco.io www.dev.gifco.io;
client_max_body_size 300M;

    access_log /var/log/nginx/gifco.access.log;
    error_log /var/log/nginx/gifco.error.log;

    root /path;

    location /api {
        proxy_pass http://localhost:5000; # Node.js backend port
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'Upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_redirect off;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Nginx-Proxy true;
    }

}
EOF

## Run Pipeline

## Restart nginx

sudo systemctl restart nginx
sudo systemctl status nginx

## SSL Certificates

sudo snap install core; sudo snap refresh core
sudo apt remove certbot
sudo snap install --classic certbot
sudo systemctl reload nginx
sudo certbot --nginx -d dev.gifco.io
