# 🐧 Exercice 2 : Ubuntu Interactif

## 🎯 Objectif
Apprendre à travailler de manière interactive avec un conteneur et explorer un système Linux.

## 🚀 Instructions

### Étape 1 : Lancer Ubuntu en mode interactif
```bash
# -i : mode interactif
# -t : allouer un pseudo-TTY (terminal)
# bash : commande à exécuter dans le conteneur
docker run -it ubuntu bash
```

**Vous devriez voir :** `root@<container-id>:/#`

### Étape 2 : Explorer l'environnement
```bash
# Dans le conteneur Ubuntu :

# Voir la version d'Ubuntu
cat /etc/os-release

# Explorer l'arborescence
ls -la /

# Vérifier les processus
ps aux

# Voir l'utilisation mémoire
free -h

# Installer un package
apt update
apt install -y curl

# Tester curl
curl -I https://www.google.com
```

### Étape 3 : Travailler avec les fichiers
```bash
# Créer un fichier
echo "Hello from Docker container!" > /tmp/test.txt

# Vérifier le contenu
cat /tmp/test.txt

# Créer un script simple
cat > /tmp/script.sh << 'EOF'
#!/bin/bash
echo "Container ID: $(hostname)"
echo "Current user: $(whoami)"
echo "Current directory: $(pwd)"
echo "Date: $(date)"
EOF

# Rendre exécutable et lancer
chmod +x /tmp/script.sh
/tmp/script.sh
```

### Étape 4 : Sortir du conteneur
```bash
# Méthode 1: Sortir et arrêter le conteneur
exit

# Méthode 2: Détacher le terminal (Ctrl+P puis Ctrl+Q)
# Le conteneur continue de tourner en arrière-plan
```

### Étape 5 : Manipuler le conteneur depuis l'hôte
```bash
# Voir les conteneurs actifs
docker ps

# Si vous avez fait Ctrl+P+Q, reconnecter :
docker attach <container-id>

# Ou exécuter une commande dans un conteneur actif :
docker exec -it <container-id> bash

# Arrêter le conteneur
docker stop <container-id>

# Redémarrer le conteneur
docker start <container-id>
```

## 🔍 Observations Importantes

### Test de Persistance
```bash
# 1. Lancer un nouveau conteneur Ubuntu
docker run -it --name test-persistence ubuntu bash

# 2. Dans le conteneur, créer un fichier
echo "Données importantes" > /home/data.txt

# 3. Sortir avec exit
exit

# 4. Relancer le MÊME conteneur
docker start -i test-persistence

# 5. Vérifier si le fichier existe
cat /home/data.txt

# 6. Comparer avec un NOUVEAU conteneur
docker run -it ubuntu bash
cat /home/data.txt  # Le fichier n'existe pas !
```

## 🧪 Expérimentations

### Test 1 : Isolation des conteneurs
```bash
# Terminal 1
docker run -it --name conteneur1 ubuntu bash
echo "Je suis le conteneur 1" > /tmp/identity.txt

# Terminal 2 (nouvel onglet)
docker run -it --name conteneur2 ubuntu bash
cat /tmp/identity.txt  # Fichier inexistant !
echo "Je suis le conteneur 2" > /tmp/identity.txt
```

### Test 2 : Ressources système
```bash
# Dans un conteneur Ubuntu
docker run -it ubuntu bash

# Voir les limites de ressources
cat /proc/meminfo | head -5
cat /proc/cpuinfo | grep "model name" | head -1

# Comparer avec l'hôte (dans un autre terminal)
cat /proc/meminfo | head -5
```

## 📊 Comparaison des Commandes

| Action | Dans le conteneur | Depuis l'hôte |
|--------|------------------|---------------|
| Lister les processus | `ps aux` | `docker exec <id> ps aux` |
| Créer un fichier | `echo "test" > file.txt` | `docker exec <id> sh -c 'echo "test" > file.txt'` |
| Installer un package | `apt install curl` | `docker exec <id> apt install curl` |

## 🔍 Questions de Compréhension

1. **Que se passe-t-il quand vous faites `exit` dans un conteneur ?**
2. **Les modifications faites dans un conteneur sont-elles persistantes ?**
3. **Deux conteneurs peuvent-ils voir les fichiers l'un de l'autre ?**
4. **Quelle est la différence entre `docker run` et `docker start` ?**

## ✅ Validation

Vous avez réussi si :
- [x] Vous pouvez naviguer dans Ubuntu via Docker
- [x] Vous comprenez la persistence des données dans un conteneur
- [x] Vous savez exécuter des commandes dans un conteneur existant
- [x] Vous comprenez l'isolation entre conteneurs

## 🧩 Défis Bonus

1. **Conteneur en arrière-plan :**
   ```bash
   # Lancer Ubuntu qui tourne indéfiniment
   docker run -d --name ubuntu-background ubuntu sleep infinity
   
   # Se connecter quand on veut
   docker exec -it ubuntu-background bash
   ```

2. **Partage de répertoire :**
   ```bash
   # Monter un dossier de l'hôte dans le conteneur
   docker run -it -v /tmp:/host-tmp ubuntu bash
   # Dans le conteneur : ls /host-tmp
   ```

## 🎓 Ce que vous avez appris

- ✅ Mode interactif avec `-it`
- ✅ Persistence des données dans un conteneur
- ✅ Isolation entre conteneurs
- ✅ Commandes `exec`, `start`, `stop`, `attach`
- ✅ Différence entre arrêter et détacher un conteneur

---

**Prochaine étape :** [Exercice 3 - Application Flask Simple](../03-flask-simple/README.md)