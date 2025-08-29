# Lance Backend API

A comprehensive FastAPI backend for the Lance gaming cafe management system.

## Features

- **User Management**: Registration, authentication, profiles with JWT
- **PC Management**: Client PC tracking, groups, remote control
- **Session Management**: User sessions, time tracking, billing
- **Wallet System**: User wallets, transactions, balance management
- **Game Library**: Game catalog, installations, play tracking
- **Real-time Features**: WebSocket connections for live updates
- **Payment Integration**: Stripe and Razorpay support
- **Social Authentication**: Google, Discord, Twitter OAuth
- **Admin Dashboard**: Comprehensive admin controls
- **Booking System**: PC reservations and scheduling
- **Support System**: Tickets, chat, announcements
- **Membership Tiers**: User groups with discounts
- **Offers & Coupons**: Promotional system
- **Leaderboards**: Gaming statistics and rankings

## Tech Stack

- **Framework**: FastAPI
- **Database**: SQLAlchemy with PostgreSQL (SQLite for development)
- **Authentication**: JWT tokens
- **WebSockets**: For real-time communication
- **Task Queue**: Redis (optional)
- **Email**: SMTP support
- **File Storage**: Local filesystem
- **Deployment**: Gunicorn + Uvicorn workers

## Prerequisites

- Python 3.10+
- Redis (optional, for OTP and caching)
- PostgreSQL (recommended for production)
- SMTP server (for emails)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/your-username/lance-backend.git
cd lance-backend
```

2. Create virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment:
```bash
cp env.example .env
# Edit .env with your configuration
```

5. Run the application:
```bash
python main.py
```

The API will be available at `http://localhost:8000`

## Configuration

Key environment variables (see `env.example` for full list):

- `DATABASE_URL`: Database connection string
- `JWT_SECRET`: Secret key for JWT tokens
- `SECRET_KEY`: Application secret key
- `APP_BASE_URL`: Base URL for the application
- `SMTP_*`: Email configuration
- `STRIPE_*`: Stripe payment configuration
- `RAZORPAY_*`: Razorpay payment configuration
- `GOOGLE_CLIENT_*`: Google OAuth credentials
- `REDIS_URL`: Redis connection (optional)

## API Documentation

Once running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Project Structure

```
backend/
├── app/
│   ├── api/
│   │   └── endpoints/      # API route handlers
│   ├── crud/               # Database operations
│   ├── models.py           # SQLAlchemy models
│   ├── schemas.py          # Pydantic schemas
│   ├── database.py         # Database configuration
│   ├── utils/              # Utility functions
│   └── ws/                 # WebSocket handlers
├── scripts/                # Utility scripts
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── env.example            # Environment variables template
└── README.md              # This file
```

## Development

### Running Tests
```bash
pytest
```

### Code Formatting
```bash
black .
isort .
```

### Database Migrations

The application automatically creates tables on startup. For production, consider using Alembic for migrations.

### Adding New Endpoints

1. Create endpoint file in `app/api/endpoints/`
2. Define schemas in `app/schemas.py`
3. Add CRUD operations in `app/crud/`
4. Include router in `app/main.py`

## Deployment

See `DEPLOYMENT.md` for detailed deployment instructions. Quick overview:

1. Set up Ubuntu 22.04 server
2. Install dependencies (Python, PostgreSQL, Redis, Nginx)
3. Clone repository
4. Configure environment variables
5. Set up systemd service
6. Configure Nginx reverse proxy
7. Install SSL certificate

## API Endpoints

Major endpoint categories:

- `/api/auth/*` - Authentication and registration
- `/api/user/*` - User management
- `/api/pc/*` - PC management
- `/api/session/*` - Session management
- `/api/game/*` - Game library
- `/api/wallet/*` - Wallet operations
- `/api/payment/*` - Payment processing
- `/api/booking/*` - Booking system
- `/api/admin/*` - Admin operations
- `/ws/*` - WebSocket connections

## Security

- JWT-based authentication
- Password hashing with bcrypt
- CORS protection
- Rate limiting on sensitive endpoints
- SQL injection protection via SQLAlchemy
- Environment-based secrets

## Monitoring

- Health check endpoint: `/health`
- Structured logging
- Error tracking
- Performance metrics

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## License

This project is proprietary software. All rights reserved.

## Support

For issues and questions:
- Create an issue in the repository
- Contact: support@primustech.in

## Acknowledgments

- FastAPI for the amazing framework
- SQLAlchemy for database ORM
- All contributors and testers