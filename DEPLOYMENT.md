# MR.SIX × Mister 6 - Production Deployment Guide

## Prerequisites

- Docker 20.10+
- Docker Compose 2.0+
- Kubernetes 1.24+ (for K8s deployment)
- kubectl configured
- Flutter 3.5+ (for APK builds)
- Android SDK (for APK builds)

## Local Development

### 1. Environment Setup

```bash
cp .env.example .env
# Edit .env with your settings
```

### 2. Start Services

```bash
docker compose up --build -d
```

### 3. Verify Health

```bash
curl http://localhost:8000/health
curl http://localhost:8000/api/mister6/status
```

## Docker Stack Deployment

### Production Setup

```bash
# Create production env
cp .env.example .env.prod
# Edit .env.prod with production credentials

# Build production images
docker compose -f docker-compose.prod.yml build

# Start with 3 replicas
docker compose -f docker-compose.prod.yml up -d --scale backend=3

# Verify
docker compose ps
```

### Monitoring

```bash
# View logs
docker compose logs -f backend

# Check container health
docker compose ps

# Scale backend
docker compose -f docker-compose.prod.yml up -d --scale backend=5
```

## Kubernetes Deployment

### 1. Create Namespace

```bash
kubectl apply -f k8s/namespace.yaml
```

### 2. Create Secrets

```bash
kubectl create secret generic mrsix-secrets \
  --from-literal=DATABASE_URL="postgresql://..." \
  --from-literal=REDIS_PASSWORD="secure_password" \
  --from-literal=MISTER_6_API_KEY="your_api_key" \
  -n mrsix
```

### 3. Deploy Services

```bash
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

### 4. Monitor Deployment

```bash
# Check pods
kubectl get pods -n mrsix

# Check logs
kubectl logs -f deployment/mrsix-backend -n mrsix

# Port forward
kubectl port-forward svc/mrsix-backend 8000:8000 -n mrsix
```

### 5. Scale Backend

```bash
kubectl scale deployment mrsix-backend --replicas=5 -n mrsix
```

## APK Build & Release

### Android APK

```bash
cd app

# Debug APK
flutter build apk --debug
# Output: build/app/outputs/flutter-app-debug.apk

# Release APK (unsigned)
flutter build apk --release
# Output: build/app/outputs/flutter-app-release.apk

# Signed Release APK
flutter build apk --release \
  --split-debug-info=split-debug-symbols/
```

### Google Play Store

```bash
# Build App Bundle
flutter build appbundle --release
# Output: build/app/outputs/bundle/release/app-release.aab

# Upload to Play Console via web or CLI
```

### iOS (macOS only)

```bash
cd app
flutter build ios --release

# Build IPA
xcodebuild -workspace ios/Runner.xcworkspace \
  -scheme Runner \
  -configuration Release \
  -derivedDataPath build/ios_build \
  -arch arm64 \
  build-for-testing
```

## SSL/TLS Configuration

### Self-Signed Certificates (Dev)

```bash
openssl req -x509 -newkey rsa:4096 -keyout nginx/ssl/private.key \
  -out nginx/ssl/certificate.crt -days 365 -nodes
```

### Let's Encrypt (Production)

```bash
# Using Certbot
certbot certonly --standalone -d yourdomain.com

# Copy certificates to nginx/ssl/
cp /etc/letsencrypt/live/yourdomain.com/fullchain.pem nginx/ssl/certificate.crt
cp /etc/letsencrypt/live/yourdomain.com/privkey.pem nginx/ssl/private.key
```

## Database Migrations

```bash
# Run migrations
cd backend
alembic upgrade head

# Create new migration
alembic revision --autogenerate -m "description"
```

## Backup & Recovery

### Database Backup

```bash
# Full backup
docker compose exec db pg_dump -U mrsix mrsix_db > backup.sql

# Compressed backup
docker compose exec db pg_dump -U mrsix mrsix_db | gzip > backup.sql.gz

# Restore
docker compose exec -T db psql -U mrsix mrsix_db < backup.sql
```

### Redis Backup

```bash
# Snapshot (RDB)
redis-cli --rdb /backup/dump.rdb

# AOF rewrite
redis-cli BGREWRITEAOF
```

## Health Checks

### API Health

```bash
curl -X GET http://localhost:8000/health
```

### Mister 6 Status

```bash
curl -X GET http://localhost:8000/api/mister6/status
```

## Troubleshooting

### Backend not responding

```bash
# Check logs
docker compose logs backend | tail -100

# Check health
curl http://localhost:8000/health

# Restart
docker compose restart backend
```

### Database connection issues

```bash
# Check database
docker compose exec db psql -U mrsix -c "SELECT version();"

# Check connections
docker compose exec db psql -U mrsix -c \
  "SELECT * FROM pg_stat_activity;"
```

### Memory leaks

```bash
# Monitor memory
docker stats mrsix-backend

# Restart container
docker compose restart backend

# Scale to new replicas
docker compose up -d --scale backend=4
```

## Performance Optimization

### Database

```sql
-- Create indexes
CREATE INDEX idx_messages_user_id ON messages(user_id);
CREATE INDEX idx_messages_created_at ON messages(created_at);

-- Vacuum
VACUUM ANALYZE;
```

### Caching

```python
# Redis cache strategy
from redis import Redis
redis = Redis.from_url(os.getenv('REDIS_URL'))
redis.setex('key', 3600, 'value')  # Cache for 1 hour
```

## Security

### Secrets Management

```bash
# Rotate API keys
kubectl delete secret mrsix-secrets -n mrsix
kubectl create secret generic mrsix-secrets \
  --from-literal=MISTER_6_API_KEY="new_key" \
  -n mrsix

# Restart pods to pick up new secrets
kubectl rollout restart deployment/mrsix-backend -n mrsix
```

### Network Policies

```yaml
# Restrict traffic
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: mrsix-network-policy
  namespace: mrsix
spec:
  podSelector:
    matchLabels:
      app: mrsix-backend
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: nginx
  egress:
  - to:
    - podSelector:
        matchLabels:
          app: database
```

## Monitoring & Alerts

### Prometheus Metrics

```
http://localhost:9090/metrics
```

### Grafana Dashboards

```
http://localhost:3000
Default: admin/admin
```

### Log Aggregation (Loki)

```
http://localhost:3100/api/prom/label/job/values
```

## CI/CD Integration

### GitHub Actions Workflow

See `.github/workflows/` for:
- `test.yml`: Run tests on PR
- `build-apk.yml`: Build APK on tag
- `deploy.yml`: Auto-deploy to production

## Rollback Strategy

```bash
# Docker Compose
git checkout previous_version
docker compose -f docker-compose.prod.yml down
docker compose -f docker-compose.prod.yml up --build -d

# Kubernetes
kubectl rollout undo deployment/mrsix-backend -n mrsix
kubectl rollout history deployment/mrsix-backend -n mrsix
```

## Contact & Support

For deployment issues, check:
1. Logs: `docker compose logs` or `kubectl logs`
2. Health endpoints: `/health`, `/api/mister6/status`
3. Network connectivity: `curl`, `telnet`
4. Database: `psql`, `redis-cli`
