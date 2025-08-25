# 🐘 Exercice 4 : Flask + PostgreSQL avec Docker Compose

## 🎯 Objectif
Découvrir Docker Compose en orchestrant une application multi-conteneurs (API Flask + Base de données PostgreSQL).

## 📋 Architecture de l'application

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Browser       │    │   Flask API     │    │  PostgreSQL     │
│   localhost:8080│◄──►│   Container     │◄──►│   Container     │
│                 │    │   (todo-api)    │    │   (todo-db)     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │                       
                       ┌─────────────────┐              
                       │   Adminer       │              
                       │   localhost:8081│              
                       │   (admin DB)    │              
                       └─────────────────┘              
```

## 🚀 Instructions

### Étape 1 : Explorer la configuration
```bash
# Examiner la structure
ls -la

# Fichiers principaux :
cat docker-compose.yml  # Configuration multi-services
cat app.py             # API Flask avec PostgreSQL
cat init.sql           # Script d'initialisation DB
cat .env.example       # Variables d'environnement
```

### Étape 2 : Comprendre docker-compose.yml
```yaml
# Services définis :
web:      # API Flask (port 8080)
db:       # PostgreSQL (port 5432)
adminer:  # Interface admin web (port 8081)

# Fonctionnalités utilisées :
- depends_on avec healthcheck
- volumes persistants
- réseaux personnalisés
- variables d'environnement
```

### Étape 3 : Lancer l'application complète
```bash
# Construire et démarrer tous les services
docker-compose up --build

# Ou en arrière-plan
docker-compose up -d --build

# Vérifier que tous les services tournent
docker-compose ps
```

### Étape 4 : Tester l'application
```bash
# API Flask
curl http://localhost:8080
curl http://localhost:8080/todos
curl http://localhost:8080/stats

# Interface admin PostgreSQL
# Ouvrir dans le navigateur : http://localhost:8081
# Server: db, User: postgres, Password: secretpassword
```

### Étape 5 : Manipulation de données
```bash
# Créer un nouveau todo
curl -X POST http://localhost:8080/todos \
  -H "Content-Type: application/json" \
  -d '{"task": "Maîtriser Docker Compose", "completed": false}'

# Modifier un todo
curl -X PUT http://localhost:8080/todos/1 \
  -H "Content-Type: application/json" \
  -d '{"completed": true}'

# Supprimer un todo
curl -X DELETE http://localhost:8080/todos/2

# Voir les statistiques
curl http://localhost:8080/stats | jq
```

### Étape 6 : Explorer les conteneurs
```bash
# Voir les logs de tous les services
docker-compose logs

# Logs d'un service spécifique
docker-compose logs web
docker-compose logs db

# Se connecter au conteneur Flask
docker-compose exec web bash

# Se connecter à PostgreSQL
docker-compose exec db psql -U postgres -d todoapp
```

### Étape 7 : Test de persistance des données
```bash
# Arrêter tous les services
docker-compose down

# Redémarrer (les données doivent persister)
docker-compose up -d

# Vérifier que les données sont toujours là
curl http://localhost:8080/todos
```

## 🔍 Commandes Docker Compose essentielles

```bash
# Gestion des services
docker-compose up              # Démarrer tous les services
docker-compose up -d           # Démarrer en arrière-plan
docker-compose down            # Arrêter et supprimer les conteneurs
docker-compose down -v         # Arrêter et supprimer volumes
docker-compose stop            # Arrêter sans supprimer
docker-compose start           # Redémarrer les services arrêtés

# Information et debugging
docker-compose ps              # Status des services
docker-compose logs            # Logs de tous les services
docker-compose logs -f web     # Suivre les logs du service web
docker-compose top             # Processus en cours
docker-compose images          # Images utilisées

# Gestion des volumes et réseaux
docker-compose exec web bash   # Shell dans le conteneur web
docker-compose run web python # Exécuter une commande ponctuelle
```

## 🧪 Expérimentations

### Test 1 : Scaling (montée en charge)
```bash
# Lancer plusieurs instances du service web
docker-compose up -d --scale web=3

# Voir les conteneurs
docker-compose ps

# Note: Il faudrait un load balancer pour distribuer le trafic
```

### Test 2 : Variables d'environnement
```bash
# Créer un fichier .env
cp .env.example .env

# Modifier les valeurs dans .env
echo "DEBUG=false" >> .env
echo "ENV=production" >> .env

# Redémarrer pour prendre en compte les changements
docker-compose down
docker-compose up -d
```

### Test 3 : Backup de la base de données
```bash
# Sauvegarder la base de données
docker-compose exec db pg_dump -U postgres todoapp > backup.sql

# Restaurer la base de données (si nécessaire)
docker-compose exec -T db psql -U postgres todoapp < backup.sql
```

### Test 4 : Développement avec volumes
```bash
# Modifier docker-compose.yml pour le développement
cat > docker-compose.dev.yml << 'EOF'
version: '3.8'
services:
  web:
    build: .
    volumes:
      - .:/app  # Montage du code source
    environment:
      - DEBUG=true
      - ENV=development
    command: python app.py  # Commande de dev au lieu de gunicorn
EOF

# Utiliser la configuration de développement
docker-compose -f docker-compose.dev.yml up
```

## 🔍 Analyse de l'architecture

### Réseaux Docker
```bash
# Voir le réseau créé
docker network ls | grep todo

# Inspecter le réseau
docker network inspect todo-network

# Tester la communication entre conteneurs
docker-compose exec web ping db
docker-compose exec web nslookup db
```

### Volumes persistants
```bash
# Voir les volumes créés
docker volume ls | grep todo

# Inspecter le volume de données
docker volume inspect todo-postgres-data

# Localiser les données sur l'hôte
docker volume inspect todo-postgres-data | jq '.[0].Mountpoint'
```

## 📊 Monitoring et debugging

### Health checks
```bash
# Vérifier la santé des services
docker-compose ps

# Voir les détails des health checks
docker inspect todo-postgres | jq '.[0].State.Health'
```

### Performance
```bash
# Statistiques des conteneurs
docker stats

# Utilisation des ressources par service
docker-compose top
```

## 🔍 Questions de Compréhension

1. **Comment les conteneurs communiquent-ils entre eux ?**
2. **Que se passe-t-il si on supprime le volume `postgres_data` ?**
3. **Pourquoi utilise-t-on `depends_on` avec `condition: service_healthy` ?**
4. **Comment modifier le port d'écoute de l'API ?**
5. **Que fait le script `init.sql` ?**

## ✅ Validation

Vous avez réussi si :
- [x] Tous les services démarrent sans erreur
- [x] L'API répond sur http://localhost:8080
- [x] Adminer est accessible sur http://localhost:8081
- [x] Les données persistent après un restart
- [x] Vous pouvez créer/modifier/supprimer des todos

## 🧩 Défis Bonus

1. **Load Balancer :** Ajouter un nginx pour distribuer le trafic
2. **Cache :** Ajouter Redis pour la mise en cache
3. **Monitoring :** Ajouter Prometheus + Grafana
4. **SSL :** Configurer HTTPS avec certificats

## 🎓 Ce que vous avez appris

- ✅ Orchestration multi-conteneurs avec Docker Compose
- ✅ Communication entre services via réseaux Docker
- ✅ Volumes persistants pour les données
- ✅ Health checks et dépendances entre services
- ✅ Variables d'environnement et configuration
- ✅ Debugging d'applications multi-conteneurs

---

**Prochaine étape :** [Exercice 5 - Publication sur Docker Hub](../05-docker-hub/README.md)