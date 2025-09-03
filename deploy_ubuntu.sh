#!/bin/bash

# =============================================================================
# PRIMUS BACKEND - UBUNTU SERVER DEPLOYMENT SCRIPT
# =============================================================================
# This script sets up the Primus backend on Ubuntu server
# Run with: chmod +x deploy_ubuntu.sh && sudo ./deploy_ubuntu.sh

set -e  # Exit on any error

echo "🚀 Starting Primus Backend deployment on Ubuntu..."

# =============================================================================
# SYSTEM UPDATES & BASIC PACKAGES
# =============================================================================
echo "📦 Updating system packages..."
apt update && apt upgrade -y

echo "🔧 Installing essential build tools..."
apt install -y \
    python3 \
    python3-dev \
    python3-pip \
    python3-venv \
    build-essential \
    pkg-config \
    curl \
    wget \
    git \
    unzip \
    software-properties-common \
    apt-transport-https \
    ca-certificates \
    gnupg \
    lsb-release

# =============================================================================
# POSTGRESQL DATABASE
# =============================================================================
echo "🗄️ Installing PostgreSQL..."
apt install -y postgresql postgresql-contrib libpq-dev

echo "🔐 Setting up PostgreSQL database..."
sudo -u postgres psql -c "CREATE USER primus WITH PASSWORD 'primus123';" || true
sudo -u postgres psql -c "CREATE DATABASE primus_db OWNER primus;" || true
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE primus_db TO primus;" || true

# Enable PostgreSQL to start on boot
systemctl enable postgresql
systemctl start postgresql

# =============================================================================
# REDIS (for caching and sessions)
# =============================================================================
echo "🔴 Installing Redis..."
apt install -y redis-server

# Configure Redis
sed -i 's/supervised no/supervised systemd/' /etc/redis/redis.conf
systemctl enable redis-server
systemctl start redis-server

# =============================================================================
# NGINX (Web Server & Reverse Proxy)
# =============================================================================
echo "🌐 Installing Nginx..."
apt install -y nginx

# Enable Nginx
systemctl enable nginx
systemctl start nginx

# =============================================================================
# SUPERVISOR (Process Management)
# =============================================================================
echo "👥 Installing Supervisor..."
apt install -y supervisor
systemctl enable supervisor
systemctl start supervisor

# =============================================================================
# SSL/TLS CERTIFICATES (Let's Encrypt)
# =============================================================================
echo "🔒 Installing Certbot for SSL certificates..."
apt install -y certbot python3-certbot-nginx

# =============================================================================
# NODE.JS (for frontend)
# =============================================================================
echo "📦 Installing Node.js..."
curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
apt install -y nodejs

# =============================================================================
# PYTHON ENVIRONMENT SETUP
# =============================================================================
echo "🐍 Setting up Python environment..."

# Create application directory
mkdir -p /var/www/primus
cd /var/www/primus

# Clone repository (replace with your actual repo)
echo "📥 Cloning repository..."
git clone https://github.com/LORD-VAISHWIK/primus-backend.git backend || true
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip setuptools wheel

# Install Python dependencies
echo "📚 Installing Python packages..."
pip install -r requirements.txt

# =============================================================================
# ENVIRONMENT CONFIGURATION
# =============================================================================
echo "⚙️ Setting up environment configuration..."

# Create .env file template
cat > .env << EOF
# Database Configuration
DATABASE_URL=postgresql://primus:primus123@localhost:5432/primus_db

# Security
SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))")
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS Settings
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173,https://yourdomain.com

# Redis Configuration
REDIS_URL=redis://127.0.0.1:6379/0

# SMTP Configuration (update with your settings)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SMTP_FROM_EMAIL=your-email@gmail.com

# Application Settings
APP_BASE_URL=https://yourdomain.com
API_BASE_URL=https://yourdomain.com/api

# Firebase (optional - add your credentials)
FIREBASE_CREDENTIALS_JSON={}

# Payment Gateways (add your keys)
STRIPE_SECRET_KEY=sk_test_your_stripe_key
STRIPE_PUBLISHABLE_KEY=pk_test_your_stripe_key
RAZORPAY_KEY_ID=your_razorpay_key_id
RAZORPAY_KEY_SECRET=your_razorpay_key_secret

# File Upload Settings
UPLOAD_DIR=/var/www/primus/uploads
MAX_FILE_SIZE=10485760

EOF

# Create uploads directory
mkdir -p /var/www/primus/uploads
chown -R www-data:www-data /var/www/primus/uploads

# =============================================================================
# DATABASE MIGRATIONS
# =============================================================================
echo "🗃️ Running database migrations..."
cd /var/www/primus/backend
source venv/bin/activate

# Initialize Alembic if not already done
alembic upgrade head || echo "⚠️ Migrations failed - you may need to initialize Alembic"

# =============================================================================
# SYSTEMD SERVICE CONFIGURATION
# =============================================================================
echo "🔧 Creating systemd service..."

cat > /etc/systemd/system/primus-backend.service << EOF
[Unit]
Description=Primus Backend FastAPI application
After=network.target postgresql.service redis-server.service

[Service]
Type=notify
User=www-data
Group=www-data
WorkingDirectory=/var/www/primus/backend
Environment=PATH=/var/www/primus/backend/venv/bin
ExecStart=/var/www/primus/backend/venv/bin/gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app --bind 127.0.0.1:8000 --timeout 120 --keep-alive 2 --max-requests 1000 --max-requests-jitter 100
ExecReload=/bin/kill -s HUP \$MAINPID
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

# =============================================================================
# NGINX CONFIGURATION
# =============================================================================
echo "🌐 Configuring Nginx..."

cat > /etc/nginx/sites-available/primus << EOF
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;  # Replace with your domain
    
    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    
    # Client max body size (for file uploads)
    client_max_body_size 10M;
    
    # Backend API
    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_cache_bypass \$http_upgrade;
        proxy_read_timeout 300s;
        proxy_connect_timeout 75s;
    }
    
    # WebSocket connections
    location /ws/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
    
    # Frontend (React app)
    location / {
        root /var/www/primus/frontend/dist;
        try_files \$uri \$uri/ /index.html;
        
        # Cache static assets
        location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)\$ {
            expires 1y;
            add_header Cache-Control "public, immutable";
        }
    }
    
    # Uploads directory
    location /uploads/ {
        alias /var/www/primus/uploads/;
        expires 1y;
        add_header Cache-Control "public";
    }
}
EOF

# Enable the site
ln -sf /etc/nginx/sites-available/primus /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default

# Test nginx configuration
nginx -t

# =============================================================================
# FIREWALL CONFIGURATION
# =============================================================================
echo "🔥 Configuring UFW firewall..."
ufw --force enable
ufw allow ssh
ufw allow 'Nginx Full'
ufw allow 5432  # PostgreSQL (only if external access needed)

# =============================================================================
# SET PERMISSIONS
# =============================================================================
echo "🔐 Setting proper permissions..."
chown -R www-data:www-data /var/www/primus
chmod -R 755 /var/www/primus
chmod 600 /var/www/primus/backend/.env

# =============================================================================
# START SERVICES
# =============================================================================
echo "🚀 Starting services..."

# Reload systemd and start services
systemctl daemon-reload
systemctl enable primus-backend
systemctl start primus-backend

# Restart nginx
systemctl reload nginx

# =============================================================================
# FINAL INSTRUCTIONS
# =============================================================================
echo ""
echo "✅ Primus Backend deployment completed!"
echo ""
echo "📋 Next steps:"
echo "1. Update .env file with your actual configuration:"
echo "   nano /var/www/primus/backend/.env"
echo ""
echo "2. Update Nginx configuration with your domain:"
echo "   nano /etc/nginx/sites-available/primus"
echo ""
echo "3. Set up SSL certificate:"
echo "   sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com"
echo ""
echo "4. Deploy your frontend:"
echo "   cd /var/www/primus"
echo "   git clone https://github.com/your-username/primus-frontend.git frontend"
echo "   cd frontend && npm install && npm run build"
echo ""
echo "5. Check service status:"
echo "   systemctl status primus-backend"
echo "   systemctl status nginx"
echo "   systemctl status postgresql"
echo "   systemctl status redis-server"
echo ""
echo "6. View logs:"
echo "   journalctl -u primus-backend -f"
echo "   tail -f /var/log/nginx/error.log"
echo ""
echo "🌐 Your backend will be available at: http://yourdomain.com/api"
echo "📊 Admin panel will be at: http://yourdomain.com"
echo ""
echo "🔧 Don't forget to:"
echo "   - Configure your domain DNS to point to this server"
echo "   - Update CORS origins in .env file"
echo "   - Set up proper backup procedures"
echo "   - Configure monitoring and logging"
echo ""
