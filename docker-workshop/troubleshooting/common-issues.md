# 🚨 Docker - Problèmes Courants et Solutions

## 🔧 Problèmes d'Installation et Configuration

### 1. Docker ne démarre pas
```bash
# Symptôme
docker: Cannot connect to the Docker daemon. Is the docker daemon running?

# Solutions
# Sur Linux
sudo systemctl start docker
sudo systemctl enable docker

# Vérifier le status
sudo systemctl status docker

# Ajouter l'utilisateur au groupe docker
sudo usermod -aG docker $USER
newgrp docker  # ou redémarrer la session
```

### 2. Permissions refusées
```bash
# Symptôme
Got permission denied while trying to connect to the Docker daemon socket

# Solution
sudo chmod 666 /var/run/docker.sock
# Ou mieux, ajouter l'utilisateur au groupe docker (voir ci-dessus)
```

### 3. Espace disque insuffisant
```bash
# Symptôme
no space left on device

# Diagnostic
docker system df
df -h

# Solutions
docker system prune -a --volumes  # ⚠️ ATTENTION: Supprime beaucoup
docker image prune
docker container prune
docker volume prune
```

---

## 🏗️ Problèmes de Build

### 1. Build très lent
```dockerfile
# ❌ Problème : Ordre des layers
FROM python:3.11-slim
COPY . .  # Copie tout, invalide le cache à chaque changement
RUN pip install -r requirements.txt

# ✅ Solution : Dependencies d'abord
FROM python:3.11-slim
COPY requirements.txt .
RUN pip install -r requirements.txt  # Mis en cache
COPY . .  # Copié seulement si le code change
```

### 2. COPY échoue
```bash
# Symptôme
COPY failed: file not found in build context

# Solution
# Vérifier que le fichier existe relativement au Dockerfile
ls -la  # Dans le répertoire du Dockerfile

# Vérifier .dockerignore
cat .dockerignore
```

### 3. Dépendances manquantes
```dockerfile
# Symptôme
/bin/sh: command not found

# Solution pour Alpine
FROM python:3.11-alpine
RUN apk add --no-cache build-base curl

# Solution pour Debian/Ubuntu
FROM python:3.11-slim
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*
```

---

## 🚀 Problèmes de Conteneurs

### 1. Conteneur se ferme immédiatement
```bash
# Diagnostic
docker logs <container-id>
docker run -it mon-image sh  # Debug interactif

# Causes communes
# 1. Processus principal se termine
CMD ["python", "app.py"]  # Au lieu de CMD ["python", "-c", "print('hello')"]

# 2. Erreur dans le script
#!/bin/bash
set -e  # Arrêter sur la première erreur
exec "$@"  # Exécuter la commande principale
```

### 2. Application non accessible
```bash
# Symptôme
curl: (7) Failed to connect to localhost port 8080

# Vérifications
docker ps  # Le conteneur tourne-t-il ?
docker logs <container-id>  # Y a-t-il des erreurs ?

# Solution Flask/Express/etc.
# ❌ app.run(host='127.0.0.1')  # Écoute seulement localhost
# ✅ app.run(host='0.0.0.0')    # Écoute toutes les interfaces
```

### 3. Ports non exposés
```bash
# Diagnostic
docker port <container-id>

# Solution
docker run -p 8080:5000 mon-app  # host:container
# Ou dans le Dockerfile
EXPOSE 5000
```

---

## 🌐 Problèmes de Réseau

### 1. Conteneurs ne communiquent pas
```bash
# Diagnostic
docker network ls
docker network inspect bridge

# Solution : Créer un réseau personnalisé
docker network create mon-reseau
docker run --network mon-reseau --name app1 image1
docker run --network mon-reseau --name app2 image2

# Test de connectivité
docker exec app1 ping app2
docker exec app1 nslookup app2
```

### 2. DNS ne fonctionne pas
```bash
# Diagnostic dans le conteneur
docker exec -it <container-id> nslookup google.com

# Solution : Spécifier des DNS
docker run --dns 8.8.8.8 --dns 8.8.4.4 mon-image

# Ou dans docker-compose.yml
services:
  web:
    image: mon-image
    dns:
      - 8.8.8.8
      - 8.8.4.4
```

### 3. Problèmes de proxy
```bash
# Configuration pour corporate proxy
docker build --build-arg HTTP_PROXY=http://proxy.company.com:8080 .

# Ou variables d'environnement
export HTTP_PROXY=http://proxy.company.com:8080
export HTTPS_PROXY=http://proxy.company.com:8080
export NO_PROXY=localhost,127.0.0.1,.company.com

# Configuration daemon Docker
# /etc/docker/daemon.json
{
  "proxies": {
    "default": {
      "httpProxy": "http://proxy.company.com:8080",
      "httpsProxy": "http://proxy.company.com:8080",
      "noProxy": "localhost,127.0.0.1"
    }
  }
}
```

---

## 💾 Problèmes de Volumes

### 1. Données perdues
```bash
# Symptôme : Les données disparaissent au restart

# Solution : Volume persistant
docker run -v mon-volume:/data mon-app
# Au lieu de juste : docker run mon-app

# Vérifier les volumes
docker volume ls
docker volume inspect mon-volume
```

### 2. Permissions sur les volumes
```bash
# Symptôme
permission denied writing to /data

# Solution 1 : Utilisateur correct dans le conteneur
FROM ubuntu
RUN useradd -m -u 1000 appuser
USER appuser

# Solution 2 : Changer les permissions
docker run --user 1000:1000 -v $(pwd):/data mon-app

# Solution 3 : Init container
docker run --rm -v mon-volume:/data alpine chown -R 1000:1000 /data
```

### 3. Volume non monté
```bash
# Diagnostic
docker inspect <container-id> | grep -A 10 "Mounts"

# Vérifier le path
docker run -v /chemin/absolu:/data mon-app  # Path absolu
docker run -v $(pwd):/data mon-app          # Répertoire courant
```

---

## 🐙 Problèmes Docker Compose

### 1. Services ne démarrent pas dans l'ordre
```yaml
# ❌ Problème
version: '3.8'
services:
  web:
    depends_on:
      - db  # Démarre après db, mais db peut ne pas être prêt

# ✅ Solution
version: '3.8'
services:
  web:
    depends_on:
      db:
        condition: service_healthy
  db:
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5
```

### 2. Variables d'environnement non reconnues
```bash
# Vérifier que le fichier .env existe
ls -la .env

# Vérifier le format
# ❌ export VAR=value
# ✅ VAR=value

# Debug des variables
docker-compose config  # Voir la configuration finale
```

### 3. Conflits de ports
```bash
# Symptôme
ERROR: for web Cannot start service web: Ports are not available

# Solution
docker-compose down  # Arrêter les services
docker ps  # Vérifier qu'aucun autre service n'utilise le port
lsof -i :8080  # Voir qui utilise le port 8080

# Changer le port dans docker-compose.yml
ports:
  - "8081:8080"  # Au lieu de 8080:8080
```

---

## 🔍 Problèmes de Debugging

### 1. Logs illisibles
```bash
# Solution : Logs structurés
docker logs <container-id> --timestamps
docker logs <container-id> --follow --tail 100

# Dans l'application
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

### 2. Conteneur ne répond plus
```bash
# Diagnostic
docker exec -it <container-id> ps aux
docker exec -it <container-id> top
docker stats <container-id>

# Solutions
# 1. Redémarrer
docker restart <container-id>

# 2. Signaux
docker kill --signal=SIGUSR1 <container-id>

# 3. Recréer
docker-compose up -d --force-recreate web
```

### 3. Out of Memory (OOM)
```bash
# Diagnostic
dmesg | grep -i "killed process"
docker inspect <container-id> | grep -i oom

# Solution : Limiter la mémoire
docker run --memory=512m mon-app

# Ou optimiser l'application
# Java : -Xmx256m
# Node.js : --max-old-space-size=256
# Python : Profiler avec memory_profiler
```

---

## ⚡ Problèmes de Performance

### 1. Build très lent
```bash
# Solution 1 : BuildKit
export DOCKER_BUILDKIT=1
docker build .

# Solution 2 : Multi-stage build cache
docker build --target development .  # Build seulement dev stage

# Solution 3 : .dockerignore optimisé
echo "node_modules/" >> .dockerignore
echo ".git/" >> .dockerignore
```

### 2. Conteneur lent au démarrage
```dockerfile
# Solution 1 : Init system
FROM ubuntu
RUN apt-get update && apt-get install -y dumb-init
ENTRYPOINT ["dumb-init", "--"]

# Solution 2 : Optimiser l'application
# Precompiler, préchauffer les caches, etc.
```

### 3. I/O disque lent
```bash
# Solution : Volumes optimisés
# Linux
docker run -v /fast/ssd/path:/data mon-app

# macOS/Windows : éviter bind mounts pour gros volumes
docker volume create fast-volume
docker run -v fast-volume:/data mon-app
```

---

## 🛠️ Outils de Diagnostic

### 1. Scripts de debug
```bash
#!/bin/bash
# debug-docker.sh

echo "=== Docker Info ==="
docker version
docker info

echo "=== Containers ==="
docker ps -a

echo "=== Images ==="
docker images

echo "=== Volumes ==="
docker volume ls

echo "=== Networks ==="
docker network ls

echo "=== System Usage ==="
docker system df

echo "=== Logs (derniers containers) ==="
for container in $(docker ps -q); do
    echo "--- Container $container ---"
    docker logs --tail 10 $container
done
```

### 2. Health checks avancés
```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD curl -f http://localhost:8080/health && \
      ps aux | grep -v grep | grep -q "python app.py" || exit 1
```

### 3. Monitoring
```bash
# Statistiques en temps réel
watch -n 1 'docker stats --no-stream'

# Logs en temps réel
docker-compose logs -f

# Événements système
docker events --filter container=mon-container
```

---

## 📚 Ressources pour aller plus loin

- [Docker Troubleshooting Guide](https://docs.docker.com/config/daemon/troubleshoot/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Container Security](https://docs.docker.com/engine/security/)
- [Docker Performance](https://docs.docker.com/config/containers/resource_constraints/)

---

**💡 Conseil :** Gardez ce guide sous la main et n'hésitez pas à consulter les logs - ils contiennent souvent la solution ! 🕵️‍♂️