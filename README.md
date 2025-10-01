# finenotes-server

A Finenotes.AI server for the FineNotes.AI extension.

## Features

- **YouTube Transcript Processing**: Extract and parse video transcripts with timestamp support
- **Notion Integration**: OAuth authentication and page creation for seamless note-taking
- **Transcript Parsing**: Advanced timestamp-based text extraction from video transcripts
- **Browser Extension Support**: Backend API server for the FineNotes.AI browser extension

## API Endpoints

The server provides the following endpoints:

### YouTube API (`/youtube`)

- **POST** `/youtube/transcript` - Process YouTube video transcripts with timestamp parsing

### Notion API (`/notion`)

- **GET** `/notion/oauth/start` - Initiate Notion OAuth flow
- **GET** `/notion/oauth/callback` - Handle Notion OAuth callback
- **POST** `/notion/pages/create` - Create new pages in Notion with notes and content

## Environment Variables

The following environment variables are required for the server to function properly:

| Variable               | Description                                                                           | Required |
| ---------------------- | ------------------------------------------------------------------------------------- | -------- |
| `NOTION_CLIENT_ID`     | Your Notion OAuth application client ID                                               | Yes      |
| `NOTION_CLIENT_SECRET` | Your Notion OAuth application client secret                                           | Yes      |
| `NOTION_REDIRECT_URI`  | OAuth callback redirect URI (e.g., `http://localhost:5000/api/notion/oauth/callback`) | Yes      |

# Docker

Build the Docker image:

```bash
docker build -t finenotes/finenotes-server:latest .
```

Run the container:

```bash
docker run -d -p 5000:5000 finenotes/finenotes-server:latest
```

Push to registry (optional):

```bash
docker push <your-registry>/finenotes-server:latest
```

# Deployment on AWS

## System Setup

```bash
sudo apt update && clear
sudo apt install -y nginx
sudo systemctl status nginx

```

## Install Docker

### Add Docker's official GPG key:

```bash
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

```

### Add the repository to Apt sources:

```bash

echo \
 "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
 $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | \
 sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update

sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

```

### Verify installation

```bash

sudo docker run hello-world

```

### Add User to docker group

```bash

sudo usermod -aG docker $USER
newgrp docker
sudo systemctl restart docker

```

## Nginx Setup

```bash
sudo tee /etc/nginx/sites-available/default > /dev/null << EOF
server {
    server_name your-domain.com www.your-domain.com;
    client_max_body_size 300M;

    access_log /var/log/nginx/finenotes.access.log;
    error_log /var/log/nginx/finenotes.error.log;

    root /path;

    location /api {
        proxy_pass http://localhost:5000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'Upgrade';
        proxy_set_header Host \$host;
        proxy_cache_bypass \$http_upgrade;
        proxy_redirect off;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_set_header X-Nginx-Proxy true;
    }

}
EOF

```

## Run Pipeline

## Restart nginx

```bash

sudo systemctl restart nginx
sudo systemctl status nginx

```

## SSL Certificates

```bash
sudo snap install core; sudo snap refresh core
sudo apt remove certbot
sudo snap install --classic certbot
sudo systemctl reload nginx
sudo certbot --nginx -d your-domain.com
```
