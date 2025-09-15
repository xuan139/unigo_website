          		*UniGo Website Deploy Manual*

# 

*Application Name: \[OStation\]*  
*Version: \[1.1\]*  
*Author: \[XUAN\]*  
*Date: \[15/09/2025\]*

# 

# 

*[**1\. UniGo Website Overview	4**](#unigo-website-overview)*

[*1.1  Project Structure local	4*](#1.1-project-structure-local)

[***2\. Deployment Guide	6***](#deployment-guide)

[*2.1 Push Project to GitHub	6*](#2.1-push-project-to-github)

[*2.2 Prepare AWS EC2 Deployment Environment	7*](#2.2-prepare-aws-ec2-deployment-environment)

[*2.3 Deploy Project on EC2 Server for the First Time	7*](#2.3-deploy-project-on-ec2-server-for-the-first-time)

[*2.4 Start Flask with Gunicorn	8*](#2.4-start-flask-with-gunicorn)

[*2.5 Update Ubuntu Website	9*](#2.5-update-ubuntu-website)

[*2.5.1 Push code to github with crm.db from local	9*](#2.5.1-push-code-to-github-with-crm.db-from-local)

[*2.5.2 On Ubuntu	9*](#2.5.2-on-ubuntu)

[*2.5.3 Pull newest code from github	9*](#2.5.3-pull-newest-code-from-github)

[*2.5.4 Active venv and install requirements.txt	9*](#2.5.4-active-venv-and-install-requirements.txt)

[*2.5.5 Restart  Gunicorn service	9*](#2.5.5-restart-gunicorn-service)

[*2.5.6 Check gunicorn service is running	9*](#2.5.6-check-gunicorn-service-is-running)

[***3\. Configure Nginx on Ubuntu	11***](#configure-nginx-on-ubuntu)

[*3.1 Verify DNS	11*](#3.1-verify-dns)

[*3.2 Check Firewall	11*](#3.2-check-firewall)

[*3.3 Verify Nginx is Listening	12*](#3.3-verify-nginx-is-listening)

[***4\. Install Certbot and Nginx Plugin	13***](#install-certbot-and-nginx-plugin)

[*4.1 Nginx \+ Let's Encrypt Setup for unigo.ai	13*](#4.1-nginx-+-let's-encrypt-setup-for-unigo.ai)

[*4.1.1 Open Port 80 (HTTP)	13*](#4.1.1-open-port-80-\(http\))

[*4.1.2 Configure Nginx	13*](#4.1.2-configure-nginx)

[*4.1.3 Verify Nginx is Listening	14*](#4.1.3-verify-nginx-is-listening)

[*4.1.4 Install Certbot and Nginx Plugin	15*](#4.1.4-install-certbot-and-nginx-plugin)

[*4.1.5 Request SSL Certificate	15*](#4.1.5-request-ssl-certificate)

[*4.1.6 Verify HTTPS	16*](#4.1.6-verify-https)

[*4.1.7 Automatic Renewal	16*](#4.1.7-automatic-renewal)

[*\#\# Notes	16*](###-notes)

[*\#\# Notes	17*](###-notes-1)

[***Users Info Exist for Demo	18***](#users-info-exist-for-demo)

# 

# 

# 

1. # *UniGo Website Overview* {#unigo-website-overview}

   *A Flask-based web application for managing software downloads and updates.*  
   *\[[unigo.ai](http://unigo.ai)\](https://unigo.ai)*  
   

   ## *1.1  Project Structure local* {#1.1-project-structure-local}

     
   *unigo\_website/*  
   *├── app.py                 \# Main Flask application*  
   *├── db/*  
   *│   └── crm.db            \# ✅ SQLite database*  
   *├── templates/*  
   *│   └── \*.html            \# HTML templates*  
   *├── /static/*  
   *│   └── uploads/          \# File uploads directory*  
   *│   └── i18n/             \# Multi language*  
   *│   └── images/           \# images*  
   *│   └── style.css         \# css*  
   *│   └── forum.css         \# css*  
   *├── requirements.txt      \# ✅ Python package dependencies*  
   *├── .gitignore            \# Git ignore rules*  
   *└── README.md             \# Project documentation*

2. # *Deployment Guide* {#deployment-guide}

##  *2.1 Push Project to GitHub* {#2.1-push-project-to-github}

*bash*  
*cd unigo\_website/*  
*git init*  
*git add .*  
*git commit \-m "initial commit"*  
*git remote add origin https://github.com/xuan139/unigo\_website*  
*git push \-u origin main*  
*\*\*Important\*\*: Ensure \`.gitignore\` excludes cache or temporary files, but \*\*DO NOT\*\* ignore \`db/crm.db\` as you need to migrate data\!*  
*Example \`.gitignore\`:*  
*\`\`\`txt*  
*\_\_pycache\_\_/*  
*\*.pyc*  
*\*.pyo*  
*\*.log*  
*instance/*  
*.env*

## *2.2 Prepare AWS EC2 Deployment Environment* {#2.2-prepare-aws-ec2-deployment-environment}

*1\. \*\*Create EC2 Instance\*\*: Ubuntu 22.04*  
*2\. \*\*Configure Security Groups\*\*:*  
  *\- TCP 22 (SSH)*  
  *\- TCP 80 (HTTP)*  
  *\- TCP 443 (HTTPS)*  
*3\. \*\*SSH Login\*\*:*  
*bash*  
*ssh \-i your-key.pem ubuntu@your-ec2-public-ip*

## *2.3 Deploy Project on EC2 Server for the First Time* {#2.3-deploy-project-on-ec2-server-for-the-first-time}

*bash*  
*\# Install dependencies*  
*sudo apt update*  
*sudo apt install git python3-pip python3-venv nginx \-y*  
*\# Clone project*  
*git clone https://github.com/xuan139/unigo\_website*  
*cd unigo\_website*  
*\# Create virtual environment*  
*python3 \-m venv venv*  
*source venv/bin/activate*  
*\# Install dependencies*  
*pip install \-r requirements.txt*  
*Pip install gunicorn*

## *2.4 Start Flask with Gunicorn* {#2.4-start-flask-with-gunicorn}

*bash*  
*sudo pkill \-f gunicorn*  
*sudo gunicorn \-w 4 \-b 0.0.0.0:5050 app:app \\*  
 *\--access-logfile gunicorn\_access.log \\*  
 *\--error-logfile gunicorn\_error.log \-D*  
*Test with: \`curl http://localhost:5050\`*  
*Certificate renewal will be automatically ad*

## *2.5 Update Ubuntu Website* {#2.5-update-ubuntu-website}

###  *2.5.1 Push code to github with crm.db from local* {#2.5.1-push-code-to-github-with-crm.db-from-local}

*git add .*  
*git commit \-m "update"*  
*git push origin main*

###  *2.5.2 On Ubuntu* {#2.5.2-on-ubuntu}

*cd /home/unigo\_website*

###  *2.5.3 Pull newest code from github* {#2.5.3-pull-newest-code-from-github}

*git fetch \--all*  
*git reset \--hard origin/main*

### *2.5.4 Active venv and install requirements.txt* {#2.5.4-active-venv-and-install-requirements.txt}

*source venv/bin/activate*  
*pip install \-r requirements.txt*  
*pip install gunicorn*

### *2.5.5 Restart  Gunicorn service* {#2.5.5-restart-gunicorn-service}

*pkill \-f gunicorn*  
*gunicorn \-w 4 \-b 0.0.0.0:5050 app:app \\*  
 *\--access-logfile gunicorn\_access.log \\*  
 *\--error-logfile gunicorn\_error.log \-D*

### *2.5.6 Check gunicorn service is running* {#2.5.6-check-gunicorn-service-is-running}

*ps aux | grep gunicorn*  
*curl [http://localhost:5050](http://localhost:5050)*

3. # *Configure Nginx on Ubuntu*  {#configure-nginx-on-ubuntu}

   *Domain name*  
   *\[[unigo.ai](http://unigo.ai)\](https://unigo.ai)*

## *3.1 Verify DNS* {#3.1-verify-dns}

*Check that your domain points to your server IP:*  
*\`\`\`bash*  
*dig \+short unigo.ai*  
*dig \+short www.unigo.ai*  
*\`\`\`*  
*Expected output:*  
*\`\`\`*  
*18.183.186.19*  
*18.183.186.19*  
*\`\`\`*

## *3.2 Check Firewall* {#3.2-check-firewall}

*Verify if \`ufw\` is active:*  
*\`\`\`bash*  
*sudo ufw status*  
*\`\`\`*  
*If inactive, no extra firewall rules are blocking HTTP/HTTPS.*

## *3.3 Verify Nginx is Listening* {#3.3-verify-nginx-is-listening}

*Check if Nginx is running on port 80:*  
*bash*  
*sudo lsof \-i :80*  
*You should see something like:*

*COMMAND   PID     USER   FD   TYPE DEVICE SIZE/OFF NODE NAME*  
*nginx     12332   root   5u   IPv4  44161  0t0      TCP \*:http (LISTEN)*  
*nginx     12333 www-data 5u   IPv4 44161  0t0      TCP \*:http (LISTEN)*

*Test local access:*  
*\`\`\`bash*  
*curl http://unigo.ai*  
*\`\`\`*  
*Expected output:*  
*\`\`\`*  
*Hello from unigo.ai*  
*\`\`\`*

4. # *Install Certbot and Nginx Plugin* {#install-certbot-and-nginx-plugin}

## *4.1 Nginx \+ Let's Encrypt Setup for unigo.ai* {#4.1-nginx-+-let's-encrypt-setup-for-unigo.ai}

### *4.1.1 Open Port 80 (HTTP)* {#4.1.1-open-port-80-(http)}

*Before requesting a certificate, ensure port 80 is open for Let's Encrypt HTTP challenge.*  
*\`\`\`bash*  
*sudo ufw allow 80/tcp*  
*sudo ufw enable   \# if not already enabled*  
*sudo ufw status*  
*\`\`\`*  
*You should see:*  
*\`\`\`*  
*80/tcp                     ALLOW       Anywhere*  
*\`	\`\`*

### *4.1.2 Configure Nginx* {#4.1.2-configure-nginx}

*Create a server block for your domain:*  
*\`\`\`bash*  
*sudo nano /etc/nginx/sites-available/[unigo.ai](http://unigo.ai)*  
*\`\`\`*  
*Example configuration:*  
*\`\`\`nginx*  
*server {*  
    *listen 80;*  
    *server\_name unigo.ai www.unigo.ai;*  
    *root /var/www/unigo.ai;*  
    *index index.html;*  
    *location / {*  
        *try\_files $uri $uri/ \=404;*  
    *}*  
*}*  
*\`\`\`*  
*Enable the site:*  
*\`\`\`bash*  
*sudo ln \-s /etc/nginx/sites-available/unigo.ai /etc/nginx/sites-enabled/*  
*sudo nginx \-t*  
*sudo systemctl reload nginx*  
*\`\`\`*

### *4.1.3 Verify Nginx is Listening* {#4.1.3-verify-nginx-is-listening}

*\`\`\`bash*  
*sudo lsof \-i :80*  
*\`\`\`*  
*Expected output:*  
*\`\`\`*  
*COMMAND   PID     USER   FD   TYPE DEVICE SIZE/OFF NODE NAME*  
*nginx     12332   root   5u   IPv4  44161  0t0      TCP \*:http (LISTEN)*  
*nginx     12333 www-data 5u  IPv4 44161 0t0      TCP \*:http (LISTEN)*  
*\`\`\`*  
*Test local access:*  
*\`\`\`bash*  
*curl http://unigo.ai*  
*\`\`\`*  
*Expected response:*  
*\`\`\`*  
*Hello from [unigo.ai](http://unigo.ai)*

### *4.1.4 Install Certbot and Nginx Plugin* {#4.1.4-install-certbot-and-nginx-plugin}

*\`\`\`bash*  
*sudo apt update*  
*sudo apt install certbot python3-certbot-nginx \-y*  
*\`\`\`*

### *4.1.5 Request SSL Certificate* {#4.1.5-request-ssl-certificate}

*\`\`\`bash*  
*sudo certbot \--nginx \-d unigo.ai \-d www.unigo.ai*  
*\`\`\`*  
*Expected success message:*  
*\`\`\`*  
*Successfully received certificate.*  
*Certificate is saved at: /etc/letsencrypt/live/unigo.ai/fullchain.pem*  
*Key is saved at:         /etc/letsencrypt/live/unigo.ai/privkey.pem*  
*Certificate expires on:  2025-12-14*  
*Successfully deployed certificate for unigo.ai to /etc/nginx/sites-enabled/unigo.ai*  
*Successfully deployed certificate for www.unigo.ai to /etc/nginx/sites-enabled/unigo.ai*  
*\`\`\`*

### *4.1.6 Verify HTTPS* {#4.1.6-verify-https}

*\`\`\`bash*  
*curl \-I [https://unigo.ai](https://unigo.ai)*  
*\`\`\`*  
*You should see \`HTTP/2 200\` or \`HTTP/1.1 200 OK\`.*

### *4.1.7 Automatic Renewal* {#4.1.7-automatic-renewal}

*Certbot automatically sets up a cron job to renew certificates. Test manually:*  
*\`\`\`bash*  
*sudo certbot renew \--dry-run*

### *\#\# Notes* {###-notes}

*\- Ensure your domain \`unigo.ai\` resolves to the correct public IP.*  
*\- Firewall must allow HTTP (port 80\) for certificate issuance.*  
*\- After successful SSL setup, you can optionally redirect HTTP to HTTPS in Nginx.*

### *\#\# Notes* {###-notes-1}

*\- Ensure your domain resolves to the correct public IP.*  
*\- Nginx must be accessible from the Internet for Certbot HTTP challenge.*

# *Users Info Exist for Demo* {#users-info-exist-for-demo}

*\- \*\*User1\*\**   
 *Email: \`user1@example.com\`*   
 *Password: \`e7KO24UX\`*  
*\- \*\*User2\*\**   
 *Email: \`user2@example.com\`*   
 *Password: \`Qye4HCZb\`*  
*\- \*\*User3\*\**   
 *Email: \`user3@example.com\`*   
 *Password: \`mwL6PnZa\`*  
