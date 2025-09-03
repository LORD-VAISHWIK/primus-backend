# 🚀 Primus Backend - Ubuntu Server Deployment Guide

Complete automated deployment solution for the Primus Gaming Platform backend on Ubuntu Server.

## 🎯 Quick Start (One-Line Installation)

### For Production Deployment:
```bash
curl -sSL https://raw.githubusercontent.com/LORD-VAISHWIK/primus-backend/main/install.sh | sudo bash -s yourdomain.com your-email@domain.com
```

### For Local Development:
```bash
curl -sSL https://raw.githubusercontent.com/LORD-VAISHWIK/primus-backend/main/install.sh | sudo bash -s localhost admin@localhost
```

### Example:
```bash
curl -sSL https://raw.githubusercontent.com/LORD-VAISHWIK/primus-backend/main/install.sh | sudo bash -s primus.example.com admin@example.com
```

## 📋 What Gets Installed

### ✅ System Components
- **Ubuntu 20.04/22.04 LTS** (recommended)
- **Python 3.8+** with virtual environment
- **PostgreSQL 13+** database server
- **Redis 6+** for caching and sessions
- **Nginx** web server and reverse proxy
- **Node.js 20** for frontend builds
- **SSL/TLS certificates** via Let's Encrypt (for domains)

### ✅ Security Features
- **UFW Firewall** configured
- **Fail2ban** protection
- **Secure headers** in Nginx
- **Rate limiting** for API endpoints
- **Auto-generated secure passwords**
- **SSL/HTTPS enforcement** (for domains)

### ✅ Production Features
- **Systemd service** management
- **Gunicorn WSGI** server with 4 workers
- **Log rotation** and management
- **Automated daily backups**
- **Health monitoring** scripts
- **Process supervision** and auto-restart

### ✅ Application Features
- **FastAPI backend** with all endpoints
- **WebSocket support** for real-time features
- **Database migrations** with Alembic
- **File upload handling**
- **Payment gateway integration** (Stripe, Razorpay)
- **Firebase authentication** support
- **Email/SMTP configuration**

## 🛠️ Manual Installation Options

### Option 1: Download and Run Locally
```bash
# Download the automated script
wget https://raw.githubusercontent.com/LORD-VAISHWIK/primus-backend/main/deploy_ubuntu_auto.sh

# Make it executable
chmod +x deploy_ubuntu_auto.sh

# Run with your domain and email
sudo ./deploy_ubuntu_auto.sh yourdomain.com your-email@domain.com
```

### Option 2: Clone Repository First
```bash
# Clone the repository
git clone https://github.com/LORD-VAISHWIK/primus-backend.git
cd primus-backend

# Run the automated deployment
sudo ./deploy_ubuntu_auto.sh yourdomain.com your-email@domain.com
```

### Option 3: Docker Deployment
```bash
# Clone the repository
git clone https://github.com/LORD-VAISHWIK/primus-backend.git
cd primus-backend

# Update environment variables in docker-compose.yml
nano docker-compose.yml

# Deploy with Docker Compose
docker-compose up -d
```

## ⚙️ Post-Installation Configuration

After installation, you'll need to update these configuration files:

### 1. Environment Variables (`/var/www/primus/backend/.env`)
```bash
sudo nano /var/www/primus/backend/.env
```

**Update these important settings:**
```env
# Email/SMTP Configuration
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SMTP_FROM_EMAIL=noreply@yourdomain.com

# Payment Gateway Keys
STRIPE_SECRET_KEY=sk_live_your_stripe_key
STRIPE_PUBLISHABLE_KEY=pk_live_your_stripe_key
RAZORPAY_KEY_ID=your_razorpay_key_id
RAZORPAY_KEY_SECRET=your_razorpay_key_secret

# Firebase (Optional)
FIREBASE_CREDENTIALS_JSON={"type":"service_account",...}
```

### 2. Restart Services After Configuration
```bash
sudo systemctl restart primus-backend
sudo systemctl reload nginx
```

## 🌐 Access Your Application

After successful deployment:

### API Documentation
- **Swagger UI**: `https://yourdomain.com/docs`
- **ReDoc**: `https://yourdomain.com/redoc`

### API Endpoints
- **Base URL**: `https://yourdomain.com/api`
- **WebSocket**: `https://yourdomain.com/ws`
- **Health Check**: `https://yourdomain.com/health`

### Admin Panel (After Frontend Deployment)
- **Admin Dashboard**: `https://yourdomain.com`

## 📊 Management Commands

### Service Management
```bash
# Check status of all services
/usr/local/bin/primus-status.sh

# Restart backend service
sudo systemctl restart primus-backend

# View backend logs
sudo journalctl -u primus-backend -f

# View Nginx logs
sudo tail -f /var/log/nginx/error.log

# Check system resources
htop
```

### Database Management
```bash
# Connect to PostgreSQL
sudo -u postgres psql primus_db

# Create database backup
/usr/local/bin/primus-backup.sh

# View recent backups
ls -la /var/www/primus/backups/
```

### SSL Certificate Management
```bash
# Renew SSL certificates manually
sudo certbot renew

# Check certificate status
sudo certbot certificates

# Test certificate renewal
sudo certbot renew --dry-run
```

## 🔧 Troubleshooting

### Common Issues and Solutions

#### 1. Backend Service Won't Start
```bash
# Check logs for errors
sudo journalctl -u primus-backend -n 50

# Check if port 8000 is available
sudo netstat -tulpn | grep :8000

# Restart the service
sudo systemctl restart primus-backend
```

#### 2. Database Connection Issues
```bash
# Check PostgreSQL status
sudo systemctl status postgresql

# Test database connection
sudo -u postgres psql -c "\l"

# Check database credentials in .env file
sudo cat /var/www/primus/backend/.env | grep DATABASE_URL
```

#### 3. Nginx Configuration Issues
```bash
# Test Nginx configuration
sudo nginx -t

# Reload Nginx configuration
sudo systemctl reload nginx

# Check Nginx error logs
sudo tail -f /var/log/nginx/error.log
```

#### 4. SSL Certificate Issues
```bash
# Check certificate status
sudo certbot certificates

# Manually renew certificates
sudo certbot renew --force-renewal

# Check if domain DNS is pointing to server
nslookup yourdomain.com
```

#### 5. Permission Issues
```bash
# Fix file permissions
sudo chown -R primus:primus /var/www/primus
sudo chmod -R 755 /var/www/primus
sudo chmod 600 /var/www/primus/backend/.env
```

### Log Locations
- **Backend Logs**: `/var/log/primus/`
- **Nginx Logs**: `/var/log/nginx/`
- **System Logs**: `journalctl -u primus-backend`
- **PostgreSQL Logs**: `/var/log/postgresql/`

## 🔒 Security Recommendations

### 1. Update System Regularly
```bash
sudo apt update && sudo apt upgrade -y
```

### 2. Configure Fail2ban (Optional)
```bash
sudo apt install fail2ban
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

### 3. Set Up Additional Monitoring
```bash
# Install monitoring tools
sudo apt install htop iotop nethogs

# Set up log monitoring
sudo apt install logwatch
```

### 4. Backup Strategy
- **Automated**: Daily backups are configured automatically
- **Manual**: Run `/usr/local/bin/primus-backup.sh`
- **Offsite**: Consider copying backups to cloud storage

## 📱 Frontend Deployment

After backend deployment, deploy your React frontend:

### 1. Clone Frontend Repository
```bash
cd /var/www/primus
sudo git clone https://github.com/your-username/primus-frontend.git frontend
cd frontend
```

### 2. Build Frontend
```bash
sudo npm install
sudo npm run build
```

### 3. Configure Nginx (Already Done)
The Nginx configuration is already set up to serve the frontend from `/var/www/primus/frontend/dist`.

## 🚀 Performance Optimization

### 1. Database Optimization
```sql
-- Connect to PostgreSQL and run these optimizations
sudo -u postgres psql primus_db

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_sessions_user_id ON sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_pcs_current_user ON client_pcs(current_user_id);
```

### 2. Redis Configuration
Edit `/etc/redis/redis.conf` for production:
```bash
maxmemory 512mb
maxmemory-policy allkeys-lru
```

### 3. Nginx Caching (Optional)
Add caching configuration to Nginx for better performance.

## 📞 Support

- **Documentation**: Check the API docs at `/docs`
- **Issues**: Create issues on GitHub repository
- **Logs**: Always check logs first for troubleshooting
- **Community**: Join discussions on GitHub

## 🎉 Success!

Your Primus Gaming Platform backend is now running in production!

**Next Steps:**
1. Configure email and payment settings
2. Deploy your frontend application
3. Set up monitoring and alerting
4. Configure regular offsite backups
5. Test all functionality thoroughly

---

**Made with ❤️ for the Primus Gaming Platform**
