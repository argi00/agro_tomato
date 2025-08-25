#!/usr/bin/env python3
"""
Simple Flask API for Docker Workshop
API endpoints for managing a todo list
"""

from flask import Flask, request, jsonify
from datetime import datetime
import os

app = Flask(__name__)

# Simple in-memory storage
todos = [
    {"id": 1, "task": "Apprendre Docker", "completed": False, "created": "2024-01-15"},
    {"id": 2, "task": "Créer un Dockerfile", "completed": True, "created": "2024-01-15"},
    {"id": 3, "task": "Utiliser Docker Compose", "completed": False, "created": "2024-01-15"}
]

next_id = 4

@app.route('/')
def home():
    """Page d'accueil avec informations sur l'API"""
    return {
        "message": "🐳 API Todo - Workshop Docker",
        "version": "1.0",
        "environment": os.getenv("ENV", "development"),
        "endpoints": {
            "GET /": "Informations API",
            "GET /todos": "Liste des tâches",
            "POST /todos": "Créer une tâche",
            "PUT /todos/<id>": "Modifier une tâche",
            "DELETE /todos/<id>": "Supprimer une tâche",
            "GET /health": "Status de santé"
        }
    }

@app.route('/health')
def health():
    """Endpoint de santé pour les checks Docker"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "container_id": os.getenv("HOSTNAME", "unknown")
    }

@app.route('/todos', methods=['GET'])
def get_todos():
    """Récupérer toutes les tâches"""
    return jsonify({
        "todos": todos,
        "count": len(todos)
    })

@app.route('/todos', methods=['POST'])
def create_todo():
    """Créer une nouvelle tâche"""
    global next_id
    
    data = request.get_json()
    if not data or 'task' not in data:
        return jsonify({"error": "Le champ 'task' est requis"}), 400
    
    new_todo = {
        "id": next_id,
        "task": data['task'],
        "completed": data.get('completed', False),
        "created": datetime.now().strftime("%Y-%m-%d")
    }
    
    todos.append(new_todo)
    next_id += 1
    
    return jsonify(new_todo), 201

@app.route('/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    """Modifier une tâche existante"""
    todo = next((t for t in todos if t['id'] == todo_id), None)
    if not todo:
        return jsonify({"error": "Tâche non trouvée"}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({"error": "Données JSON requises"}), 400
    
    # Mettre à jour les champs fournis
    if 'task' in data:
        todo['task'] = data['task']
    if 'completed' in data:
        todo['completed'] = data['completed']
    
    return jsonify(todo)

@app.route('/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    """Supprimer une tâche"""
    global todos
    todo = next((t for t in todos if t['id'] == todo_id), None)
    if not todo:
        return jsonify({"error": "Tâche non trouvée"}), 404
    
    todos = [t for t in todos if t['id'] != todo_id]
    return jsonify({"message": f"Tâche {todo_id} supprimée"})

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint non trouvé"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Erreur interne du serveur"}), 500

if __name__ == '__main__':
    # Configuration pour Docker
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('DEBUG', 'False').lower() == 'true'
    
    print(f"🚀 Démarrage de l'API sur le port {port}")
    print(f"🐳 Environnement: {os.getenv('ENV', 'development')}")
    
    # Important: host='0.0.0.0' pour écouter sur toutes les interfaces
    app.run(host='0.0.0.0', port=port, debug=debug)