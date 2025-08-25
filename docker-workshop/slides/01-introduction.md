# 🐳 Workshop Docker
## Introduction à la Conteneurisation

---

## 🤔 Le Problème

### Scenario typique :
```
💻 Développeur : "Ça marche chez moi !"
🖥️ Serveur de prod : "Erreur 500..."
😱 Équipe : "Mais pourquoi ?!"
```

### Causes fréquentes :
- ✗ Versions de dépendances différentes
- ✗ Variables d'environnement manquantes  
- ✗ OS différents (Windows ↔ Linux)
- ✗ Configuration système différente

---

## 🔧 Solutions Avant Docker

### 1. Installation Manuelle
```bash
# Sur chaque serveur...
apt-get install python3.9
pip install flask==2.0.1
# Oops, conflit de dépendances !
```
**Problèmes :** Erreurs humaines, configurations divergentes

### 2. Machines Virtuelles (VMs)
```
VM 1: Ubuntu 20.04 + Python + App1  (2GB RAM)
VM 2: Ubuntu 20.04 + Node.js + App2  (2GB RAM)  
VM 3: Ubuntu 20.04 + Java + App3     (2GB RAM)
Total: 6GB RAM pour 3 apps !
```
**Problèmes :** Lourd, lent, gourmand

---

## 🚀 Docker : La Solution

### Principe
> "Packager l'application AVEC son environnement"

### Avantages
- 🏃‍♂️ **Rapide** : Démarrage en secondes
- 📦 **Portable** : Même conteneur partout
- 🪶 **Léger** : Partage le noyau OS
- 🔒 **Isolé** : Applications séparées
- 🔄 **Reproductible** : Builds identiques

---

## 📊 Docker vs VM : Comparaison

| Aspect | Docker (Conteneurs) | VM (Machines Virtuelles) |
|--------|-------------------|-------------------------|
| **OS** | Partage le noyau hôte | OS complet par VM |
| **Démarrage** | 1-3 secondes | 30-60 secondes |
| **Mémoire** | MB (megabytes) | GB (gigabytes) |
| **Isolation** | Processus | Hardware virtuel |
| **Portabilité** | Excellente | Limitée |

---

## 🏗️ Architecture Docker

```
┌─────────────────────────────────────┐
│           Docker Client             │
│        (docker CLI/Desktop)         │
└─────────────┬───────────────────────┘
              │ Docker API
┌─────────────▼───────────────────────┐
│         Docker Engine              │
│    ┌─────────┐  ┌─────────────┐    │
│    │Container│  │ Container   │    │
│    │   App1  │  │    App2     │    │
│    └─────────┘  └─────────────┘    │
└─────────────────────────────────────┘
              │
┌─────────────▼───────────────────────┐
│        Système d'exploitation       │
│            (Linux/Windows)          │
└─────────────────────────────────────┘
```

---

## 🔑 Concepts Clés

### 📸 **Image Docker**
- "Photo" d'un système à un instant T
- Immuable (read-only)
- Template pour créer des conteneurs

### 🏃‍♂️ **Conteneur**
- Instance d'une image en cours d'exécution
- Processus isolé avec son propre filesystem

### 🏪 **Registry**
- Docker Hub (public)
- Registries privés (entreprise)
- Stockage et partage d'images

---

## 💡 Analogie : Docker = Recette de Cuisine

```
📄 Dockerfile = Recette écrite
🍰 Image = Gâteau dans le moule  
🍽️ Conteneur = Portion servie
👥 Registry = Livre de recettes partagé
```

---

## 🎯 Cas d'Usage Docker

### 🔧 **Développement**
- Environnement identique pour toute l'équipe
- Pas de "ça marche chez moi"

### ☁️ **Déploiement Cloud**
- Kubernetes, AWS ECS, Azure Container Instances
- Scale automatique

### 🤖 **DevOps/CI-CD**
- Tests dans des environnements isolés
- Déploiements automatisés

### 🧠 **Data Science**
- Modèles ML packagés et déployables
- Environnements reproductibles

---

## ❓ Questions Fréquentes

**Q: Docker remplace-t-il les VMs ?**
A: Non, ils sont complémentaires. Docker pour les apps, VMs pour l'isolation complète.

**Q: Docker fonctionne-t-il sur Windows ?**
A: Oui ! Docker Desktop utilise WSL2 ou Hyper-V.

**Q: Est-ce sécurisé ?**
A: Oui, avec les bonnes pratiques (utilisateurs non-root, images officielles, etc.)

---

## 🚀 Prêt pour la Pratique ?

### Prochaine étape :
Commandes Docker essentielles et premiers conteneurs !

```bash
docker run hello-world
# Votre premier conteneur ! 🎉
```