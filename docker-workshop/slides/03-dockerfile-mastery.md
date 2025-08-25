# 🐳 Workshop Docker
## Dockerfile - Maîtrise Complète

---

## 🎯 Objectifs

- Comprendre chaque instruction Dockerfile
- Appliquer les bonnes pratiques
- Optimiser les builds et les images
- Créer des images production-ready

---

## 📋 Anatomie d'un Dockerfile

```dockerfile
# Commentaire
FROM python:3.11-slim          # Image de base
LABEL maintainer="vous@email.com"  # Métadonnées
ENV APP_ENV=production         # Variables d'environnement
WORKDIR /app                   # Répertoire de travail
COPY requirements.txt .        # Copier fichiers
RUN pip install -r requirements.txt  # Exécuter commandes
COPY . .                       # Copier le reste
EXPOSE 5000                    # Port exposé
CMD ["python", "app.py"]       # Commande par défaut
```

---

## 🏗️ Instructions Fondamentales

### FROM - Image de base
```dockerfile
# Image officielle
FROM python:3.11-slim

# Version spécifique (recommandé pour prod)
FROM python:3.11.7-slim

# Multi-architecture
FROM --platform=linux/amd64 python:3.11-slim

# Multi-stage (on y reviendra)
FROM python:3.11-slim AS builder
```

### WORKDIR - Répertoire de travail
```dockerfile
# ❌ Éviter
RUN cd /app

# ✅ Utiliser WORKDIR
WORKDIR /app
RUN ls -la  # Sera exécuté dans /app
```

---

## 📁 Gestion des Fichiers

### COPY vs ADD
```dockerfile
# ✅ COPY pour la plupart des cas
COPY requirements.txt .
COPY src/ ./src/

# ✅ ADD pour cas spéciaux (URL, archives)
ADD https://example.com/file.tar.gz /tmp/
ADD archive.tar.gz /app/  # Auto-extraction
```

### Ordre optimal pour le cache
```dockerfile
# ✅ Bon ordre (dependencies d'abord)
FROM python:3.11-slim
WORKDIR /app

# 1. Copier requirements (change rarement)
COPY requirements.txt .
RUN pip install -r requirements.txt

# 2. Copier le code (change souvent)
COPY . .
```

---

## ⚙️ Exécution de Commandes

### RUN - Pendant le build
```dockerfile
# ❌ Multiple RUN = multiple layers
RUN apt-get update
RUN apt-get install -y curl
RUN apt-get clean

# ✅ Combiner en une seule layer
RUN apt-get update && \
    apt-get install -y curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
```

### CMD vs ENTRYPOINT
```dockerfile
# CMD : Commande par défaut (peut être overridée)
CMD ["python", "app.py"]
# docker run mon-image bash  # Override CMD

# ENTRYPOINT : Point d'entrée fixe
ENTRYPOINT ["python", "app.py"]
# docker run mon-image --verbose  # Ajoute des arguments

# Combinaison
ENTRYPOINT ["python", "app.py"]
CMD ["--port", "5000"]  # Arguments par défaut
```

---

## 🔧 Variables et Configuration

### ENV vs ARG
```dockerfile
# ARG : Variables de build seulement
ARG PYTHON_VERSION=3.11
FROM python:${PYTHON_VERSION}-slim

# ENV : Variables runtime (disponibles dans le conteneur)
ENV APP_ENV=production
ENV DEBUG=false
ENV PORT=5000

# Utilisation
RUN echo "Building for environment: $APP_ENV"
```

### Exemple pratique
```dockerfile
FROM python:3.11-slim

# Build args
ARG APP_VERSION=1.0.0
ARG BUILD_DATE

# Runtime env
ENV APP_VERSION=${APP_VERSION}
ENV BUILD_DATE=${BUILD_DATE}
ENV PYTHONUNBUFFERED=1

LABEL version=${APP_VERSION}
LABEL build-date=${BUILD_DATE}

WORKDIR /app
COPY . .

CMD ["python", "app.py"]
```

---

## 🛡️ Sécurité et Permissions

### Utilisateur non-root
```dockerfile
# Créer un utilisateur dédié
RUN groupadd -r appuser && \
    useradd -r -g appuser appuser

# Créer les répertoires avec bonnes permissions
RUN mkdir -p /app /app/logs && \
    chown -R appuser:appuser /app

# Copier les fichiers avec le bon owner
COPY --chown=appuser:appuser . /app

# Changer d'utilisateur
USER appuser

# Maintenant toutes les commandes s'exécutent en tant qu'appuser
```

### Gestion des secrets
```dockerfile
# ❌ JAMAIS ça !
ENV API_KEY=secret123
COPY secrets.txt /app/

# ✅ Variables d'environnement au runtime
ENV API_KEY=""
# docker run -e API_KEY=secret123 mon-image

# ✅ Secrets Docker (Swarm)
# docker secret create api_key secrets.txt
```

---

## 🚀 Optimisations Avancées

### Multi-stage builds
```dockerfile
# Stage 1: Build
FROM node:16-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

# Stage 2: Production
FROM node:16-alpine AS production
WORKDIR /app

# Copier seulement les node_modules du builder
COPY --from=builder /app/node_modules ./node_modules
COPY . .

USER node
EXPOSE 3000
CMD ["node", "server.js"]
```

### Cache mount (BuildKit)
```dockerfile
# syntax=docker/dockerfile:1
FROM python:3.11-slim

WORKDIR /app

# Cache pip
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt

# Cache apt
RUN --mount=type=cache,target=/var/cache/apt \
    apt-get update && \
    apt-get install -y curl
```

---

## 📊 Exemple Complet : API Flask Optimisée

```dockerfile
# syntax=docker/dockerfile:1

# Build arguments
ARG PYTHON_VERSION=3.11
ARG APP_VERSION=1.0.0

# Stage 1: Dependencies
FROM python:${PYTHON_VERSION}-slim AS dependencies

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --no-deps -r requirements.txt

# Stage 2: Production
FROM python:${PYTHON_VERSION}-slim AS production

# Metadata
LABEL maintainer="workshop@docker.com"
LABEL version=${APP_VERSION}
LABEL description="Flask API for Docker Workshop"

# Runtime environment
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV APP_VERSION=${APP_VERSION}
ENV PORT=5000

# Create app user
RUN groupadd -r appuser && \
    useradd -r -g appuser -d /app -s /bin/bash appuser

# Create directories
RUN mkdir -p /app /app/logs && \
    chown -R appuser:appuser /app

# Copy dependencies from previous stage
COPY --from=dependencies /usr/local/lib/python*/site-packages /usr/local/lib/python*/site-packages
COPY --from=dependencies /usr/local/bin /usr/local/bin

# Switch to app directory and user
WORKDIR /app
USER appuser

# Copy application code
COPY --chown=appuser:appuser . .

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:5000/health')" || exit 1

# Expose port
EXPOSE 5000

# Default command
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "app:app"]
```

---

## 🧪 Exercice Pratique : Node.js App

### Créer l'application
```javascript
// app.js
const express = require('express');
const app = express();
const port = process.env.PORT || 3000;

app.get('/', (req, res) => {
  res.json({
    message: '🐳 Hello from Docker!',
    version: process.env.APP_VERSION || '1.0.0',
    environment: process.env.NODE_ENV || 'development',
    timestamp: new Date().toISOString()
  });
});

app.get('/health', (req, res) => {
  res.json({ status: 'healthy' });
});

app.listen(port, '0.0.0.0', () => {
  console.log(`App listening on port ${port}`);
});
```

```json
{
  "name": "docker-workshop-app",
  "version": "1.0.0",
  "scripts": {
    "start": "node app.js"
  },
  "dependencies": {
    "express": "^4.18.0"
  }
}
```

### Votre mission : Créer le Dockerfile optimal
```dockerfile
# À vous de jouer !
# Critères :
# ✅ Image de base Alpine
# ✅ Multi-stage build
# ✅ Utilisateur non-root
# ✅ Cache optimisé
# ✅ Health check
# ✅ Variables d'environnement
```

---

## 🎯 Solution de l'Exercice

```dockerfile
# syntax=docker/dockerfile:1

# Stage 1: Dependencies
FROM node:18-alpine AS dependencies

WORKDIR /app
COPY package*.json ./
RUN --mount=type=cache,target=/root/.npm \
    npm ci --only=production

# Stage 2: Production
FROM node:18-alpine AS production

# Install dumb-init for proper signal handling
RUN apk add --no-cache dumb-init

# Create app user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nextjs -u 1001

# Create app directory
RUN mkdir -p /app && chown -R nextjs:nodejs /app
WORKDIR /app

# Copy dependencies
COPY --from=dependencies --chown=nextjs:nodejs /app/node_modules ./node_modules

# Copy app source
COPY --chown=nextjs:nodejs . .

# Switch to non-root user
USER nextjs

# Environment
ENV NODE_ENV=production
ENV PORT=3000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:3000/health || exit 1

# Expose port
EXPOSE 3000

# Use dumb-init to handle signals properly
ENTRYPOINT ["dumb-init", "--"]
CMD ["node", "app.js"]
```

---

## 📈 Optimisation et Debug

### Analyser la taille des images
```bash
# Voir l'historique des layers
docker history mon-image:latest

# Analyser avec dive
docker run --rm -it \
    -v /var/run/docker.sock:/var/run/docker.sock \
    wagoodman/dive:latest mon-image:latest
```

### Build avec BuildKit
```bash
# Activer BuildKit
export DOCKER_BUILDKIT=1

# Build avec cache
docker build --cache-from mon-image:cache .

# Build avec secrets
echo "mysecret" | docker build --secret id=api_key,src=- .
```

---

## ✅ Checklist Dockerfile Production

### Sécurité
- [ ] Utilisateur non-root
- [ ] Image de base officielle et à jour
- [ ] Pas de secrets en dur
- [ ] Scan de vulnérabilités

### Performance
- [ ] Image de base légère (slim/alpine)
- [ ] Multi-stage si applicable
- [ ] Ordre des layers optimisé
- [ ] .dockerignore configuré

### Fiabilité
- [ ] Health check configuré
- [ ] Gestion des signaux (dumb-init)
- [ ] Variables d'environnement
- [ ] Logs structurés

---

## 🚀 Prochaine Étape

### Ce qui nous attend :
- **Docker Compose** : Orchestrer plusieurs conteneurs
- **Applications complètes** avec base de données
- **Réseaux et volumes** avancés

---

## 💡 Points Clés

- 🏗️ **Ordre des layers = optimisation du cache**
- 🛡️ **Sécurité dès la construction**
- ⚡ **Multi-stage = images légères**
- 🔍 **Health checks = monitoring intégré**