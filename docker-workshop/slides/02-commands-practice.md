# 🐳 Workshop Docker
## Commandes Essentielles - Pratique

---

## 🎯 Objectifs de cette section

- Maîtriser les commandes Docker de base
- Comprendre les images et conteneurs
- Gérer les volumes et réseaux
- Pratiquer avec des exemples concrets

---

## 📸 Gestion des Images

### Télécharger et explorer
```bash
# Télécharger une image
docker pull ubuntu:20.04
docker pull nginx:alpine

# Lister les images
docker images

# Inspecter une image
docker inspect ubuntu:20.04
docker history ubuntu:20.04
```

### Exercice pratique
```bash
# 1. Télécharger ces images
docker pull hello-world
docker pull python:3.11-slim
docker pull redis:alpine

# 2. Comparer leurs tailles
docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}"
```

---

## 🏃‍♂️ Premiers Conteneurs

### Hello World revisité
```bash
# Lancer et analyser
docker run hello-world

# Que s'est-il passé ?
docker ps -a      # Voir le conteneur terminé
docker logs <container-id>
```

### Mode interactif
```bash
# Ubuntu interactif
docker run -it ubuntu:20.04 bash

# Dans le conteneur :
whoami            # root
hostname          # ID du conteneur
cat /etc/os-release
apt update && apt install curl
```

---

## 🌐 Exposition de Ports

### Serveur Web simple
```bash
# Nginx en arrière-plan
docker run -d --name mon-nginx -p 8080:80 nginx:alpine

# Vérifier
docker ps
curl http://localhost:8080
```

### Serveur Python simple
```bash
# Serveur HTTP Python
docker run -d --name python-server -p 8000:8000 \
  python:3.11-slim python -m http.server 8000

# Test
curl http://localhost:8000
```

### 🧪 **Exercice Pratique 1**
```bash
# Objectif : Lancer 3 serveurs web différents
# 1. Nginx sur port 8080
# 2. Apache sur port 8081
# 3. Python HTTP server sur port 8082

# Solutions :
docker run -d --name web1 -p 8080:80 nginx:alpine
docker run -d --name web2 -p 8081:80 httpd:alpine
docker run -d --name web3 -p 8082:8000 \
  python:3.11-slim python -m http.server 8000

# Tester tous les serveurs
for port in 8080 8081 8082; do
  echo "Test port $port:"
  curl -s http://localhost:$port | head -1
done
```

---

## 💾 Volumes et Persistance

### Volume temporaire vs persistant
```bash
# Sans volume (données perdues)
docker run -it --name temp-container alpine sh
echo "données importantes" > /data.txt
exit
docker rm temp-container
# Les données sont perdues !

# Avec volume persistant
docker run -it --name persist-container \
  -v mon-volume:/data alpine sh
echo "données persistantes" > /data/important.txt
exit
docker rm persist-container

# Récupérer les données
docker run -it -v mon-volume:/data alpine sh
cat /data/important.txt  # Toujours là !
```

### Bind mounts
```bash
# Partager un dossier de l'hôte
mkdir ~/shared-folder
echo "Fichier de l'hôte" > ~/shared-folder/host-file.txt

docker run -it -v ~/shared-folder:/app alpine sh
# Dans le conteneur :
ls /app/
echo "Fichier du conteneur" > /app/container-file.txt
exit

# Vérifier sur l'hôte
ls ~/shared-folder/
```

### 🧪 **Exercice Pratique 2**
```bash
# Objectif : Base de données avec persistance
# 1. Lancer PostgreSQL avec volume persistant
# 2. Créer une base et des données
# 3. Supprimer le conteneur
# 4. Relancer et vérifier que les données existent

# Solution :
docker volume create postgres-data

docker run -d --name db-test \
  -e POSTGRES_PASSWORD=secret \
  -e POSTGRES_DB=testdb \
  -v postgres-data:/var/lib/postgresql/data \
  postgres:13

# Attendre que la DB démarre
sleep 10

# Créer des données
docker exec -it db-test psql -U postgres -d testdb -c \
  "CREATE TABLE test (id SERIAL, name TEXT); 
   INSERT INTO test (name) VALUES ('Docker Workshop');"

# Supprimer le conteneur
docker rm -f db-test

# Relancer avec le même volume
docker run -d --name db-test2 \
  -e POSTGRES_PASSWORD=secret \
  -e POSTGRES_DB=testdb \
  -v postgres-data:/var/lib/postgresql/data \
  postgres:13

sleep 10

# Vérifier les données
docker exec -it db-test2 psql -U postgres -d testdb -c \
  "SELECT * FROM test;"
```

---

## 🌐 Réseaux Docker

### Communication entre conteneurs
```bash
# Créer un réseau
docker network create workshop-net

# Base de données
docker run -d --name db --network workshop-net \
  -e POSTGRES_PASSWORD=secret postgres:13

# Application qui se connecte à la DB
docker run -it --name app --network workshop-net \
  postgres:13 psql -h db -U postgres
```

### Isolation réseau
```bash
# Réseau par défaut
docker run -d --name isolated1 nginx:alpine

# Réseau personnalisé
docker network create private-net
docker run -d --name isolated2 --network private-net nginx:alpine

# isolated1 et isolated2 ne peuvent pas communiquer !
```

---

## 🧹 Nettoyage et Maintenance

### Commandes de nettoyage
```bash
# Arrêter tous les conteneurs
docker stop $(docker ps -q)

# Supprimer tous les conteneurs arrêtés
docker container prune

# Supprimer les images non utilisées
docker image prune

# Nettoyage complet (ATTENTION !)
docker system prune -a --volumes
```

### Monitoring des ressources
```bash
# Utilisation de l'espace disque
docker system df

# Statistiques en temps réel
docker stats

# Événements Docker
docker events
```

---

## 🎮 Challenges Pratiques

### Challenge 1 : Stack Web Complète
```bash
# Objectif : Créer une stack Nginx + Redis + App
# 1. Réseau personnalisé
# 2. Redis pour le cache
# 3. Nginx comme reverse proxy
# 4. Application Python simple

# Solutions :
docker network create web-stack

# Redis
docker run -d --name cache --network web-stack redis:alpine

# App Python simple
docker run -d --name app --network web-stack \
  -p 5000:5000 python:3.11-slim sh -c \
  "pip install flask redis && 
   python -c '
from flask import Flask
import redis
app = Flask(__name__)
r = redis.Redis(host=\"cache\")

@app.route(\"/\")
def hello():
    count = r.incr(\"hits\")
    return f\"Hello! Visits: {count}\"

app.run(host=\"0.0.0.0\")'"

# Test
curl http://localhost:5000
```

### Challenge 2 : Debugging
```bash
# Un conteneur mystère avec un problème...
docker run -d --name mystery-app \
  -p 3000:3000 node:16-alpine sh -c \
  "echo 'console.log(\"App starting...\"); 
   setTimeout(() => process.exit(1), 5000)' > app.js && 
   node app.js"

# Votre mission :
# 1. Identifier pourquoi l'app se ferme
# 2. Voir les logs
# 3. Redémarrer automatiquement

# Indices :
docker logs mystery-app
docker ps -a
```

---

## ✅ Validation des Acquis

### Quiz rapide
1. **Quelle commande pour voir les conteneurs arrêtés ?**
2. **Comment partager un fichier entre hôte et conteneur ?**
3. **Comment faire communiquer 2 conteneurs ?**
4. **Quelle différence entre `docker stop` et `docker kill` ?**

### Checkpoint
```bash
# Vous devriez savoir faire :
# ✅ Lancer un conteneur en mode détaché
# ✅ Exposer un port
# ✅ Créer et utiliser un volume
# ✅ Connecter des conteneurs via un réseau
# ✅ Voir les logs d'un conteneur
# ✅ Nettoyer les ressources inutilisées
```

---

## 🚀 Prochaine Étape

### Ce qui nous attend :
- **Dockerfile** : Créer nos propres images
- **Applications personnalisées**
- **Bonnes pratiques de construction**

```bash
# Préparer l'environnement pour la suite
mkdir ~/docker-workshop
cd ~/docker-workshop
```

---

## 💡 Points Clés à Retenir

- 🐳 **Conteneurs = processus isolés**
- 📦 **Images = templates read-only**
- 🔗 **Réseaux = communication entre conteneurs**
- 💾 **Volumes = persistance des données**
- 🧹 **Nettoyage régulier = performances optimales**