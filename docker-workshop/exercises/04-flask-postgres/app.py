#!/usr/bin/env python3
"""
Flask API avec PostgreSQL pour Docker Workshop
Gestion de todos avec persistance en base de données
"""

from flask import Flask, request, jsonify
from datetime import datetime
import os
import psycopg2
import psycopg2.extras
from contextlib import contextmanager
import time
import sys

app = Flask(__name__)

# Configuration de la base de données
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'database': os.getenv('DB_NAME', 'todoapp'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', 'password'),
    'port': os.getenv('DB_PORT', '5432')
}

@contextmanager
def get_db_connection():
    """Context manager pour les connexions à la base de données"""
    conn = None
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        yield conn
    except psycopg2.Error as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            conn.close()

def wait_for_db(max_retries=30, delay=1):
    """Attendre que la base de données soit disponible"""
    print("🔄 Attente de la base de données...")
    
    for attempt in range(max_retries):
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT 1")
                print("✅ Base de données connectée!")
                return True
        except psycopg2.Error as e:
            print(f"❌ Tentative {attempt + 1}/{max_retries} échouée: {e}")
            time.sleep(delay)
    
    print("💥 Impossible de se connecter à la base de données")
    sys.exit(1)

def init_db():
    """Initialiser la base de données"""
    print("🔧 Initialisation de la base de données...")
    
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            # Créer la table todos si elle n'existe pas
            cur.execute("""
                CREATE TABLE IF NOT EXISTS todos (
                    id SERIAL PRIMARY KEY,
                    task VARCHAR(255) NOT NULL,
                    completed BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Vérifier s'il y a déjà des données
            cur.execute("SELECT COUNT(*) FROM todos")
            count = cur.fetchone()[0]
            
            # Insérer des données de test si la table est vide
            if count == 0:
                sample_todos = [
                    ("Apprendre Docker", False),
                    ("Maîtriser Docker Compose", False),
                    ("Configurer PostgreSQL", True),
                    ("Déployer en production", False)
                ]
                
                for task, completed in sample_todos:
                    cur.execute(
                        "INSERT INTO todos (task, completed) VALUES (%s, %s)",
                        (task, completed)
                    )
                print(f"✅ {len(sample_todos)} todos de test ajoutés")
            
        conn.commit()
    print("✅ Base de données initialisée")

@app.route('/')
def home():
    """Page d'accueil avec informations sur l'API"""
    return {
        "message": "🐳 API Todo avec PostgreSQL - Workshop Docker",
        "version": "2.0",
        "environment": os.getenv("ENV", "development"),
        "database": {
            "host": DB_CONFIG['host'],
            "database": DB_CONFIG['database'],
            "user": DB_CONFIG['user']
        },
        "endpoints": {
            "GET /": "Informations API",
            "GET /todos": "Liste des tâches",
            "POST /todos": "Créer une tâche",
            "PUT /todos/<id>": "Modifier une tâche",
            "DELETE /todos/<id>": "Supprimer une tâche",
            "GET /health": "Status de santé",
            "GET /stats": "Statistiques"
        }
    }

@app.route('/health')
def health():
    """Endpoint de santé pour les checks Docker"""
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT COUNT(*) FROM todos")
                todo_count = cur.fetchone()[0]
        
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "container_id": os.getenv("HOSTNAME", "unknown"),
            "database": "connected",
            "todo_count": todo_count
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "timestamp": datetime.now().isoformat(),
            "error": str(e)
        }, 500

@app.route('/stats')
def stats():
    """Statistiques de l'application"""
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                # Compter tous les todos
                cur.execute("SELECT COUNT(*) FROM todos")
                total = cur.fetchone()[0]
                
                # Compter les todos complétés
                cur.execute("SELECT COUNT(*) FROM todos WHERE completed = TRUE")
                completed = cur.fetchone()[0]
                
                # Compter les todos en cours
                cur.execute("SELECT COUNT(*) FROM todos WHERE completed = FALSE")
                pending = cur.fetchone()[0]
                
                # Todo le plus récent
                cur.execute("""
                    SELECT task, created_at FROM todos 
                    ORDER BY created_at DESC LIMIT 1
                """)
                latest = cur.fetchone()
                
        return {
            "statistics": {
                "total_todos": total,
                "completed_todos": completed,
                "pending_todos": pending,
                "completion_rate": round((completed / total * 100) if total > 0 else 0, 2)
            },
            "latest_todo": {
                "task": latest[0] if latest else None,
                "created_at": latest[1].isoformat() if latest else None
            }
        }
    except Exception as e:
        return {"error": str(e)}, 500

@app.route('/todos', methods=['GET'])
def get_todos():
    """Récupérer toutes les tâches"""
    try:
        with get_db_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute("""
                    SELECT id, task, completed, 
                           created_at, updated_at 
                    FROM todos 
                    ORDER BY id DESC
                """)
                todos = cur.fetchall()
                
                # Convertir les timestamps en strings
                for todo in todos:
                    todo['created_at'] = todo['created_at'].isoformat()
                    todo['updated_at'] = todo['updated_at'].isoformat()
        
        return {
            "todos": todos,
            "count": len(todos)
        }
    except Exception as e:
        return {"error": str(e)}, 500

@app.route('/todos', methods=['POST'])
def create_todo():
    """Créer une nouvelle tâche"""
    try:
        data = request.get_json()
        if not data or 'task' not in data:
            return {"error": "Le champ 'task' est requis"}, 400
        
        with get_db_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute("""
                    INSERT INTO todos (task, completed) 
                    VALUES (%s, %s) 
                    RETURNING id, task, completed, created_at, updated_at
                """, (data['task'], data.get('completed', False)))
                
                new_todo = cur.fetchone()
                new_todo['created_at'] = new_todo['created_at'].isoformat()
                new_todo['updated_at'] = new_todo['updated_at'].isoformat()
            
            conn.commit()
        
        return new_todo, 201
    except Exception as e:
        return {"error": str(e)}, 500

@app.route('/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    """Modifier une tâche existante"""
    try:
        data = request.get_json()
        if not data:
            return {"error": "Données JSON requises"}, 400
        
        with get_db_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                # Vérifier que le todo existe
                cur.execute("SELECT id FROM todos WHERE id = %s", (todo_id,))
                if not cur.fetchone():
                    return {"error": "Tâche non trouvée"}, 404
                
                # Construire la requête de mise à jour dynamiquement
                updates = []
                values = []
                
                if 'task' in data:
                    updates.append("task = %s")
                    values.append(data['task'])
                
                if 'completed' in data:
                    updates.append("completed = %s")
                    values.append(data['completed'])
                
                if updates:
                    updates.append("updated_at = CURRENT_TIMESTAMP")
                    values.append(todo_id)
                    
                    query = f"""
                        UPDATE todos 
                        SET {', '.join(updates)}
                        WHERE id = %s
                        RETURNING id, task, completed, created_at, updated_at
                    """
                    
                    cur.execute(query, values)
                    updated_todo = cur.fetchone()
                    updated_todo['created_at'] = updated_todo['created_at'].isoformat()
                    updated_todo['updated_at'] = updated_todo['updated_at'].isoformat()
                else:
                    return {"error": "Aucune donnée à mettre à jour"}, 400
            
            conn.commit()
        
        return updated_todo
    except Exception as e:
        return {"error": str(e)}, 500

@app.route('/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    """Supprimer une tâche"""
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                # Vérifier que le todo existe
                cur.execute("SELECT task FROM todos WHERE id = %s", (todo_id,))
                todo = cur.fetchone()
                if not todo:
                    return {"error": "Tâche non trouvée"}, 404
                
                # Supprimer le todo
                cur.execute("DELETE FROM todos WHERE id = %s", (todo_id,))
            
            conn.commit()
        
        return {"message": f"Tâche '{todo[0]}' supprimée avec succès"}
    except Exception as e:
        return {"error": str(e)}, 500

@app.errorhandler(404)
def not_found(error):
    return {"error": "Endpoint non trouvé"}, 404

@app.errorhandler(500)
def internal_error(error):
    return {"error": "Erreur interne du serveur"}, 500

if __name__ == '__main__':
    # Attendre que la base de données soit disponible
    wait_for_db()
    
    # Initialiser la base de données
    init_db()
    
    # Configuration pour Docker
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('DEBUG', 'False').lower() == 'true'
    
    print(f"🚀 Démarrage de l'API sur le port {port}")
    print(f"🐳 Environnement: {os.getenv('ENV', 'development')}")
    print(f"🗄️ Base de données: {DB_CONFIG['host']}:{DB_CONFIG['port']}")
    
    app.run(host='0.0.0.0', port=port, debug=debug)