
# UniGo Website Deploy Manual

**Application Name:** OStation  
**Version:** 1.1  
**Author:** XUAN  
**Date:** 15/09/2025  

---

## Table of Contents

1. [UniGo Website Overview](#unigo-website-overview)  
   - [1.1 Project Structure (Local)](#11-project-structure-local)  

2. [Deployment Guide](#deployment-guide)  
   - [2.1 Push Project to GitHub](#21-push-project-to-github)  
   - [2.2 Prepare AWS EC2 Deployment Environment](#22-prepare-aws-ec2-deployment-environment)  
   - [2.3 Deploy Project on EC2 Server (First Time)](#23-deploy-project-on-ec2-server-for-the-first-time)  
   - [2.4 Start Flask with Gunicorn](#24-start-flask-with-gunicorn)  
   - [2.5 Update Website on EC2](#25-update-website-on-ec2)  
     - [2.5.1 Push Code with crm.db](#251-push-code-to-github-with-crmdb-from-local)  
     - [2.5.2 On Ubuntu](#252-on-ubuntu)  
     - [2.5.3 Pull Newest Code](#253-pull-newest-code-from-github)  
     - [2.5.4 Activate venv & Install Dependencies](#254-active-venv-and-install-requirementstxt)  
     - [2.5.5 Restart Gunicorn](#255-restart-gunicorn-service)  
     - [2.5.6 Check Gunicorn Running](#256-check-gunicorn-service-is-running)  
     - [2.5.7 Check Gunicorn Logs](#257-check-gunicorn-log)  

3. [Configure Nginx on Ubuntu](#configure-nginx-on-ubuntu)  
   - [3.1 Verify DNS](#31-verify-dns)  
   - [3.2 Check Firewall](#32-check-firewall)  
   - [3.3 Verify Nginx is Listening](#33-verify-nginx-is-listening)  

4. [Install Certbot and Nginx Plugin](#install-certbot-and-nginx-plugin)  
   - [4.1 Nginx + Let's Encrypt Setup](#41-nginx--lets-encrypt-setup-for-unigoai)  
     - [4.1.1 Open Port 80](#411-open-port-80-http)  
     - [4.1.2 Configure Nginx](#412-configure-nginx)  
     - [4.1.3 Verify Nginx](#413-verify-nginx-is-listening)  
     - [4.1.4 Install Certbot](#414-install-certbot-and-nginx-plugin)  
     - [4.1.5 Request SSL Certificate](#415-request-ssl-certificate)  
     - [4.1.6 Verify HTTPS](#416-verify-https)  
     - [4.1.7 Launch Flask App](#417-launch-flask-app)  
     - [4.1.8 Automatic Renewal](#418-automatic-renewal)  
     - [4.1.9 Notes](#419-notes)  

5. [Demo Users Info](#users-info-exist-for-demo)

---

## 1. UniGo Website Overview

A Flask-based web application for managing software downloads and updates.  
🔗 [https://unigo.ai](https://unigo.ai)

### 1.1 Project Structure (Local)

```
unigo_website/
├── app.py               # Main Flask application
├── db/
│   └── crm.db           # ✅ SQLite database
├── templates/           # Jinja2 templates
│   └── *.html
├── static/              # Static files
│   ├── uploads/         # File uploads
│   ├── i18n/            # Multi-language
│   ├── images/          # Images
│   ├── style.css        # CSS
│   └── forum.css        # CSS
├── requirements.txt     # ✅ Dependencies
├── .gitignore           # Git ignore rules
└── README.md            # Documentation
```

---

## 2. Deployment Guide

### 2.1 Push Project to GitHub

```bash
cd unigo_website/
git init
git add .
git commit -m "initial commit"
git remote add origin https://github.com/xuan139/unigo_website
git push -u origin main
```

⚠️ Ensure `.gitignore` excludes cache/temp files but **NOT `db/crm.db`**.

Example `.gitignore`:

```
__pycache__/
*.pyc
*.pyo
*.log
instance/
.env
```

### 2.2 Prepare AWS EC2 Deployment Environment

1. Create **EC2 instance** (Ubuntu 22.04)  
2. Configure **security groups**:  
   - TCP 22 (SSH)  
   - TCP 80 (HTTP)  
   - TCP 443 (HTTPS)  
3. SSH login:

```bash
ssh -i your-key.pem ubuntu@your-ec2-public-ip
```

### 2.3 Deploy Project on EC2 Server for the First Time

```bash
sudo apt update
sudo apt install git python3-pip python3-venv nginx -y

git clone https://github.com/xuan139/unigo_website
cd unigo_website

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn
```

### 2.4 Start Flask with Gunicorn

```bash
sudo pkill -f gunicorn
sudo gunicorn -w 4 -b 0.0.0.0:5050 app:app   --access-logfile gunicorn_access.log   --error-logfile gunicorn_error.log -D
```

Test:

```bash
curl http://localhost:5050
```

### 2.5 Update Website on EC2

#### 2.5.1 Push Code to GitHub with crm.db

```bash
git add .
git commit -m "update"
git push origin main
```

#### 2.5.2 On Ubuntu

```bash
cd /home/unigo_website
```

#### 2.5.3 Pull Newest Code

```bash
git fetch --all
git reset --hard origin/main
```

#### 2.5.4 Activate venv & Install Dependencies

```bash
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn
```

#### 2.5.5 Restart Gunicorn

```bash
pkill -f gunicorn
gunicorn -w 4 -b 0.0.0.0:5050 app:app   --access-logfile gunicorn_access.log   --error-logfile gunicorn_error.log -D
```
```bash
#!/bin/bash
# restart_gunicorn.sh
# 描述: 停止当前运行的 Gunicorn 并启动新的进程

APP_MODULE="app:app"
BIND_ADDR="0.0.0.0:5050"
WORKERS=4
ACCESS_LOG="gunicorn_access.log"
ERROR_LOG="gunicorn_error.log"

echo "Stopping existing Gunicorn processes..."
pkill -f gunicorn

echo "Starting Gunicorn..."
gunicorn -w $WORKERS -b $BIND_ADDR $APP_MODULE \
    --access-logfile $ACCESS_LOG \
    --error-logfile $ERROR_LOG -D

echo "Gunicorn restarted successfully."
```

#### 2.5.6 Check Gunicorn Running

```bash
ps aux | grep gunicorn
curl http://localhost:5050
```

#### 2.5.7 Check Gunicorn Logs

```bash
tail -n 50 gunicorn_error.log
tail -n 50 gunicorn_access.log
```


## 3. Configure Nginx on Ubuntu

### 3.1 Verify DNS

```bash
dig +short unigo.ai
dig +short www.unigo.ai
```

Expected:  
```
18.183.186.19
18.183.186.19
```

### 3.2 Check Firewall

```bash
sudo ufw status
```

### 3.3 Verify Nginx is Listening

```bash
sudo lsof -i :80
```

Expected:

```
nginx   12332 root     TCP *:http (LISTEN)
nginx   12333 www-data TCP *:http (LISTEN)
```

Test:

```bash
curl http://unigo.ai
```


## 4. Install Certbot and Nginx Plugin

### 4.1 Nginx + Let's Encrypt Setup for unigo.ai

#### 4.1.1 Open Port 80 (HTTP)

```bash
sudo ufw allow 80/tcp
sudo ufw enable
sudo ufw status
```

#### 4.1.2 Configure Nginx


Example:

#### Setup Hello Unigo Web Page for Nginx

This guide explains how to create a simple test web page at
`/var/www/unigo.ai` that shows **Hello Unigo**.

------------------------------------------------------------------------

##### Step 1: Create the Website Root Directory

``` bash
sudo mkdir -p /var/www/unigo.ai
```

------------------------------------------------------------------------

##### Step 2: Create a Test HTML Page

``` bash
echo "Hello Unigo" | sudo tee /var/www/unigo.ai/index.html
```

This creates `/var/www/unigo.ai/index.html` with the following content:

``` html
Hello Unigo
```

------------------------------------------------------------------------

##### Step 3: Set Permissions

``` bash
sudo chown -R www-data:www-data /var/www/unigo.ai
sudo chmod -R 755 /var/www/unigo.ai
```

Now your Nginx root directory is ready with a test page.
Then

```bash
sudo nano /etc/nginx/sites-available/unigo.ai
```

```nginx
server {
    listen 80;
    server_name unigo.ai www.unigo.ai;
    root /var/www/unigo.ai;
    index index.html;

    location / {
        try_files $uri $uri/ =404;
    }
}
```

Enable:

```bash
sudo ln -s /etc/nginx/sites-available/unigo.ai /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

#### 4.1.3 Verify Nginx is Listening

```bash
sudo lsof -i :80
curl http://unigo.ai
Hello Unigo
```

#### 4.1.4 Install Certbot

```bash
sudo apt update
sudo apt install certbot python3-certbot-nginx -y
```

#### 4.1.5 Request SSL Certificate

```bash
sudo certbot --nginx -d unigo.ai -d www.unigo.ai
```

#### 4.1.6 Verify HTTPS

```bash
curl -I https://unigo.ai
```

#### 4.1.7 Launch Flask App 

```bash
sudo nano /etc/nginx/sites-available/unigo.ai
```

```nginx
server {
    listen 80;
    server_name unigo.ai www.unigo.ai;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    server_name unigo.ai www.unigo.ai;

    ssl_certificate /etc/letsencrypt/live/unigo.ai/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/unigo.ai/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

    access_log /var/log/nginx/unigo.ai.access.log;
    error_log /var/log/nginx/unigo.ai.error.log;

    location / {
        proxy_pass http://127.0.0.1:5050;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```
```bash
sudo ln -s /etc/nginx/sites-available/unigo.ai /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```
#### 4.1.8 Automatic Renewal

```bash
sudo certbot renew --dry-run
```

#### 4.1.9 Notes

- Ensure domain resolves to correct IP  
- Port 80 must be open for Let's Encrypt  
- Redirect HTTP → HTTPS after SSL setup  

---

## 5. Demo Users Info

- **User1**  
  Email: `user1@example.com`  
  Password: `e7KO24UX`  

- **User2**  
  Email: `user2@example.com`  
  Password: `Qye4HCZb`  

- **User3**  
  Email: `user3@example.com`  
  Password: `mwL6PnZa`

## 6. mysql 和 nginx 设置tips

### for detail check 
 
 - Mysql Installation Guide.pdf
 - Mysql Remote Access Guide
 - mysql_dump.sql

### 6.1 new user

ALTER USER 'root'@'localhost' IDENTIFIED WITH
mysql_native_password BY 'unigo!@#123';
FLUSH PRIVILEGES;

ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'unigo123!@#';
FLUSH PRIVILEGES;
EXIT;

ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'UnigoStrong123!@#';
FLUSH PRIVILEGES;

### 6.2 connect to MySql svever
 - 18.183.186.19

 - mysql -h 18.183.186.19 -P 3306 -u root -p
 - Enter password: UnigoStrong123!@#

 - UnigoStrong123!@#

CREATE USER 'unigo_remote'@'%' IDENTIFIED BY 'StrongPassword123!';
GRANT ALL PRIVILEGES ON *.* TO 'unigo_remote'@'%' WITH GRANT OPTION;
FLUSH PRIVILEGES;

  - mysql -h 18.183.186.19 -u unigo_remote -p

### 6.3 migrate sqlite to mysql 

  - CREATE DATABASE crm DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
  - USE crm;

  - mysql -h 18.183.186.19 -u root -p crm < dump.sql

### 6.4 max file upload size
  - 打开你的 Nginx 配置文件：

  - 全局修改：/etc/nginx/nginx.conf

  - 或者针对你站点的配置文件：/etc/nginx/sites-available/your_site

  - 在 http、server 或 location 块中添加：

  - client_max_body_size 3G;
