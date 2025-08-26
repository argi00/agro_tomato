# 🐍 Exercice 3 : Application Flask Simple

## 🎯 Objectif
Créer votre première application Docker personnalisée avec un Dockerfile optimisé.

## 📋 Contenu de l'exercice
- Application Flask API Todo
- Dockerfile avec bonnes pratiques
- Tests de l'API
- Optimisations Docker

## 🚀 Instructions

### Étape 1 : Explorer l'application
```bash
# Examiner les fichiers
ls -la
cat app.py        # API Flask complète
cat requirements.txt   # Dépendances Python
cat Dockerfile    # Instructions de construction
cat .dockerignore # Fichiers à ignorer
```

### Étape 2 : Tester l'app localement (optionnel)
```bash
# Si Python est installé sur votre machine
pip install -r requirements.txt
python app.py

# Tester dans un autre terminal
curl http://localhost:5000
curl http://localhost:5000/todos
```

### Étape 3 : Construire l'image Docker
```bash
# Construire l'image (-t pour donner un nom/tag)
docker build -t todo-api:v1 .

# Vérifier que l'image a été créée
docker images | grep todo-api
```

### Étape 4 : Lancer le conteneur
```bash
# Lancer en mode détaché avec port mapping
docker run -d --name todo-container -p 8080:5000 todo-api:v1

# Vérifier que le conteneur tourne
docker ps
```

### Étape 5 : Tester l'API
```bash
# Page d'accueil
curl http://localhost:8080

# Récupérer les todos
curl http://localhost:8080/todos

# Créer un nouveau todo
curl -X POST http://localhost:8080/todos \
  -H "Content-Type: application/json" \
  -d '{"task": "Maîtriser Docker", "completed": false}'

# Vérifier le health check
curl http://localhost:8080/health
```

### Étape 6 : Explorer le conteneur
```bash
# Voir les logs
docker logs todo-container

# Se connecter au conteneur
docker exec -it todo-container bash

# Dans le conteneur :
ps aux          # Voir les processus
whoami          # Vérifier l'utilisateur (appuser)
ls -la /app     # Voir les fichiers de l'app
```

### Étape 7 : Tester avec variables d'environnement
```bash
# Arrêter le conteneur actuel
docker stop todo-container
docker rm todo-container

# Relancer avec des variables d'environnement
docker run -d --name todo-dev \
  -p 8080:5000 \
  -e ENV=development \
  -e DEBUG=true \
  todo-api:v1

# Vérifier les variables
curl http://localhost:8080 | jq .environment
```

## 🔍 Analyse du Dockerfile

### Bonnes pratiques implémentées :
```dockerfile
# ✅ Image de base légère
FROM python:3.11-slim

# ✅ Métadonnées
LABEL maintainer="workshop-docker"

# ✅ Variables d'environnement
ENV PYTHONUNBUFFERED=1

# ✅ Utilisateur non-root
RUN groupadd -r appuser && useradd -r -g appuser appuser
USER appuser

# ✅ Cache des layers (requirements.txt en premier)
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app.py .

# ✅ Health check
HEALTHCHECK --interval=30s CMD curl -f http://localhost:5000/health
```

## 🧪 Expérimentations

### Test 1 : Optimisation de la taille
```bash
# Comparer les tailles d'images
docker images | grep todo-api

# Builder avec une image encore plus légère
cat > Dockerfile.alpine << 'EOF'
FROM python:3.11-alpine
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app.py .
EXPOSE 5000
CMD ["python", "app.py"]
EOF

docker build -f Dockerfile.alpine -t todo-api:alpine .
docker images | grep todo-api
```

### Test 2 : Multi-stage build
```bash
cat > Dockerfile.multistage << 'EOF'
# Stage 1: Build
FROM python:3.11-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

# Stage 2: Production
FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY app.py .
ENV PATH=/root/.local/bin:$PATH
EXPOSE 5000
CMD ["python", "app.py"]
EOF

docker build -f Dockerfile.multistage -t todo-api:multistage .
```

### Test 3 : Volumes persistants
```bash
# Créer un volume pour les logs
docker volume create todo-logs

# Lancer avec volume
docker run -d --name todo-with-volume \
  -p 8080:5000 \
  -v todo-logs:/app/logs \
  todo-api:v1
```

## 📊 Tests d'API complets

### Script de test automatisé
```bash
#!/bin/bash
# test-api.sh

API_URL="http://localhost:8080"

echo "🧪 Test de l'API Todo"

# Test 1: Page d'accueil
echo "Test 1: Page d'accueil"
curl -s $API_URL | jq .message

# Test 2: Liste des todos
echo "Test 2: Liste des todos"
curl -s $API_URL/todos | jq .count

# Test 3: Créer un todo
echo "Test 3: Créer un todo"
RESPONSE=$(curl -s -X POST $API_URL/todos \
  -H "Content-Type: application/json" \
  -d '{"task": "Test Docker", "completed": false}')
TODO_ID=$(echo $RESPONSE | jq .id)
echo "Todo créé avec ID: $TODO_ID"

# Test 4: Modifier le todo
echo "Test 4: Modifier le todo"
curl -s -X PUT $API_URL/todos/$TODO_ID \
  -H "Content-Type: application/json" \
  -d '{"completed": true}' | jq .

# Test 5: Supprimer le todo
echo "Test 5: Supprimer le todo"
curl -s -X DELETE $API_URL/todos/$TODO_ID | jq .message

echo "✅ Tests terminés"
```

## 🔍 Questions de Compréhension

1. **Pourquoi utiliser `COPY requirements.txt .` avant `COPY . .` ?**
2. **Quel est l'avantage de l'utilisateur `appuser` ?**
3. **Pourquoi `host='0.0.0.0'` dans Flask est nécessaire ?**
4. **À quoi sert le `.dockerignore` ?**
5. **Comment fonctionne le HEALTHCHECK ?**

## ✅ Validation

Vous avez réussi si :
- [x] L'image se construit sans erreur
- [x] Le conteneur démarre et écoute sur le port 8080
- [x] L'API répond correctement aux requêtes
- [x] Le health check fonctionne
- [x] Vous pouvez créer/modifier/supprimer des todos

## 🧩 Défis Bonus

1. **Optimisation :** Réduire la taille de l'image au maximum
2. **Sécurité :** Scanner l'image avec `docker scout` (si disponible)
3. **Monitoring :** Ajouter des métriques avec `/metrics`
4. **Configuration :** Utiliser un fichier de config externe

## 🎓 Ce que vous avez appris

- ✅ Écriture d'un Dockerfile complet
- ✅ Bonnes pratiques Docker (layers, sécurité, optimisation)
- ✅ Variables d'environnement
- ✅ Health checks
- ✅ Debugging d'applications containerisées

---

**Prochaine étape :** [Exercice 4 - Flask + PostgreSQL avec Docker Compose](../04-flask-postgres/README.md)