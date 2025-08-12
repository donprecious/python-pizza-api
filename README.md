# Usersnack Pizza Ordering System

A full-stack pizza ordering application built with FastAPI (backend) and React (frontend), containerized with Docker.

## 🏗️ Architecture

- **Backend**: FastAPI with PostgreSQL database
- **Frontend**: React with TypeScript and Vite
- **Database**: PostgreSQL 15
- **Containerization**: Docker & Docker Compose

## 📋 Prerequisites

- Docker and Docker Compose installed on your system
- Git (for cloning the repository)

For local development without Docker:
- Python 3.12+ with Poetry
- Node.js 20+ with npm
- PostgreSQL 15+

## 🚀 Quick Start with Docker Compose

### 1. Clone the Repository

```bash
git clone <repository-url>
cd usersnack
```

### 2. Environment Setup

Copy the example environment file and configure it:

```bash
cp .env.example .env
```

Edit the `.env` file with your preferred settings. The default values work for local development.

### 3. Run with Docker Compose

Start all services (frontend, backend, and database):

```bash
docker-compose up -d
```

This will:
- Build and start the backend API on `http://localhost:8000`
- Build and start the frontend on `http://localhost:3000`
- Start PostgreSQL database on `localhost:5432`

### 4. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

### 5. Stop the Services

```bash
docker-compose down
```

To remove volumes (database data):

```bash
docker-compose down -v
```

## 🛠️ Development Setup

### Running Services Individually

#### Backend Only

```bash
# Navigate to backend directory
cd backend

# Copy environment file
cp .env.example .env

# Install dependencies
poetry install

# Start PostgreSQL (using Docker)
docker run -d \
  --name usersnack-postgres \
  -e POSTGRES_USER=usersnack \
  -e POSTGRES_PASSWORD=password \
  -e POSTGRES_DB=usersnack_db \
  -p 5432:5432 \
  postgres:15-alpine

# Run database migrations
poetry run alembic upgrade head

# Seed the database
poetry run python scripts/seed.py

# Start the backend server
poetry run uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

#### Frontend Only

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend will be available at `http://localhost:5173` (Vite default port).

### Building for Production

#### Backend

```bash
cd backend
docker build -t usersnack-backend .
```

#### Frontend

```bash
cd frontend
docker build -t usersnack-frontend .
```

## 📁 Project Structure

```
usersnack/
├── backend/                 # FastAPI backend
│   ├── app/                # Application code
│   │   ├── api/           # API routes
│   │   ├── core/          # Core functionality
│   │   ├── db/            # Database models and repositories
│   │   ├── schemas/       # Pydantic schemas
│   │   └── services/      # Business logic
│   ├── migrations/         # Database migrations
│   ├── scripts/           # Utility scripts
│   ├── tests/             # Test suite
│   ├── Dockerfile         # Backend Docker configuration
│   ├── pyproject.toml     # Python dependencies
│   └── main.py            # Application entry point
├── frontend/               # React frontend
│   ├── src/               # Source code
│   │   ├── components/    # React components
│   │   ├── pages/         # Page components
│   │   ├── services/      # API services
│   │   └── types/         # TypeScript types
│   ├── public/            # Static assets
│   ├── Dockerfile         # Frontend Docker configuration
│   ├── nginx.conf         # Nginx configuration
│   └── package.json       # Node.js dependencies
├── docker-compose.yml      # Multi-service orchestration
├── .env.example           # Environment variables template
├── .gitignore             # Git ignore rules
└── README.md              # This file
```

## 🔧 Configuration

### Environment Variables

Key environment variables in `.env`:

| Variable | Description | Default |
|----------|-------------|---------|
| `DB_USER` | Database username | `usersnack` |
| `DB_PASSWORD` | Database password | `password` |
| `DB_NAME` | Database name | `usersnack_db` |
| `DB_HOST` | Database host | `localhost` |
| `DB_PORT` | Database port | `5432` |
| `API_CORS_ORIGINS` | Allowed CORS origins | `["http://localhost:3000"]` |

### Docker Compose Services

- **backend**: FastAPI application (port 8000)
- **frontend**: React application with Nginx (port 3000)
- **postgres**: PostgreSQL database (port 5432)

## 🧪 Testing

### Backend Tests

```bash
cd backend
poetry run pytest
```

### Frontend Tests

```bash
cd frontend
npm run test
```

## 📊 API Documentation

Once the backend is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🔍 Health Checks

Both services include health check endpoints:
- Backend: `GET /health`
- Frontend: `GET /health` (via Nginx)

## 🐛 Troubleshooting

### Common Issues

1. **Port conflicts**: Ensure ports 3000, 8000, and 5432 are available
2. **Database connection**: Check if PostgreSQL is running and accessible
3. **Environment variables**: Verify `.env` file exists and has correct values

### Logs

Docker Compose provides multiple ways to view and manage logs:

#### View Real-time Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f postgres

# Last 100 lines
docker-compose logs --tail=100 backend

# Logs from last hour
docker-compose logs --since=1h frontend
```

#### Log Files Location

Logs are automatically saved to the `./logs/` directory:

```
logs/
├── backend/        # Backend application logs
├── frontend/       # Nginx access and error logs
└── postgres/       # PostgreSQL logs
```

#### Log Configuration

Each service is configured with:
- **Log rotation**: Maximum 10MB per file
- **Log retention**: Keep 3 log files
- **Format**: JSON format for structured logging

#### Viewing Persistent Logs

```bash
# Backend logs
tail -f logs/backend/app.log

# Frontend access logs
tail -f logs/frontend/access.log

# Frontend error logs
tail -f logs/frontend/error.log

# PostgreSQL logs
tail -f logs/postgres/postgresql.log
```

#### Log Management Commands

```bash
# Clear all logs
docker-compose down && sudo rm -rf logs/*

# View logs by timestamp
docker-compose logs --since="2024-01-01T00:00:00" --until="2024-01-01T23:59:59"

# Export logs to file
docker-compose logs backend > backend_logs.txt
```

### Reset Database

```bash
docker-compose down -v
docker-compose up -d
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.