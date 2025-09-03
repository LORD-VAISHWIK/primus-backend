import os
from dotenv import load_dotenv

load_dotenv()

# Default to SQLite for local development; can be overridden via .env
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./lance.db")
JWT_SECRET = os.getenv("JWT_SECRET", "supersecret")

def load_from_file(filename: str):
    try:
        with open(filename, 'r') as f:
            for line in f:
                line=line.strip()
                if not line or line.startswith('#') or '=' not in line:
                    continue
                k,v = line.split('=',1)
                os.environ.setdefault(k.strip(), v.strip())
    except Exception:
        pass

# Load defaults from conf/ if present
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_from_file(os.path.join(base_dir, 'conf', 'payments.conf'))
load_from_file(os.path.join(base_dir, 'conf', 'oauth.conf'))

# Payment gateways
STRIPE_SECRET = os.getenv("STRIPE_SECRET", "")
STRIPE_CURRENCY = os.getenv("STRIPE_CURRENCY", "usd")
STRIPE_SUCCESS_URL = os.getenv("STRIPE_SUCCESS_URL", "https://example.com/success")
STRIPE_CANCEL_URL = os.getenv("STRIPE_CANCEL_URL", "https://example.com/cancel")

RAZORPAY_KEY_ID = os.getenv("RAZORPAY_KEY_ID", "")
RAZORPAY_KEY_SECRET = os.getenv("RAZORPAY_KEY_SECRET", "")
RAZORPAY_CURRENCY = os.getenv("RAZORPAY_CURRENCY", "INR")
RAZORPAY_SUCCESS_URL = os.getenv("RAZORPAY_SUCCESS_URL", "https://example.com/razorpay/success")

# OAuth providers (desktop flow)
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET", "")

# SMTP and app URL
SMTP_HOST = os.getenv("SMTP_HOST", "")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASS = os.getenv("SMTP_PASS", "")
SMTP_FROM = os.getenv("SMTP_FROM", SMTP_USER)
APP_BASE_URL = os.getenv("APP_BASE_URL", "http://localhost:8000")
DISCORD_CLIENT_ID = os.getenv("DISCORD_CLIENT_ID", "")
DISCORD_CLIENT_SECRET = os.getenv("DISCORD_CLIENT_SECRET", "")
TWITTER_CLIENT_ID = os.getenv("TWITTER_CLIENT_ID", "")
TWITTER_CLIENT_SECRET = os.getenv("TWITTER_CLIENT_SECRET", "")
