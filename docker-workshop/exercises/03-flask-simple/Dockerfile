# Dockerfile pour l'API Flask Todo
# Version optimisée avec bonnes pratiques

# Image de base légère
FROM python:3.11-slim

# Métadonnées
LABEL maintainer="workshop-docker"
LABEL description="API Todo Flask pour le workshop Docker"
LABEL version="1.0"

# Variables d'environnement
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PORT=5000
ENV ENV=production

# Créer un utilisateur non-root pour la sécurité
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Définir le répertoire de travail
WORKDIR /app

# Copier et installer les dépendances en premier (cache Docker)
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copier le code de l'application
COPY app.py .

# Changer les permissions
RUN chown -R appuser:appuser /app
USER appuser

# Exposer le port
EXPOSE 5000

# Healthcheck pour vérifier que l'app fonctionne
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:5000/health || exit 1

# Commande par défaut
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--timeout", "60", "app:app"]