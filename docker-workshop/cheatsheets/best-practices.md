# 🏆 Docker - Bonnes Pratiques

## 🐳 Dockerfile - Optimisations

### 1. Images de base légères
```dockerfile
# ❌ Éviter les images complètes
FROM ubuntu:latest

# ✅ Préférer les images slim/alpine
FROM python:3.11-slim
FROM node:18-alpine
FROM golang:1.21-alpine
```

### 2. Ordre des layers pour le cache
```dockerfile
# ✅ Bon ordre (dependencies avant code)
FROM python:3.11-slim
WORKDIR /app

# Copier requirements en premier (change moins souvent)
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copier le code ensuite (change plus souvent)
COPY . .
```

### 3. Multi-stage builds
```dockerfile
# Stage 1: Build
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

# Stage 2: Production
FROM node:18-alpine
WORKDIR /app
COPY --from=builder /app/node_modules ./node_modules
COPY . .
USER node
CMD ["node", "server.js"]
```

### 4. Minimiser les layers
```dockerfile
# ❌ Trop de layers
RUN apt-get update
RUN apt-get install -y curl
RUN apt-get install -y wget
RUN apt-get clean

# ✅ Combiner les commandes
RUN apt-get update && \
    apt-get install -y curl wget && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
```

### 5. Utilisateur non-root
```dockerfile
# Créer un utilisateur dédié
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Copier les fichiers
COPY --chown=appuser:appuser . /app

# Changer d'utilisateur
USER appuser
```

---

## 🔒 Sécurité

### 1. Images officielles et vérifiées
```bash
# ✅ Utiliser les images officielles
docker pull python:3.11-slim
docker pull nginx:alpine
docker pull postgres:15

# ✅ Vérifier les signatures (si disponible)
export DOCKER_CONTENT_TRUST=1
docker pull alpine:latest
```

### 2. Scanner les vulnérabilités
```bash
# Avec Docker Scout (intégré)
docker scout cves mon-image:latest

# Avec Trivy
trivy image mon-image:latest

# Avec Snyk
snyk container test mon-image:latest
```

### 3. Secrets et credentials
```dockerfile
# ❌ Ne JAMAIS faire ça
ENV API_KEY=secret123
RUN echo "password123" > /app/config

# ✅ Utiliser des variables d'environnement
ENV API_KEY=""
# Puis : docker run -e API_KEY=secret123 mon-image
```

```bash
# ✅ Docker secrets (Swarm mode)
echo "mon_secret" | docker secret create api_key -
docker service create --secret api_key mon-service
```

### 4. .dockerignore essentiel
```dockerignore
# Fichiers sensibles
.env
.env.local
secrets/
*.key
*.pem

# Fichiers temporaires
.git/
.gitignore
node_modules/
__pycache__/
.pytest_cache/

# Documentation
README.md
docs/
*.md
```

---

## ⚡ Performance

### 1. Optimisation des images
```bash
# Voir la taille des layers
docker history mon-image:latest

# Analyser l'efficacité
docker run --rm -it wagoodman/dive mon-image:latest
```

### 2. Cache de build
```bash
# Utiliser BuildKit (plus rapide)
export DOCKER_BUILDKIT=1
docker build -t mon-app .

# Cache externe pour CI/CD
docker buildx build --cache-from type=registry,ref=myregistry/cache \
                   --cache-to type=registry,ref=myregistry/cache \
                   -t mon-app .
```

### 3. Ressources limitées
```bash
# Limiter CPU et mémoire
docker run --memory=512m --cpus=1.0 mon-app

# Avec Docker Compose
services:
  web:
    image: mon-app
    deploy:
      resources:
        limits:
          memory: 512M
          cpus: '1.0'
```

### 4. Health checks optimisés
```dockerfile
# Health check léger
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8080/health || exit 1

# Ou avec un script custom
COPY healthcheck.sh /usr/local/bin/
HEALTHCHECK --interval=30s CMD /usr/local/bin/healthcheck.sh
```

---

## 🏗️ Architecture et Organisation

### 1. Structure de projet
```
project/
├── docker/
│   ├── Dockerfile.dev
│   ├── Dockerfile.prod
│   └── docker-compose.yml
├── src/
├── tests/
├── .dockerignore
├── .env.example
└── docker-compose.override.yml
```

### 2. Environnements multiples
```yaml
# docker-compose.yml (base)
version: '3.8'
services:
  web:
    build: .
    environment:
      - NODE_ENV=production

# docker-compose.override.yml (dev automatique)
version: '3.8'
services:
  web:
    build:
      context: .
      dockerfile: Dockerfile.dev
    volumes:
      - .:/app
    environment:
      - NODE_ENV=development
      - DEBUG=true
```

### 3. Gestion des configurations
```dockerfile
# ✅ Configuration externalisée
ENV CONFIG_FILE=/app/config/app.conf
VOLUME ["/app/config"]

# ✅ Patterns de configuration
ENV DATABASE_URL=""
ENV REDIS_URL=""
ENV LOG_LEVEL=info
```

---

## 🔄 CI/CD et Déploiement

### 1. Pipeline de build
```yaml
# .github/workflows/docker.yml
name: Docker Build
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v2
        
      - name: Build and push
        uses: docker/build-push-action@v4
        with:
          context: .
          push: true
          tags: myregistry/myapp:${{ github.sha }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

### 2. Tags et versioning
```bash
# Stratégie de tags
docker tag mon-app:latest mon-app:v1.2.3
docker tag mon-app:latest mon-app:v1.2
docker tag mon-app:latest mon-app:v1
docker tag mon-app:latest mon-app:latest

# Tags avec métadonnées
docker build \
  --label version=1.2.3 \
  --label commit=$(git rev-parse HEAD) \
  --label build-date=$(date -u +%Y-%m-%dT%H:%M:%SZ) \
  -t mon-app:v1.2.3 .
```

### 3. Rolling updates
```yaml
# Docker Compose avec rolling update
version: '3.8'
services:
  web:
    image: mon-app:v1.2.3
    deploy:
      replicas: 3
      update_config:
        parallelism: 1
        delay: 10s
        order: start-first
```

---

## 📊 Monitoring et Logging

### 1. Logs structurés
```dockerfile
# Configuration des logs
ENV LOG_FORMAT=json
ENV LOG_LEVEL=info

# Driver de logs
docker run --log-driver=fluentd --log-opt fluentd-address=localhost:24224 mon-app
```

### 2. Métriques et monitoring
```yaml
# docker-compose avec monitoring
version: '3.8'
services:
  app:
    image: mon-app
    expose:
      - "8080"
    labels:
      - "prometheus.io/scrape=true"
      - "prometheus.io/port=8080"
      - "prometheus.io/path=/metrics"
```

### 3. Health checks avancés
```bash
#!/bin/bash
# healthcheck.sh

# Vérifier que l'app répond
if ! curl -f http://localhost:8080/health 2>/dev/null; then
  exit 1
fi

# Vérifier la connectivité à la DB
if ! nc -z database 5432; then
  exit 1
fi

# Vérifier l'utilisation mémoire
MEMORY_USAGE=$(free | grep Mem | awk '{printf "%.0f", $3/$2 * 100.0}')
if [ $MEMORY_USAGE -gt 90 ]; then
  exit 1
fi

exit 0
```

---

## 🎯 Cas d'Usage Spécifiques

### 1. Applications Web
```dockerfile
FROM node:18-alpine

# Installer dumb-init pour gérer les signaux
RUN apk add --no-cache dumb-init

# Créer utilisateur
RUN addgroup -g 1001 -S nodejs
RUN adduser -S nextjs -u 1001

# Copier et installer les dépendances
COPY --chown=nextjs:nodejs package*.json ./
RUN npm ci --only=production && npm cache clean --force

# Copier l'application
COPY --chown=nextjs:nodejs . .

USER nextjs
EXPOSE 3000

# Utiliser dumb-init comme PID 1
ENTRYPOINT ["dumb-init", "--"]
CMD ["node", "server.js"]
```

### 2. Applications de données
```dockerfile
FROM python:3.11-slim

# Installer les dépendances système nécessaires
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Créer des répertoires avec permissions
RUN mkdir -p /app/data /app/logs
RUN useradd -m -u 1001 datauser
RUN chown -R datauser:datauser /app

USER datauser
WORKDIR /app

# Volume pour la persistance
VOLUME ["/app/data"]

CMD ["python", "process_data.py"]
```

---

## 📝 Checklist finale

### Avant la production :
- [ ] Image de base officielle et à jour
- [ ] Scan de sécurité passé
- [ ] Utilisateur non-root
- [ ] Health check configuré
- [ ] Logs structurés
- [ ] Variables d'environnement pour la config
- [ ] .dockerignore optimisé
- [ ] Tags de version appropriés
- [ ] Documentation à jour
- [ ] Tests d'intégration passés

### Monitoring en production :
- [ ] Métriques collectées
- [ ] Logs centralisés
- [ ] Alertes configurées
- [ ] Backup des volumes
- [ ] Politique de retention des images
- [ ] Plans de rollback testés

---

**💡 Rappel :** Les bonnes pratiques évoluent. Restez à jour avec la [documentation officielle Docker](https://docs.docker.com/develop/dev-best-practices/) !