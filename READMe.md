# UniGo Website

A Flask-based web application for managing software downloads and updates.

## Project Structure

```
unigo_website/
├── app.py                 # Main Flask application
├── db/
│   └── crm.db            # ✅ SQLite database
├── templates/
│   └── *.html            # HTML templates
├── static/
│   └── uploads/          # File uploads directory
├── requirements.txt      # ✅ Python package dependencies
├── .gitignore           # Git ignore rules
└── README.md            # Project documentation
```

## Deployment Guide

### Step 1: Push Project to GitHub

```bash
cd unigo_website/
git init
git add .
git commit -m "initial commit"
git remote add origin https://github.com/xuan139/unigo_website
git push -u origin main
```

**Important**: Ensure `.gitignore` excludes cache or temporary files, but **DO NOT** ignore `db/crm.db` as you need to migrate data!

Example `.gitignore`:
```txt
__pycache__/
*.pyc
*.pyo
*.log
instance/
.env
```

### Step 2: Prepare AWS EC2 Deployment Environment

1. **Create EC2 Instance**: Ubuntu 22.04
2. **Configure Security Groups**:
   - TCP 22 (SSH)
   - TCP 80 (HTTP)
   - TCP 443 (HTTPS)

3. **SSH Login**:
```bash
ssh -i your-key.pem ubuntu@your-ec2-public-ip
```

### Step 3: Deploy Project on Server

```bash
# Install dependencies
sudo apt update
sudo apt install git python3-pip python3-venv nginx -y

# Clone project
git clone https://github.com/xuan139/unigo_website
cd unigo_website

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 4: Start Flask with Gunicorn

```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```
Test with: `curl http://localhost:5000`

### Step 5: Configure Nginx Reverse Proxy + HTTPS

1. **Edit Nginx configuration**:
```bash
sudo nano /etc/nginx/sites-available/unigo
```

2. **Configuration content**:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

3. **Enable and restart Nginx**:
```bash
sudo ln -s /etc/nginx/sites-available/unigo /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Step 6: Configure HTTPS (Let's Encrypt)

```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d your-domain.com
```

Certificate renewal will be automatically added to crontab.

### Step 7: Auto Deployment Script (Optional)

Create `deploy.sh` on server:

```bash
#!/bin/bash
cd /home/unigo_website

# 获取并同步远程最新代码
git fetch --all
git reset --hard origin/main
```

## Created Users

- **User1**  
  Email: `user1@example.com`  
  Password: `e7KO24UX`

- **User2**  
  Email: `user2@example.com`  
  Password: `Qye4HCZb`

- **User3**  
  Email: `user3@example.com`  
  Password: `mwL6PnZa`

## AWS Server IP Address
3.27.169.60

### Step 8: 更新 Ubuntu Website 步骤

```bash
# 1. 推送最新代码到 GitHub（若有数据库更新更佳）
git add .
git commit -m "update"
git push origin main

# 2. 在 Ubuntu 服务器上执行以下步骤
cd /home/unigo_website

# 获取并同步远程最新代码
git fetch --all
git reset --hard origin/main

# 3. 进入虚拟环境并安装依赖
source venv/bin/activate
pip install -r requirements.txt

# 4. 重启 Gunicorn 服务
pkill -f gunicorn
gunicorn -w 4 -b 0.0.0.0:5050 app:app \
  --access-logfile gunicorn_access.log \
  --error-logfile gunicorn_error.log -D

# 5. 检查服务是否正常运行
ps aux | grep gunicorn
curl http://localhost:5050



