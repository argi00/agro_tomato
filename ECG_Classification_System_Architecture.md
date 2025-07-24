# Système de Classification d'ECG en Temps Réel
## Architecture et Documentation Technique

---

## 📋 Table des Matières

1. [Vue d'ensemble du Projet](#vue-densemble-du-projet)
2. [Architecture Système](#architecture-système)
3. [Structure du Projet](#structure-du-projet)
4. [Composants Techniques](#composants-techniques)
5. [Flux de Données](#flux-de-données)
6. [Diagrammes d'Architecture](#diagrammes-darchitecture)
7. [Technologies et Outils](#technologies-et-outils)
8. [Objectifs et Métriques](#objectifs-et-métriques)
9. [Plan de Développement](#plan-de-développement)

---

## 🎯 Vue d'ensemble du Projet

### Titre
**Conception d'un système intelligent de classification de signaux ECG en temps réel, intégré à une application Web interconnectée à un moniteur patient.**

### Justification
Les maladies cardiovasculaires représentent la première cause de décès dans le monde. Le diagnostic précoce via l'analyse d'ECG est crucial, mais l'analyse manuelle présente des limitations :
- ⏱️ Lenteur du processus
- ❌ Risque d'erreurs humaines
- 👨‍⚕️ Dépendance à la disponibilité des spécialistes

### Solution Proposée
Développement d'un système automatisé basé sur le **Deep Learning** pour :
- 🤖 Classification automatique des signaux ECG
- ⚡ Traitement en temps réel
- 🌐 Interface web intuitive
- 📡 Connexion directe aux moniteurs patients
- 🏥 Support de la télémédecine

---

## 🏗️ Architecture Système

### Architecture Globale

```mermaid
graph TB
    subgraph "Acquisition des Données"
        A[Moniteur Patient ECG] -->|Bluetooth| B[Module de Connexion]
        C[Fichiers ECG] --> D[Interface de Chargement]
    end
    
    subgraph "Traitement Backend"
        B --> E[Préprocesseur de Signaux]
        D --> E
        E --> F[Modèle de Classification ML]
        F --> G[Moteur de Prédiction]
    end
    
    subgraph "Interface Utilisateur"
        G --> H[API REST]
        H --> I[Application Web Frontend]
        I --> J[Visualisation ECG]
        I --> K[Dashboard Prédictions]
        I --> L[Alertes Médicales]
    end
    
    subgraph "Stockage"
        M[(Base de Données ECG)]
        N[(Modèles Entraînés)]
        O[(Logs & Métriques)]
    end
    
    E --> M
    F --> N
    G --> O
```

### Architecture en Couches

```mermaid
graph LR
    subgraph "Couche Présentation"
        A1[Interface Web]
        A2[Dashboard]
        A3[API REST]
    end
    
    subgraph "Couche Métier"
        B1[Classification Service]
        B2[Preprocessing Service]
        B3[Prediction Engine]
        B4[Alert Manager]
    end
    
    subgraph "Couche Données"
        C1[Modèle ML]
        C2[Base de Données]
        C3[Cache Redis]
        C4[File Storage]
    end
    
    subgraph "Couche Infrastructure"
        D1[Bluetooth Handler]
        D2[WebSocket Server]
        D3[Background Tasks]
        D4[Monitoring]
    end
    
    A1 --> B1
    A2 --> B2
    A3 --> B3
    B1 --> C1
    B2 --> C2
    B3 --> C3
    B4 --> C4
    C1 --> D1
    C2 --> D2
    C3 --> D3
    C4 --> D4
```

---

## 📁 Structure du Projet

```
ecg_classification_system/
├── 📂 data/
│   ├── 📂 raw/                    # Données ECG brutes
│   ├── 📂 processed/              # Données prétraitées
│   ├── 📂 external/               # Datasets externes
│   └── 📂 interim/                # Données intermédiaires
│
├── 📂 models/
│   ├── 📂 trained/                # Modèles entraînés (.h5, .pkl)
│   ├── 📂 checkpoints/            # Checkpoints d'entraînement
│   └── 📂 experiments/            # Expérimentations ML
│
├── 📂 src/
│   ├── 📂 data/
│   │   ├── preprocessing.py       # Prétraitement des signaux ECG
│   │   ├── data_loader.py         # Chargement des données
│   │   └── augmentation.py        # Augmentation de données
│   │
│   ├── 📂 models/
│   │   ├── cnn_model.py           # Modèle CNN pour ECG
│   │   ├── lstm_model.py          # Modèle LSTM
│   │   ├── ensemble.py            # Modèles d'ensemble
│   │   └── base_model.py          # Classe de base
│   │
│   ├── 📂 training/
│   │   ├── train.py               # Script d'entraînement
│   │   ├── evaluate.py            # Évaluation des modèles
│   │   └── hyperparameter_tuning.py
│   │
│   ├── 📂 inference/
│   │   ├── predictor.py           # Moteur de prédiction
│   │   ├── real_time_processor.py # Traitement temps réel
│   │   └── batch_processor.py     # Traitement par lot
│   │
│   └── 📂 utils/
│       ├── signal_utils.py        # Utilitaires signaux
│       ├── metrics.py             # Métriques d'évaluation
│       └── visualization.py       # Visualisation
│
├── 📂 backend/
│   ├── 📂 api/
│   │   ├── routes/
│   │   │   ├── ecg_routes.py      # Routes ECG
│   │   │   ├── prediction_routes.py
│   │   │   └── monitoring_routes.py
│   │   ├── middleware/             # Middleware API
│   │   └── schemas/                # Schémas de validation
│   │
│   ├── 📂 services/
│   │   ├── ecg_service.py         # Service ECG
│   │   ├── prediction_service.py  # Service prédiction
│   │   ├── bluetooth_service.py   # Service Bluetooth
│   │   └── websocket_service.py   # Service WebSocket
│   │
│   ├── 📂 database/
│   │   ├── models.py              # Modèles de données
│   │   ├── database.py            # Configuration DB
│   │   └── migrations/            # Migrations DB
│   │
│   └── main.py                    # Point d'entrée API
│
├── 📂 frontend/
│   ├── 📂 src/
│   │   ├── 📂 components/
│   │   │   ├── ECGChart.js        # Composant graphique ECG
│   │   │   ├── Dashboard.js       # Dashboard principal
│   │   │   ├── PredictionPanel.js # Panneau prédictions
│   │   │   └── AlertSystem.js     # Système d'alertes
│   │   │
│   │   ├── 📂 services/
│   │   │   ├── api.js             # Client API
│   │   │   ├── websocket.js       # Client WebSocket
│   │   │   └── bluetooth.js       # Interface Bluetooth
│   │   │
│   │   ├── 📂 pages/
│   │   │   ├── Dashboard.js       # Page tableau de bord
│   │   │   ├── RealTime.js        # Page temps réel
│   │   │   └── History.js         # Page historique
│   │   │
│   │   └── App.js                 # Composant principal
│   │
│   ├── package.json
│   └── public/
│
├── 📂 hardware/
│   ├── bluetooth_interface.py     # Interface Bluetooth
│   ├── device_manager.py          # Gestionnaire périphériques
│   └── protocols/                 # Protocoles communication
│
├── 📂 notebooks/
│   ├── 01_data_exploration.ipynb  # Exploration des données
│   ├── 02_model_development.ipynb # Développement modèle
│   ├── 03_evaluation.ipynb        # Évaluation
│   └── 04_visualization.ipynb     # Visualisation
│
├── 📂 tests/
│   ├── test_models.py             # Tests modèles
│   ├── test_api.py                # Tests API
│   ├── test_services.py           # Tests services
│   └── test_integration.py        # Tests d'intégration
│
├── 📂 deployment/
│   ├── Dockerfile                 # Container Docker
│   ├── docker-compose.yml         # Orchestration
│   ├── kubernetes/                # Manifests K8s
│   └── scripts/                   # Scripts déploiement
│
├── 📂 docs/
│   ├── api_documentation.md       # Documentation API
│   ├── user_guide.md             # Guide utilisateur
│   └── technical_specs.md        # Spécifications techniques
│
├── requirements.txt               # Dépendances Python
├── package.json                   # Dépendances Node.js
├── README.md                      # Documentation principale
└── .env.example                   # Variables d'environnement
```

---

## 🔧 Composants Techniques

### 1. Module de Classification ML

```mermaid
graph TD
    A[Signal ECG Brut] --> B[Préprocessing]
    B --> C[Normalisation]
    C --> D[Segmentation]
    D --> E[Feature Extraction]
    E --> F[Modèle CNN-LSTM]
    F --> G[Post-processing]
    G --> H[Classification Result]
    
    subgraph "Classes de Classification"
        I[Normal]
        J[Arythmie]
        K[Fibrillation Atriale]
        L[Tachycardie]
        M[Bradycardie]
    end
    
    H --> I
    H --> J
    H --> K
    H --> L
    H --> M
```

### 2. Architecture du Modèle Deep Learning

```mermaid
graph TB
    subgraph "Input Layer"
        A[ECG Signal - 12 leads x 5000 samples]
    end
    
    subgraph "Feature Extraction"
        B[Conv1D - 64 filters]
        C[MaxPooling1D]
        D[Conv1D - 128 filters]
        E[MaxPooling1D]
        F[Conv1D - 256 filters]
    end
    
    subgraph "Temporal Learning"
        G[LSTM - 128 units]
        H[LSTM - 64 units]
        I[Dropout 0.3]
    end
    
    subgraph "Classification"
        J[Dense - 64 units]
        K[Dropout 0.5]
        L[Dense - 5 classes]
        M[Softmax Activation]
    end
    
    A --> B --> C --> D --> E --> F
    F --> G --> H --> I
    I --> J --> K --> L --> M
```

### 3. Flux de Données Temps Réel

```mermaid
sequenceDiagram
    participant M as Moniteur ECG
    participant B as Bluetooth Service
    participant P as Preprocessor
    participant ML as ML Model
    participant W as WebSocket
    participant F as Frontend
    participant DB as Database
    
    M->>B: Signal ECG continu
    B->>P: Buffer de données
    P->>P: Segmentation (5 sec)
    P->>ML: Signal préprocessé
    ML->>ML: Prédiction
    ML->>W: Résultat + Confiance
    W->>F: Notification temps réel
    ML->>DB: Sauvegarde résultat
    
    Note over P,ML: Latence < 1 seconde
    Note over W,F: Mise à jour UI
```

---

## 🛠️ Technologies et Outils

### Machine Learning & Data Science
| Composant | Technologie | Usage |
|-----------|-------------|-------|
| **Framework ML** | TensorFlow/Keras | Développement des modèles CNN-LSTM |
| **Traitement Signal** | SciPy, PyWavelets | Préprocessing des signaux ECG |
| **Analyse de Données** | Pandas, NumPy | Manipulation et analyse des données |
| **Visualisation** | Matplotlib, Plotly | Graphiques et visualisation ECG |
| **Métriques** | Scikit-learn | Évaluation des performances |

### Backend & API
| Composant | Technologie | Usage |
|-----------|-------------|-------|
| **Framework Web** | FastAPI | API REST haute performance |
| **Base de Données** | PostgreSQL | Stockage des données ECG |
| **Cache** | Redis | Cache des prédictions |
| **Message Queue** | Celery | Tâches asynchrones |
| **WebSocket** | WebSocket | Communication temps réel |

### Frontend
| Composant | Technologie | Usage |
|-----------|-------------|-------|
| **Framework** | React.js | Interface utilisateur |
| **Graphiques** | Chart.js, D3.js | Visualisation ECG interactive |
| **UI Components** | Material-UI | Composants interface |
| **État Global** | Redux | Gestion d'état |
| **WebSocket Client** | Socket.io | Communication temps réel |

### Communication & Hardware
| Composant | Technologie | Usage |
|-----------|-------------|-------|
| **Bluetooth** | PyBluez, Bleak | Communication moniteur patient |
| **Protocoles** | HL7 FHIR | Standards médicaux |
| **Sérialisation** | Protocol Buffers | Optimisation transfert données |

### DevOps & Déploiement
| Composant | Technologie | Usage |
|-----------|-------------|-------|
| **Containerisation** | Docker | Packaging application |
| **Orchestration** | Kubernetes | Déploiement scalable |
| **CI/CD** | GitHub Actions | Intégration continue |
| **Monitoring** | Prometheus, Grafana | Surveillance système |

---

## 📊 Objectifs et Métriques

### Objectif Général
Développer un système intelligent de classification d'ECG intégré à une plateforme Web, avec capacité de prédiction en temps réel.

### Objectifs Spécifiques

#### 1. Performance du Modèle ML
| Métrique | Objectif | Seuil Minimum |
|----------|----------|---------------|
| **Précision** | > 90% | 85% |
| **Rappel** | > 90% | 85% |
| **F1-Score** | > 90% | 85% |
| **Spécificité** | > 95% | 90% |

#### 2. Performance Système
| Métrique | Objectif | Seuil Maximum |
|----------|----------|---------------|
| **Latence Prédiction** | < 500ms | 1000ms |
| **Débit** | > 100 ECG/min | 50 ECG/min |
| **Disponibilité** | > 99.5% | 99% |
| **Temps de Réponse API** | < 200ms | 500ms |

#### 3. Qualité du Code
| Métrique | Objectif |
|----------|----------|
| **Couverture Tests** | > 90% |
| **Documentation** | 100% fonctions |
| **Standards Code** | PEP8, ESLint |

---

## 📈 Plan de Développement

### Phase 1: Foundation (Semaines 1-4)
```mermaid
gantt
    title Phase 1 - Foundation
    dateFormat  YYYY-MM-DD
    section Data & ML
    Collecte données ECG        :2024-01-01, 1w
    Préprocessing               :2024-01-08, 1w
    Modèle baseline            :2024-01-15, 2w
    section Infrastructure
    Setup projet               :2024-01-01, 3d
    API Backend                :2024-01-04, 1w
    Base de données            :2024-01-11, 3d
```

### Phase 2: Core Development (Semaines 5-8)
```mermaid
gantt
    title Phase 2 - Core Development
    dateFormat  YYYY-MM-DD
    section ML Development
    Optimisation modèle        :2024-01-29, 2w
    Évaluation performance     :2024-02-12, 1w
    section Application
    Frontend React             :2024-01-29, 3w
    WebSocket temps réel       :2024-02-12, 1w
```

### Phase 3: Integration (Semaines 9-12)
```mermaid
gantt
    title Phase 3 - Integration
    dateFormat  YYYY-MM-DD
    section Hardware
    Interface Bluetooth        :2024-02-19, 2w
    Tests moniteur patient     :2024-03-05, 1w
    section System
    Intégration complète       :2024-02-26, 2w
    Tests end-to-end          :2024-03-12, 1w
```

### Phase 4: Deployment (Semaines 13-16)
```mermaid
gantt
    title Phase 4 - Deployment
    dateFormat  YYYY-MM-DD
    section Production
    Configuration Docker       :2024-03-19, 1w
    Déploiement cloud         :2024-03-26, 1w
    Monitoring & alertes      :2024-04-02, 1w
    Documentation finale      :2024-04-09, 1w
```

---

## 🔍 Métriques de Surveillance

### Surveillance ML
```mermaid
graph LR
    subgraph "Métriques Modèle"
        A[Accuracy] --> D[Dashboard ML]
        B[Precision] --> D
        C[Recall] --> D
        E[F1-Score] --> D
        F[Confusion Matrix] --> D
    end
    
    subgraph "Dérive des Données"
        G[Data Drift] --> H[Alertes]
        I[Model Drift] --> H
        J[Performance Degradation] --> H
    end
    
    subgraph "Surveillance Temps Réel"
        K[Latence Prédiction] --> L[Grafana]
        M[Débit Traitement] --> L
        N[Erreurs API] --> L
    end
```

### Dashboard de Monitoring
- 📊 **Métriques de Performance ML** : Précision, rappel, F1-score en temps réel
- 🚨 **Alertes Système** : Latence élevée, erreurs, pannes
- 📈 **Analyse des Tendances** : Évolution des performances
- 🔍 **Traçabilité** : Logs détaillés des prédictions

---

## 🚀 Résultats Attendus

### Livrables Principaux

1. **🤖 Modèle de Classification ECG**
   - Performance > 85% sur toutes les métriques
   - Support de 5 classes principales d'arythmies
   - Temps d'inférence < 500ms

2. **🌐 Application Web Complète**
   - Interface intuitive pour visualisation ECG
   - Dashboard temps réel avec prédictions
   - Système d'alertes médicales automatisé
   - Historique des examens et tendances

3. **📡 Module de Connexion Temps Réel**
   - Interface Bluetooth stable avec moniteurs patients
   - Traitement streaming des signaux ECG
   - Prédictions automatiques et instantanées
   - Notifications push en cas d'anomalies

4. **📋 Documentation Technique**
   - Guide d'installation et déploiement
   - Documentation API complète
   - Manuel utilisateur médical
   - Protocoles de maintenance

### Impact Attendu
- 🏥 **Amélioration du diagnostic** : Réduction du temps de diagnostic de 70%
- 👨‍⚕️ **Support aux professionnels** : Assistance au diagnostic pour médecins non-cardiologues
- 🌍 **Télémédecine** : Monitoring à distance des patients
- 📊 **Traçabilité** : Historique complet des examens ECG

---

## 📞 Support et Maintenance

### Équipe Technique
- **Data Scientist** : Développement et optimisation des modèles ML
- **Backend Developer** : API et services backend
- **Frontend Developer** : Interface utilisateur et expérience
- **DevOps Engineer** : Déploiement et infrastructure
- **Medical Advisor** : Validation clinique et spécifications médicales

### Maintenance Continue
- 🔄 **Mise à jour des modèles** : Réentraînement périodique
- 🔒 **Sécurité** : Audits et mises à jour de sécurité
- 📊 **Monitoring** : Surveillance 24/7 des performances
- 🆘 **Support** : Assistance technique et formation utilisateurs

---

*Document généré pour le projet de Système de Classification d'ECG en Temps Réel*
*Version 1.0 - Architecture et Documentation Technique*