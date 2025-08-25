# 🌟 Exercice 1 : Hello World Docker

## 🎯 Objectif
Vérifier que Docker fonctionne et comprendre le cycle de vie d'un conteneur basique.

## 📋 Prérequis
- Docker installé et démarré
- Accès à Internet (pour télécharger l'image)

## 🚀 Instructions

### Étape 1 : Vérifier Docker
```bash
# Vérifier la version
docker --version

# Vérifier que le daemon Docker fonctionne
docker info
```

**Résultat attendu :** Version de Docker affichée sans erreur.

### Étape 2 : Premier conteneur
```bash
# Lancer le conteneur hello-world
docker run hello-world
```

**Que se passe-t-il ?**
1. Docker cherche l'image `hello-world` localement
2. Ne la trouve pas → la télécharge depuis Docker Hub
3. Crée un conteneur à partir de cette image
4. Exécute le conteneur (affiche un message)
5. Le conteneur se termine

### Étape 3 : Analyser ce qui s'est passé
```bash
# Voir les images téléchargées
docker images

# Voir tous les conteneurs (même arrêtés)
docker ps -a
```

### Étape 4 : Nettoyage
```bash
# Supprimer le conteneur
docker rm <container-id>

# Supprimer l'image
docker rmi hello-world
```

## 🔍 Questions de Compréhension

1. **Où Docker a-t-il téléchargé l'image `hello-world` ?**
2. **Pourquoi le conteneur s'est-il arrêté tout seul ?**
3. **Quelle est la différence entre `docker ps` et `docker ps -a` ?**

## ✅ Validation

Vous avez réussi si :
- [x] Le message "Hello from Docker!" s'affiche
- [x] Vous voyez l'image dans `docker images`
- [x] Vous voyez le conteneur dans `docker ps -a`

## 🧩 Défi Bonus

Essayez ces variantes :
```bash
# Exécuter et supprimer automatiquement
docker run --rm hello-world

# Donner un nom au conteneur
docker run --name mon-premier-conteneur hello-world
```

## 🎓 Ce que vous avez appris

- ✅ Docker télécharge automatiquement les images manquantes
- ✅ Un conteneur = une instance d'image en cours d'exécution
- ✅ Les conteneurs peuvent se terminer automatiquement
- ✅ Les images et conteneurs persistent après utilisation

---

**Prochaine étape :** [Exercice 2 - Ubuntu Interactif](../02-ubuntu-interactive/README.md)