-- Script d'initialisation de la base de données
-- Ce script est exécuté automatiquement par PostgreSQL au premier démarrage

-- Créer la table todos si elle n'existe pas déjà
CREATE TABLE IF NOT EXISTS todos (
    id SERIAL PRIMARY KEY,
    task VARCHAR(255) NOT NULL,
    completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Créer un index sur la colonne created_at pour les performances
CREATE INDEX IF NOT EXISTS idx_todos_created_at ON todos(created_at);

-- Créer un index sur la colonne completed pour les statistiques
CREATE INDEX IF NOT EXISTS idx_todos_completed ON todos(completed);

-- Fonction pour mettre à jour automatiquement updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Trigger pour mettre à jour updated_at automatiquement
DROP TRIGGER IF EXISTS update_todos_updated_at ON todos;
CREATE TRIGGER update_todos_updated_at
    BEFORE UPDATE ON todos
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Insérer quelques données de test
INSERT INTO todos (task, completed) VALUES
    ('🐳 Apprendre Docker', true),
    ('🐘 Configurer PostgreSQL', true),
    ('🚀 Maîtriser Docker Compose', false),
    ('☁️ Déployer en production', false),
    ('📊 Ajouter monitoring', false)
ON CONFLICT DO NOTHING;

-- Afficher un message de confirmation
DO $$
BEGIN
    RAISE NOTICE '✅ Base de données todoapp initialisée avec succès!';
END $$;