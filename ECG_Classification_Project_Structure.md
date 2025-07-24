# 🫀 Système de Classification d'ECG en Temps Réel

## 📋 Table des Matières
- [1. Présentation du Projet](#1-présentation-du-projet)
- [2. Architecture Générale](#2-architecture-générale)
- [3. Structure du Projet](#3-structure-du-projet)
- [4. Flux de Données](#4-flux-de-données)
- [5. Modules Techniques](#5-modules-techniques)
- [6. Technologies et Outils](#6-technologies-et-outils)
- [7. Phases de Développement](#7-phases-de-développement)
- [8. Métriques et Validation](#8-métriques-et-validation)

---

## 1. Présentation du Projet

### 🎯 Titre
**Conception d'un système intelligent de classification de signaux ECG en temps réel, intégré à une application Web interconnecté à un moniteur patient.**

### 📊 Justification
Les maladies cardiovasculaires sont l'une des premières causes de décès dans le monde. Le diagnostic précoce, notamment à travers l'analyse d'ECG est crucial. Toutefois l'analyse manuelle est :
- ⏱️ **Lente** 
- ❌ **Sujette aux erreurs**
- 👨‍⚕️ **Dépendante de la disponibilité des spécialistes**

### 🎯 Objectifs

#### Objectif Général
Développer un système intelligent de classification d'ECG intégré à une plateforme Web, avec capacité de prédiction à partir de données captées en temps réel via le moniteur patient.

#### Objectifs Spécifiques
1. 🤖 Développer un modèle de classification d'ECG avec une précision > 85%
2. 🌐 Développer une application Web de visualisation et de prédiction 
3. 📡 Intégrer un module de récupération de données en réel depuis le moniteur 
4. 🔮 Appliquer une prédiction sur les signaux captés

---

## 2. Architecture Générale

```mermaid
graph TB
    subgraph "Acquisition de Données"
        A[Moniteur Patient] -->|Bluetooth| B[Module Bluetooth]
        B --> C[API d'Acquisition]
    end
    
    subgraph "Traitement IA"
        C --> D[Preprocessing ECG]
        D --> E[Modèle de Classification]
        E --> F[Post-processing]
    end
    
    subgraph "Application Web"
        F --> G[API Backend Flask/FastAPI]
        G --> H[Interface Utilisateur]
        H --> I[Dashboard de Monitoring]
        I --> J[Alertes en Temps Réel]
    end
    
    subgraph "Stockage"
        G --> K[(Base de Données)]
        K --> L[Historique ECG]
        K --> M[Résultats Prédictions]
    end

    style A fill:#ff9999
    style E fill:#99ff99
    style H fill:#9999ff
```

---

## 3. Structure du Projet

```
ecg-classification/
├── 📁 data/
│   ├── raw/                    # Données ECG brutes
│   ├── processed/              # Données prétraitées
│   ├── external/               # Datasets externes
│   └── real_time/              # Buffer données temps réel
│
├── 📁 models/
│   ├── trained/                # Modèles entraînés (.h5, .pkl)
│   ├── architectures/          # Définitions des modèles
│   ├── preprocessing/          # Modules de prétraitement
│   └── evaluation/             # Scripts d'évaluation
│
├── 📁 notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_model_training.ipynb
│   ├── 03_model_evaluation.ipynb
│   └── 04_real_time_testing.ipynb
│
├── 📁 src/
│   ├── 📁 data/
│   │   ├── acquisition.py      # Module Bluetooth
│   │   ├── preprocessing.py    # Nettoyage données
│   │   └── validation.py       # Validation données
│   │
│   ├── 📁 models/
│   │   ├── cnn_model.py        # Architecture CNN
│   │   ├── lstm_model.py       # Architecture LSTM
│   │   ├── ensemble.py         # Modèles ensemble
│   │   └── predictor.py        # Prédictions temps réel
│   │
│   ├── 📁 api/
│   │   ├── app.py              # Application Flask/FastAPI
│   │   ├── routes.py           # Routes API
│   │   ├── websocket.py        # WebSocket temps réel
│   │   └── auth.py             # Authentification
│   │
│   └── 📁 frontend/
│       ├── static/             # CSS, JS, images
│       ├── templates/          # Templates HTML
│       └── components/         # Composants UI
│
├── 📁 tests/
│   ├── test_models.py
│   ├── test_api.py
│   └── test_bluetooth.py
│
├── 📁 docs/
│   ├── api_documentation.md
│   ├── user_manual.md
│   └── deployment_guide.md
│
├── 📁 configs/
│   ├── model_config.yaml
│   ├── api_config.yaml
│   └── bluetooth_config.yaml
│
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
```

---

## 4. Flux de Données

```mermaid
sequenceDiagram
    participant M as Moniteur Patient
    participant B as Module Bluetooth
    participant A as API Backend
    participant ML as Modèle ML
    participant UI as Interface Web
    participant DB as Base de Données

    M->>B: Signal ECG (temps réel)
    B->>A: Données ECG via Bluetooth
    A->>A: Validation & Nettoyage
    A->>ML: Données prétraitées
    ML->>ML: Classification
    ML->>A: Résultat prédiction
    A->>DB: Sauvegarde résultats
    A->>UI: Diffusion WebSocket
    UI->>UI: Mise à jour dashboard
    
    alt Anomalie détectée
        A->>UI: Alerte critique
        UI->>UI: Notification urgente
    end
```

---

## 5. Modules Techniques

### 🤖 Module de Classification ML

```mermaid
graph LR
    A[Signal ECG Brut] --> B[Filtrage Numérique]
    B --> C[Segmentation]
    C --> D[Extraction Features]
    D --> E[Normalisation]
    E --> F[Modèle CNN/LSTM]
    F --> G[Classification]
    G --> H[Post-processing]
    H --> I[Résultat Final]

    style F fill:#90EE90
```

**Caractéristiques :**
- 🏗️ **Architecture :** CNN + LSTM hybride
- 📊 **Classes :** Normal, Arythmie, Tachycardie, Bradycardie, etc.
- 🎯 **Performance cible :** > 85% accuracy
- ⚡ **Latence :** < 100ms

### 📡 Module Acquisition Bluetooth

```mermaid
graph TD
    A[Moniteur Patient] -->|Bluetooth LE| B[Récepteur]
    B --> C[Parser Protocole]
    C --> D[Validation Signal]
    D --> E[Buffer Circulaire]
    E --> F[API REST]
    
    G[Gestion Erreurs] --> C
    H[Reconnexion Auto] --> B

    style A fill:#FFB6C1
    style F fill:#98FB98
```

### 🌐 Module Application Web

```mermaid
graph TB
    subgraph "Frontend"
        A[Dashboard Monitoring]
        B[Graphiques ECG]
        C[Alertes]
        D[Historique]
    end
    
    subgraph "Backend API"
        E[Routes REST]
        F[WebSocket Handler]
        G[Auth Service]
        H[Business Logic]
    end
    
    subgraph "Database"
        I[(PostgreSQL)]
        J[Cache Redis]
    end
    
    A --> E
    B --> F
    C --> F
    D --> E
    
    E --> I
    F --> J
    G --> I
    H --> I

    style A fill:#87CEEB
    style E fill:#DDA0DD
```

---

## 6. Technologies et Outils

### 🔧 Stack Technique

| Composant | Technologies | Justification |
|-----------|-------------|---------------|
| **ML/IA** | Python, TensorFlow/Keras, Scikit-learn | Écosystème mature pour deep learning |
| **Backend** | Flask/FastAPI, SQLAlchemy, Redis | Performance et scalabilité |
| **Frontend** | React/Vue.js, Chart.js, WebSockets | Interface réactive temps réel |
| **Communication** | Bluetooth LE, WebSocket, REST API | Communication temps réel fiable |
| **Database** | PostgreSQL, Redis | Stockage robuste + cache |
| **Deployment** | Docker, Kubernetes, CI/CD | Déploiement et maintenance |

### 📊 Librairies Spécialisées

```python
# Deep Learning
tensorflow>=2.12.0
keras>=2.12.0
scikit-learn>=1.3.0

# Signal Processing
scipy>=1.10.0
numpy>=1.24.0
pandas>=2.0.0

# Visualization
matplotlib>=3.7.0
plotly>=5.14.0
seaborn>=0.12.0

# Web Framework
fastapi>=0.95.0
uvicorn>=0.21.0
websockets>=11.0

# Bluetooth Communication
pybluez>=0.23
bleak>=0.20.0

# Database
sqlalchemy>=2.0.0
psycopg2>=2.9.0
redis>=4.5.0
```

---

## 7. Phases de Développement

```mermaid
gantt
    title Planning de Développement ECG
    dateFormat  YYYY-MM-DD
    section Phase 1: Données & Modèle
    Collecte données        :done,    data, 2024-01-01, 2024-01-15
    Préparation datasets    :done,    prep, 2024-01-10, 2024-01-25
    Développement modèle    :active,  model, 2024-01-20, 2024-02-15
    Training & validation   :         train, 2024-02-10, 2024-02-28
    
    section Phase 2: Backend
    API Development         :         api, 2024-02-01, 2024-02-20
    Module Bluetooth        :         bt, 2024-02-15, 2024-03-05
    Base de données         :         db, 2024-02-01, 2024-02-15
    
    section Phase 3: Frontend
    Interface utilisateur   :         ui, 2024-02-20, 2024-03-15
    Dashboard monitoring    :         dash, 2024-03-01, 2024-03-20
    Tests utilisateur       :         test, 2024-03-15, 2024-03-30
    
    section Phase 4: Intégration
    Tests intégration       :         int, 2024-03-20, 2024-04-05
    Optimisation performance:         opt, 2024-04-01, 2024-04-15
    Documentation           :         doc, 2024-04-10, 2024-04-25
    Déploiement             :         deploy, 2024-04-20, 2024-04-30
```

### 🎯 Livrables par Phase

#### Phase 1 : Modèle IA (4 semaines)
- ✅ Dataset ECG nettoyé et segmenté
- ✅ Modèle CNN/LSTM entraîné
- ✅ Validation croisée > 85% accuracy
- ✅ Export modèle optimisé

#### Phase 2 : Backend (4 semaines)
- ✅ API REST fonctionnelle
- ✅ Module Bluetooth opérationnel
- ✅ Base de données configurée
- ✅ WebSocket temps réel

#### Phase 3 : Frontend (3 semaines)
- ✅ Interface web responsive
- ✅ Dashboard monitoring en temps réel
- ✅ Système d'alertes
- ✅ Tests utilisateur validés

#### Phase 4 : Intégration (3 semaines)
- ✅ Tests end-to-end
- ✅ Optimisations performance
- ✅ Documentation complète
- ✅ Déploiement production

---

## 8. Métriques et Validation

### 📊 Métriques du Modèle

```mermaid
pie title Distribution des Classes ECG
    "Normal" : 40
    "Arythmie" : 25
    "Tachycardie" : 15
    "Bradycardie" : 10
    "Autres anomalies" : 10
```

### 🎯 KPIs de Performance

| Métrique | Cible | Critique |
|----------|-------|----------|
| **Accuracy** | > 85% | > 90% |
| **Precision** | > 80% | > 85% |
| **Recall** | > 80% | > 85% |
| **F1-Score** | > 80% | > 85% |
| **Latence Prédiction** | < 100ms | < 50ms |
| **Disponibilité** | > 99% | > 99.9% |

### 🔍 Matrice de Confusion Cible

```
               Prédictions
Réalité    Normal  Arythmie  Tachy  Brady
Normal       95%      2%      2%     1%
Arythmie      3%     92%      3%     2%
Tachy         2%      3%     90%     5%
Brady         1%      4%      5%    90%
```

---

## 9. Architecture de Déploiement

```mermaid
graph TB
    subgraph "Production Environment"
        subgraph "Load Balancer"
            LB[Nginx/HAProxy]
        end
        
        subgraph "Application Tier"
            API1[API Instance 1]
            API2[API Instance 2]
            API3[API Instance 3]
        end
        
        subgraph "ML Service"
            ML1[ML Service 1]
            ML2[ML Service 2]
        end
        
        subgraph "Data Tier"
            DB[(PostgreSQL Cluster)]
            REDIS[(Redis Cluster)]
        end
        
        subgraph "Monitoring"
            PROM[Prometheus]
            GRAF[Grafana]
            ALERT[AlertManager]
        end
    end
    
    subgraph "External"
        MONITOR[Moniteur Patient]
        USER[Utilisateurs Web]
    end
    
    MONITOR -->|Bluetooth| API1
    USER --> LB
    LB --> API1
    LB --> API2
    LB --> API3
    
    API1 --> ML1
    API2 --> ML2
    API3 --> ML1
    
    API1 --> DB
    API2 --> DB
    API3 --> DB
    
    API1 --> REDIS
    API2 --> REDIS
    API3 --> REDIS
    
    API1 --> PROM
    API2 --> PROM
    API3 --> PROM
    ML1 --> PROM
    ML2 --> PROM
    
    PROM --> GRAF
    PROM --> ALERT

    style LB fill:#FF6B6B
    style DB fill:#4ECDC4
    style ML1 fill:#45B7D1
    style ML2 fill:#45B7D1
```

---

## 10. Sécurité et Conformité

### 🔒 Mesures de Sécurité

- 🔐 **Chiffrement** : TLS 1.3 pour toutes communications
- 👤 **Authentification** : OAuth 2.0 + JWT
- 🛡️ **Autorisation** : RBAC (Role-Based Access Control)
- 🔍 **Audit** : Logs complets des accès et actions
- 💾 **Données** : Chiffrement AES-256 at rest
- 🌐 **API** : Rate limiting et validation stricte

### 📋 Conformité Médicale

- ✅ **RGPD** : Protection données personnelles
- ✅ **ISO 27001** : Sécurité information
- ✅ **IEC 62304** : Logiciels dispositifs médicaux
- ✅ **FDA Guidelines** : Validation algorithmes ML médicaux

---

## 11. Plan de Tests

### 🧪 Stratégie de Test

```mermaid
graph TD
    A[Tests Unitaires] --> B[Tests d'Intégration]
    B --> C[Tests End-to-End]
    C --> D[Tests de Performance]
    D --> E[Tests de Sécurité]
    E --> F[Tests Utilisateur]
    
    A1[Modèles ML] --> A
    A2[API Routes] --> A
    A3[Bluetooth] --> A
    
    B1[API + ML] --> B
    B2[Frontend + Backend] --> B
    B3[DB + Cache] --> B
    
    C1[User Journey] --> C
    C2[Real-time Flow] --> C
    
    D1[Load Testing] --> D
    D2[Stress Testing] --> D
    
    E1[Penetration] --> E
    E2[Vulnerability] --> E
    
    F1[UAT] --> F
    F2[Usability] --> F

    style A fill:#FFE5B4
    style D fill:#FFB4B4
    style E fill:#FF6B6B
```

---

## 🚀 Conclusion

Ce projet représente une solution complète de télémédecine pour le monitoring cardiaque, combinant :

- 🤖 **Intelligence Artificielle** avancée pour la classification ECG
- 🌐 **Technologies Web** modernes pour l'interface utilisateur
- 📡 **Communication IoT** pour l'acquisition temps réel
- 🏥 **Standards médicaux** pour la sécurité et conformité

L'architecture modulaire permet une évolutivité et une maintenance optimales, while garantissant les performances critiques nécessaires en contexte médical.

---

*Document créé le : 2024*  
*Version : 1.0*  
*Auteur : Équipe de Développement ECG*