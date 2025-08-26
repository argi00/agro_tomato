# 🐳 Workshop Docker - Guide Complet

Bienvenue dans ce workshop Docker ! Ce guide vous accompagne pas à pas dans l'apprentissage de Docker, de la théorie à la pratique.

## 📁 Structure du Workshop

```
docker-workshop/
├── README.md                    # Ce fichier
├── slides/                      # Support de présentation
├── exercises/                   # Exercices pratiques
│   ├── 01-hello-world/
│   ├── 02-ubuntu-interactive/
│   ├── 03-flask-simple/
│   ├── 04-flask-postgres/
│   └── 05-docker-hub/
├── examples/                    # Exemples d'applications
│   ├── flask-api/
│   ├── nodejs-app/
│   └── multi-service/
├── cheatsheets/                 # Aide-mémoires
└── troubleshooting/             # Guide de dépannage
```

## 🎯 Objectifs du Workshop

À la fin de ce workshop, vous saurez :
- ✅ Comprendre les concepts fondamentaux de Docker
- ✅ Utiliser les commandes Docker essentielles
- ✅ Créer des Dockerfiles optimisés
- ✅ Orchestrer plusieurs conteneurs avec Docker Compose
- ✅ Appliquer les bonnes pratiques
- ✅ Déployer vos applications

## ⏱️ Planning (3-4h)

| Durée | Section | Contenu |
|-------|---------|---------|
| 15 min | Introduction | Théorie et concepts |
| 30 min | Commandes de base | Manipulation d'images et conteneurs |
| 30 min | Dockerfile | Création d'images personnalisées |
| 45 min | Application Flask | API dockerisée complète |
| 45 min | Docker Compose | Multi-conteneurs avec BDD |
| 15-30 min | Bonnes pratiques | Optimisation et sécurité |

## 🚀 Démarrage Rapide

1. **Installer Docker** : [Guide d'installation](https://docs.docker.com/get-docker/)
2. **Vérifier l'installation** :
   ```bash
   docker --version
   docker run hello-world
   ```
3. **Cloner ce repository** :
   ```bash
   git clone <url-du-repo>
   cd docker-workshop
   ```

## 📚 Ressources Complémentaires

- [Documentation officielle Docker](https://docs.docker.com/)
- [Docker Hub](https://hub.docker.com/)
- [Guide des bonnes pratiques](./cheatsheets/best-practices.md)
- [Résolution des problèmes courants](./troubleshooting/common-issues.md)

---

**Bonne formation ! 🎓**