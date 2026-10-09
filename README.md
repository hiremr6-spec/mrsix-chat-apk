# MR.SIX × Mister 6 Chat APK

Production-grade Flutter chat application powered by Mister 6 with full unrestricted access capabilities. Deploy to Android, iOS, or web with Docker-backed API infrastructure.

## Features

- **Real-time Chat UI**: Material 3 Flutter interface with smooth animations
- **Mister 6 Backend**: FastAPI service with unrestricted data inspection capabilities
- **Docker Infrastructure**: Full containerized deployment stack
- **Horizontal Scaling**: Load-balancer ready architecture
- **Environment-based Config**: 12-factor app principles
- **CORS Enabled**: Full cross-origin support
- **Health Checks**: Built-in liveness and readiness probes
- **Production Logging**: Structured JSON logging

## Architecture

```
Flutter APK (iOS/Android/Web)
        ↓
    HTTP/REST
        ↓
    Nginx Load Balancer
        ↓
    FastAPI Backend (Mister 6)
        ↓
    PostgreSQL / Redis Cache
```

## Quick Start (Local Development)

### Prerequisites

- Flutter 3.5+
- Docker 20.10+
- Docker Compose 2.0+
- Python 3.11+
- Android Studio (for APK building)

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/hiremr6-spec/mrsix-chat-apk.git
   cd mrsix-chat-apk
   ```

2. Configure environment:
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

3. Start Docker infrastructure:
   ```bash
   docker compose -f docker-compose.yml up --build -d
   ```

4. Run Flutter app:
   ```bash
   cd app
   flutter pub get
   flutter run -d emulator-5554  # or your device
   ```

5. Verify backend health:
   ```bash
   curl http://localhost:8000/health
   ```

## Production Deployment

### Docker Stack

```bash
# Build production images
docker compose -f docker-compose.prod.yml build

# Deploy with replicas
docker compose -f docker-compose.prod.yml up -d --scale backend=3

# Check status
docker compose ps
```

### Kubernetes Deployment

```bash
# Apply all manifests
kubectl apply -f k8s/

# Scale backend
kubectl scale deployment/mrsix-backend --replicas=3

# Check pods
kubectl get pods -l app=mrsix-backend
```

### APK Build & Release

```bash
# Build signed APK
cd app
flutter build apk --release

# Output: build/app/outputs/flutter-app.apk

# Build App Bundle (for Google Play)
flutter build appbundle --release
```

## API Endpoints

### Health Check
```
GET /health
Response: { status, brand, engine, access_policy, capabilities }
```

### Chat Endpoint
```
POST /api/chat
Request: { "message": "Ask Mister 6 anything" }
Response: { "reply", "source", "brand", "access_level" }
```

### Mister 6 Status
```
GET /api/mister6/status
Response: { name, status, access_policy, capabilities }
```

## Environment Variables

```env
APP_NAME=MR.SIX
APP_TAGLINE="MR.SIX powered by Mister 6"
MISTER_6_API_KEY=<your-api-key>
BACKEND_PORT=8000
FRONTEND_PORT=8080
MISTER_6_ACCESS_POLICY=unrestricted
MISTER_6_ALLOW_FILE_INSPECTION=true
MISTER_6_ALLOW_SYSTEM_CHECKS=true
MISTER_6_ALLOW_DATA_ACCESS=true
DATABASE_URL=postgresql://user:pass@db:5432/mrsix
REDIS_URL=redis://cache:6379
LOG_LEVEL=INFO
CORS_ORIGINS=*
```

## Project Structure

```
mrsix-chat-apk/
├── app/                       # Flutter frontend
│   ├── lib/
│   │   ├── main.dart         # App entry point
│   │   ├── screens/          # UI screens
│   │   ├── models/           # Data models
│   │   └── services/         # API clients
│   ├── pubspec.yaml
│   └── build/                # Build outputs
├── backend/                   # FastAPI service
│   ├── app/
│   │   ├── main.py          # API routes
│   │   ├── models.py        # Pydantic models
│   │   ├── services/        # Business logic
│   │   └── db/              # Database
│   ├── requirements.txt
│   └── Dockerfile
├── k8s/                       # Kubernetes manifests
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── configmap.yaml
│   └── ingress.yaml
├── nginx/                     # Load balancer config
│   └── nginx.conf
├── docker-compose.yml         # Local dev stack
├── docker-compose.prod.yml    # Production stack
├── .env.example               # Environment template
└── README.md                  # This file
```

## CI/CD Pipeline

GitHub Actions workflows:
- `test.yml`: Run Flutter tests on PR
- `build-apk.yml`: Build APK on release tag
- `deploy.yml`: Deploy to production on main branch

## Monitoring & Logging

- **Prometheus**: Metrics at `/metrics`
- **Loki**: Centralized logging
- **Grafana**: Dashboards and alerts
- **Jaeger**: Distributed tracing

## Security

- ✅ Secrets managed via environment variables
- ✅ HTTPS enforced in production
- ✅ Rate limiting enabled
- ✅ CORS properly configured
- ✅ SQL injection prevention (ORM-based)
- ✅ Input validation on all endpoints

## Testing

```bash
# Run Flutter tests
cd app
flutter test

# Run backend tests
cd backend
pytest

# Integration tests
cd tests
pytest integration/
```

## Troubleshooting

### Backend not connecting
```bash
# Check if Docker container is running
docker compose ps

# View logs
docker compose logs backend

# Restart service
docker compose restart backend
```

### APK build fails
```bash
# Clean build
cd app
flutter clean
flutter pub get
flutter build apk --release
```

### Port already in use
```bash
# Change port in .env
BACKEND_PORT=9000

# Rebuild containers
docker compose down
docker compose up --build
```

## Performance Tuning

- Backend replicas: Scale horizontally via Docker Compose or Kubernetes
- Database: Use connection pooling (pgBouncer)
- Cache: Redis for frequently accessed data
- CDN: CloudFront for static assets
- APK Size: Use ProGuard/R8 for code shrinking

## Support & Contribution

For issues, feature requests, or contributions, open a GitHub issue or pull request.

## License

MIT License - See LICENSE file

## Deployment Checklist

- [ ] Environment variables set in `.env`
- [ ] Database migrations run
- [ ] Backend health check passing
- [ ] APK signed and keystore backed up
- [ ] API endpoints tested with Postman/cURL
- [ ] Monitoring and logging configured
- [ ] Load balancer health checks enabled
- [ ] SSL/TLS certificates valid
- [ ] Backup strategy in place
- [ ] Runbook for common issues created
