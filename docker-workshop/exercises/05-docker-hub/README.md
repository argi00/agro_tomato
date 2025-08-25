# 📦 Exercice 5 : Publication sur Docker Hub

## 🎯 Objectif
Apprendre à publier vos images Docker sur Docker Hub pour les partager avec le monde entier.

## 📋 Prérequis
- Compte Docker Hub : [hub.docker.com](https://hub.docker.com)
- Docker installé et fonctionnel
- Une image Docker prête à publier

## 🚀 Instructions

### Étape 1 : Préparation de l'image
```bash
# Utiliser l'image de l'exercice 3 ou créer une nouvelle
cd ../03-flask-simple

# Reconstruire l'image avec un tag approprié
docker build -t todo-api:latest .

# Vérifier l'image
docker images | grep todo-api
```

### Étape 2 : Connexion à Docker Hub
```bash
# Se connecter avec vos identifiants
docker login

# Vérifier la connexion
docker info | grep Username
```

### Étape 3 : Taguer l'image
```bash
# Format : docker tag image:tag username/repository:tag
docker tag todo-api:latest votre-username/todo-api:1.0.0
docker tag todo-api:latest votre-username/todo-api:latest

# Vérifier les tags
docker images | grep todo-api
```

### Étape 4 : Publier l'image
```bash
# Pousser les images
docker push votre-username/todo-api:1.0.0
docker push votre-username/todo-api:latest

# La première fois prend plus de temps (upload de tous les layers)
# Les fois suivantes sont plus rapides (layers en cache)
```

### Étape 5 : Vérifier la publication
```bash
# Voir sur Docker Hub
# https://hub.docker.com/r/votre-username/todo-api

# Tester le téléchargement
docker rmi votre-username/todo-api:latest
docker run -p 8080:5000 votre-username/todo-api:latest
```

## 🧪 Exercices Avancés

### Test 1 : Multi-architecture
```bash
# Construire pour plusieurs architectures
docker buildx create --use
docker buildx build --platform linux/amd64,linux/arm64 \
  -t votre-username/todo-api:multiarch \
  --push .
```

### Test 2 : Automated Builds avec GitHub
```bash
# 1. Connecter votre repo GitHub à Docker Hub
# 2. Configurer les builds automatiques
# 3. Pousser du code → image automatiquement buildée
```

### Test 3 : Tags sémantiques
```bash
# Stratégie de versioning
docker tag todo-api:latest votre-username/todo-api:v1.0.0
docker tag todo-api:latest votre-username/todo-api:v1.0
docker tag todo-api:latest votre-username/todo-api:v1
docker tag todo-api:latest votre-username/todo-api:latest

# Pousser tous les tags
docker push votre-username/todo-api --all-tags
```

## 📊 Bonnes Pratiques

### Documentation du Repository
```markdown
# README.md pour Docker Hub

# Todo API Docker Image

Simple Flask API for managing todos.

## Quick Start

```bash
docker run -p 8080:5000 votre-username/todo-api:latest
curl http://localhost:8080/todos
```

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| PORT | 5000 | API port |
| DEBUG | false | Debug mode |
| ENV | production | Environment |

## Versions

- `latest` - Latest stable release
- `v1.0.0` - Specific version
- `dev` - Development branch
```

### Labels pour métadonnées
```dockerfile
LABEL org.opencontainers.image.title="Todo API"
LABEL org.opencontainers.image.description="Simple Flask API for managing todos"
LABEL org.opencontainers.image.version="1.0.0"
LABEL org.opencontainers.image.authors="votre-nom"
LABEL org.opencontainers.image.source="https://github.com/votre-username/todo-api"
LABEL org.opencontainers.image.licenses="MIT"
```

## 🔒 Sécurité et Gestion

### Scanner les vulnérabilités
```bash
# Scanner avec Docker Scout
docker scout cves votre-username/todo-api:latest

# Voir les recommandations
docker scout recommendations votre-username/todo-api:latest
```

### Gestion des accès
```bash
# Créer un token d'accès personnel
# https://hub.docker.com/settings/security

# Utiliser le token au lieu du mot de passe
echo "votre-token" | docker login --username votre-username --password-stdin
```

### Repository privé
```bash
# Créer un repository privé sur Docker Hub
# Puis pousser l'image
docker tag todo-api:latest votre-username/private-app:latest
docker push votre-username/private-app:latest

# Télécharger (nécessite d'être connecté)
docker pull votre-username/private-app:latest
```

## 🤖 Automatisation CI/CD

### GitHub Actions
```yaml
# .github/workflows/docker.yml
name: Build and Push Docker Image

on:
  push:
    branches: [main]
    tags: ['v*']

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v2
        
      - name: Login to Docker Hub
        uses: docker/login-action@v2
        with:
          username: ${{ secrets.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}
          
      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v4
        with:
          images: votre-username/todo-api
          tags: |
            type=ref,event=branch
            type=ref,event=pr
            type=semver,pattern={{version}}
            type=semver,pattern={{major}}.{{minor}}
            
      - name: Build and push
        uses: docker/build-push-action@v4
        with:
          context: .
          platforms: linux/amd64,linux/arm64
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

### GitLab CI
```yaml
# .gitlab-ci.yml
stages:
  - build
  - push

variables:
  DOCKER_IMAGE: votre-username/todo-api

build:
  stage: build
  image: docker:latest
  services:
    - docker:dind
  script:
    - docker build -t $DOCKER_IMAGE:$CI_COMMIT_SHA .
    - docker tag $DOCKER_IMAGE:$CI_COMMIT_SHA $DOCKER_IMAGE:latest
    
push:
  stage: push
  image: docker:latest
  services:
    - docker:dind
  script:
    - echo $DOCKERHUB_TOKEN | docker login -u $DOCKERHUB_USERNAME --password-stdin
    - docker push $DOCKER_IMAGE:$CI_COMMIT_SHA
    - docker push $DOCKER_IMAGE:latest
  only:
    - main
```

## 📈 Monitoring et Analytics

### Métriques Docker Hub
- Nombre de pulls
- Étoiles et favoris  
- Builds automatiques
- Statistiques d'utilisation

### Notifications
```bash
# Webhook pour notifications
curl -X POST https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK \
  -H 'Content-type: application/json' \
  --data '{"text":"New Docker image pushed: todo-api:v1.0.0"}'
```

## ✅ Validation

Vous avez réussi si :
- [x] Votre image est visible sur hub.docker.com
- [x] L'image peut être téléchargée par d'autres
- [x] La documentation est claire
- [x] Les tags sont cohérents
- [x] L'image fonctionne après téléchargement

## 🧩 Défis Bonus

1. **Registry privé** : Héberger votre propre registry
2. **Multi-arch** : Support ARM64 et AMD64
3. **Signatures** : Signer vos images avec Cosign
4. **SBOM** : Générer un Software Bill of Materials

## 🎓 Ce que vous avez appris

- ✅ Publication d'images sur Docker Hub
- ✅ Stratégies de versioning et tagging
- ✅ Documentation et métadonnées
- ✅ Automatisation CI/CD
- ✅ Sécurité et gestion des accès

---

**Félicitations ! 🎉 Votre image Docker est maintenant disponible dans le monde entier !**

**Prochaine étape :** Intégration dans des environnements de production (Kubernetes, Cloud, etc.)