# 🐳 Docker - Commandes Essentielles

## 📸 Images Docker

### Gestion des images
```bash
# Lister les images locales
docker images
docker image ls

# Télécharger une image
docker pull ubuntu:20.04
docker pull nginx:alpine

# Supprimer une image
docker rmi ubuntu:20.04
docker image rm nginx:alpine

# Supprimer les images non utilisées
docker image prune
docker image prune -a  # Toutes les images non utilisées

# Inspecter une image
docker inspect ubuntu:20.04
docker history ubuntu:20.04

# Rechercher une image sur Docker Hub
docker search nginx
```

### Construction d'images
```bash
# Construire une image depuis un Dockerfile
docker build -t mon-app:v1.0 .
docker build -t mon-app:latest --no-cache .

# Construire avec un Dockerfile spécifique
docker build -f Dockerfile.prod -t mon-app:prod .

# Construire avec build args
docker build --build-arg VERSION=1.0 -t mon-app .

# Taguer une image
docker tag mon-app:v1.0 mon-app:latest
docker tag mon-app:v1.0 registry.com/mon-app:v1.0
```

---

## 🏃‍♂️ Conteneurs Docker

### Lifecycle des conteneurs
```bash
# Créer et démarrer un conteneur
docker run ubuntu:20.04
docker run -it ubuntu:20.04 bash     # Mode interactif
docker run -d nginx:alpine           # Mode détaché (background)

# Démarrer/arrêter un conteneur existant
docker start <container-id>
docker stop <container-id>
docker restart <container-id>

# Mettre en pause/reprendre
docker pause <container-id>
docker unpause <container-id>

# Supprimer un conteneur
docker rm <container-id>
docker rm -f <container-id>          # Forcer la suppression
```

### Informations sur les conteneurs
```bash
# Lister les conteneurs
docker ps                            # Conteneurs actifs
docker ps -a                         # Tous les conteneurs
docker ps -q                         # IDs seulement

# Inspecter un conteneur
docker inspect <container-id>
docker logs <container-id>
docker logs -f <container-id>        # Suivre les logs

# Statistiques en temps réel
docker stats
docker stats <container-id>

# Processus dans un conteneur
docker top <container-id>
```

### Interaction avec les conteneurs
```bash
# Exécuter une commande dans un conteneur
docker exec -it <container-id> bash
docker exec <container-id> ls -la /app

# Copier des fichiers
docker cp file.txt <container-id>:/app/
docker cp <container-id>:/app/logs ./logs

# Attacher/détacher un terminal
docker attach <container-id>
# Détacher : Ctrl+P puis Ctrl+Q
```

---

## 🌐 Réseaux Docker

### Gestion des réseaux
```bash
# Lister les réseaux
docker network ls

# Créer un réseau
docker network create mon-reseau
docker network create --driver bridge mon-bridge

# Connecter un conteneur à un réseau
docker network connect mon-reseau <container-id>
docker network disconnect mon-reseau <container-id>

# Inspecter un réseau
docker network inspect mon-reseau

# Supprimer un réseau
docker network rm mon-reseau
docker network prune                 # Supprimer réseaux non utilisés
```

### Ports et exposition
```bash
# Exposer des ports
docker run -p 8080:80 nginx          # Port hôte:port conteneur
docker run -p 127.0.0.1:8080:80 nginx # IP spécifique
docker run -P nginx                   # Ports aléatoires

# Voir les ports exposés
docker port <container-id>
```

---

## 💾 Volumes Docker

### Types de volumes
```bash
# Volume nommé
docker volume create mon-volume
docker run -v mon-volume:/data alpine

# Bind mount (dossier hôte)
docker run -v /host/path:/container/path alpine
docker run -v $(pwd):/app alpine

# Volume temporaire
docker run --tmpfs /tmp alpine
```

### Gestion des volumes
```bash
# Lister les volumes
docker volume ls

# Inspecter un volume
docker volume inspect mon-volume

# Supprimer un volume
docker volume rm mon-volume
docker volume prune                   # Supprimer volumes non utilisés

# Sauvegarder un volume
docker run --rm -v mon-volume:/data -v $(pwd):/backup alpine \
  tar czf /backup/backup.tar.gz -C /data .

# Restaurer un volume
docker run --rm -v mon-volume:/data -v $(pwd):/backup alpine \
  tar xzf /backup/backup.tar.gz -C /data
```

---

## 🐙 Docker Compose

### Gestion des services
```bash
# Démarrer les services
docker-compose up
docker-compose up -d                 # En arrière-plan
docker-compose up --build            # Reconstruire les images

# Arrêter les services
docker-compose down
docker-compose down -v               # Supprimer aussi les volumes
docker-compose stop
docker-compose start

# Scaling
docker-compose up -d --scale web=3
```

### Information et debugging
```bash
# Status des services
docker-compose ps

# Logs
docker-compose logs
docker-compose logs -f web           # Suivre logs du service web

# Exécuter des commandes
docker-compose exec web bash
docker-compose run web python manage.py migrate

# Configuration
docker-compose config                # Valider docker-compose.yml
docker-compose config --services     # Lister les services
```

---

## 🧹 Nettoyage et Maintenance

### Nettoyage général
```bash
# Nettoyer tout ce qui n'est pas utilisé
docker system prune

# Nettoyage agressif (attention !)
docker system prune -a --volumes

# Nettoyer par type de ressource
docker container prune               # Conteneurs arrêtés
docker image prune                   # Images non taguées
docker volume prune                  # Volumes non utilisés
docker network prune                 # Réseaux non utilisés
```

### Informations système
```bash
# Utilisation de l'espace disque
docker system df

# Informations détaillées
docker system df -v

# Informations Docker
docker info
docker version
```

---

## 🔧 Options Utiles

### Options de docker run
```bash
# Nom du conteneur
--name mon-conteneur

# Variables d'environnement
-e KEY=value
--env-file .env

# Suppression automatique
--rm

# Mode interactif
-it

# Mode détaché
-d

# Redémarrage automatique
--restart unless-stopped
--restart always

# Limites de ressources
--memory 512m
--cpus 1.5

# Utilisateur
--user 1000:1000

# Répertoire de travail
--workdir /app
```

### Options de docker build
```bash
# Tag
-t nom:tag

# Fichier Dockerfile
-f Dockerfile.prod

# Pas de cache
--no-cache

# Arguments de build
--build-arg VERSION=1.0

# Target pour multi-stage
--target production
```

---

## 🆘 Commandes de Debug

### Inspection et troubleshooting
```bash
# Voir les événements Docker
docker events

# Inspecter en détail
docker inspect <container-id> | jq '.[0].State'

# Entrer dans un conteneur en panne
docker run --rm -it --entrypoint sh <image>

# Voir les modifications dans un conteneur
docker diff <container-id>

# Créer une image depuis un conteneur
docker commit <container-id> debug-image:latest
```

### Performance
```bash
# Statistiques en temps réel
docker stats --no-stream

# Voir les processus
docker exec <container-id> ps aux

# Utilisation des ressources
docker exec <container-id> free -h
docker exec <container-id> df -h
```

---

**💡 Conseil :** Utilisez `docker --help` ou `docker <commande> --help` pour plus d'options !