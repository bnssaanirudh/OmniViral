<div align="center">

<h1>⚡ OmniViral</h1>

<p><strong>Autonomous Multi-Modal Predictive Content Lifecycle Forecaster & Agentic Creative Optimization Engine</strong></p>

<p>
  <img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/FastAPI-0.111-009688?style=for-the-badge&logo=fastapi&logoColor=white"/>
  <img src="https://img.shields.io/badge/React-18-61DAFB?style=for-the-badge&logo=react&logoColor=black"/>
  <img src="https://img.shields.io/badge/PostgreSQL-16-336791?style=for-the-badge&logo=postgresql&logoColor=white"/>
  <img src="https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white"/>
  <img src="https://img.shields.io/badge/Kubernetes-Ready-326CE5?style=for-the-badge&logo=kubernetes&logoColor=white"/>
</p>

<p>
  <img src="https://img.shields.io/badge/LangGraph-Agents-FF6B35?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/ChromaDB-VectorDB-FF4B4B?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/MLflow-MLOps-0194E2?style=for-the-badge&logo=mlflow&logoColor=white"/>
  <img src="https://img.shields.io/badge/XGBoost-Ensemble-F7931E?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/PyTorch-GNN-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white"/>
</p>

<p>
  <img src="https://img.shields.io/github/license/bnssaanirudh/OmniViral?style=flat-square"/>
  <img src="https://img.shields.io/github/stars/bnssaanirudh/OmniViral?style=flat-square"/>
  <img src="https://img.shields.io/github/issues/bnssaanirudh/OmniViral?style=flat-square"/>
  <img src="https://img.shields.io/badge/coverage-85%25+-brightgreen?style=flat-square"/>
</p>

<br/>

> **Zero human intervention.** Ingest → Predict → Optimize → Publish. Fully autonomous.

</div>

---

## 📖 Table of Contents

- [Overview](#-overview)
- [Architecture](#-architecture)
- [Modules](#-modules)
- [Tech Stack](#-tech-stack)
- [Quick Start](#-quick-start)
- [Installation](#-installation)
- [API Reference](#-api-reference)
- [ML Pipeline](#-ml-pipeline)
- [Agentic CARAG System](#-agentic-carag-system)
- [Directory Structure](#-directory-structure)
- [Environment Variables](#-environment-variables)
- [Deployment](#-deployment)
- [Monitoring](#-monitoring)
- [Testing](#-testing)
- [Roadmap](#-roadmap)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🌟 Overview

**OmniViral** is a production-grade, enterprise AI platform designed for autonomous content lifecycle management. It implements the full **CRISP-DM** methodology end-to-end — from raw content ingestion to published, optimized output — with no manual steps required.

### What It Does

```
Content Asset
     │
     ▼
┌─────────────────┐
│  Ingestion      │  Watchdog monitors folders → validates → extracts metadata
│  Engine         │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  ML Pipeline    │  EDA → Feature Engineering → Classification → Ensemble
│  (CRISP-DM)     │  → Time Series Forecast → GNN → SHAP Explainability
└────────┬────────┘
         │
         ▼
┌─────────────────┐     score < threshold
│  Gatekeeper     │ ─────────────────────────────────────┐
└────────┬────────┘                                       │
         │ score ≥ threshold                              ▼
         │                                    ┌──────────────────────┐
         │                                    │  CARAG Agent Loop    │
         │                                    │  Critic → Specialist │
         │                                    │  → Editor → Verify   │
         │◄───────────────────────────────────┘
         │
         ▼
┌─────────────────┐
│  Auto Publisher │  YouTube │ Instagram │ TikTok
└─────────────────┘
```

### Key Capabilities

| Capability | Details |
|---|---|
| 🎯 **Virality Prediction** | 10-model ensemble (LR, DT, NB, KNN, SVM, RF, XGBoost, GBM, AdaBoost, Voting) |
| 📈 **90-Day Forecasting** | LSTM, Temporal Fusion Transformer, Autoformer |
| 🤖 **Multi-Agent CARAG** | Critic → Specialist → Editor → Verification loop via LangGraph |
| 🔍 **Semantic Search** | ChromaDB vector store with evergreen content knowledge base |
| 🧠 **Graph Neural Network** | PyTorch Geometric — models audience/platform behavior graphs |
| 🔬 **Explainable AI** | SHAP values for every prediction |
| 📡 **Drift Detection** | PSI + KS test — auto-retraining triggered on drift |
| 🚀 **Auto Publishing** | YouTube, Instagram, TikTok adapters |
| 📊 **MLOps** | MLflow experiment tracking, model registry, leaderboard |
| 🔐 **Multi-Tenant RBAC** | JWT + role-based access (admin, editor, viewer, agent) |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           OMNIVIRAL PLATFORM                            │
│                                                                         │
│  ┌──────────────┐    ┌───────────────────────────────────────────────┐  │
│  │   Frontend   │    │               FastAPI Backend                  │  │
│  │  React + TS  │◄──►│  /ingest  /predict  /forecast  /optimize      │  │
│  │  TailwindCSS │    │  /publish  /metrics  /dashboard  /auth        │  │
│  │  ShadCN UI   │    └──────────────────┬────────────────────────────┘  │
│  └──────────────┘                       │                               │
│                              ┌──────────▼──────────┐                   │
│  ┌──────────────┐            │    Celery Workers    │                   │
│  │   ChromaDB   │            │  ingestion │ ml      │                   │
│  │  Vector DB   │◄──────────►│  agents   │ publish  │                   │
│  │  Embeddings  │            └──────────┬──────────┘                   │
│  └──────────────┘                       │                               │
│                              ┌──────────▼──────────┐                   │
│  ┌──────────────┐            │    ML Pipeline       │                   │
│  │   MLflow     │◄──────────►│  Classification      │                   │
│  │  Experiment  │            │  Ensemble Engine     │                   │
│  │  Tracking    │            │  LSTM/TFT Forecast   │                   │
│  └──────────────┘            │  GNN │ SHAP │ Drift  │                   │
│                              └──────────┬──────────┘                   │
│  ┌──────────────┐                       │                               │
│  │  PostgreSQL  │◄──────────────────────┤                               │
│  │  6 Tables    │            ┌──────────▼──────────┐                   │
│  └──────────────┘            │   CARAG Agents       │                   │
│                              │  Critic │ Specialist  │                   │
│  ┌──────────────┐            │  Editor │ Verification│                   │
│  │    Redis     │◄──────────►│  LangGraph Orchestr. │                   │
│  │  Task Queue  │            └──────────┬──────────┘                   │
│  └──────────────┘                       │                               │
│                              ┌──────────▼──────────┐                   │
│  ┌──────────────┐            │  Publishing Engine   │                   │
│  │  Prometheus  │            │  YouTube │ Instagram  │                   │
│  │  + Grafana   │            │  TikTok              │                   │
│  └──────────────┘            └─────────────────────┘                   │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 📦 Modules

| # | Module | Description |
|---|--------|-------------|
| 1 | **Data Ingestion Engine** | Watchdog file monitoring, async event queue, retry mechanism |
| 2 | **Automated EDA** | Histograms, correlation matrix, pair plots, missing value reports |
| 3 | **Feature Engineering** | One-hot encoding, VIF collinearity detection, greedy feature selection |
| 4 | **Classification Engine** | LR, Decision Tree, Naive Bayes, KNN, SVM — High/Medium/Low Risk |
| 5 | **Ensemble Engine** | Random Forest, XGBoost, GBM, AdaBoost, Voting Classifier — leaderboard.json |
| 6 | **Time Series Forecasting** | LSTM, Autoformer, Informer, TFT — 90-day lifecycle curves |
| 7 | **Graph Neural Network** | PyTorch Geometric — audience/platform/category graphs |
| 8 | **Vector Database** | ChromaDB — chunking, embeddings, semantic search |
| 9 | **CARAG Agent System** | LangGraph multi-agent: Critic → Specialist → Editor → Verification |
| 10 | **Content Improvement** | Manifest generation (`manifest.json`) + FFmpeg edit scripts |
| 11 | **Gatekeeper System** | Configurable score thresholds, loop routing logic |
| 12 | **Auto Publishing Engine** | YouTube / Instagram / TikTok adapters |
| 13 | **FastAPI Backend** | RESTful API with Swagger docs, WebSocket, JWT auth |
| 14 | **React Dashboard** | 6-page enterprise UI — Overview, Predictions, Forecasting, Agents, Publishing, Monitoring |
| 15 | **Database Design** | PostgreSQL — 6 tables with migrations via Alembic |
| 16 | **MLOps** | MLflow model registry, versioning, experiment tracking |
| 17 | **Monitoring** | Prometheus metrics + Grafana dashboards |
| 18 | **Testing** | Pytest unit/integration/API tests (>85% coverage) |
| 19 | **Documentation** | Full API docs, architecture, setup guide |
| 20 | **Deployment** | Docker Compose + Kubernetes (Deployment, Service, Ingress, HPA) |

---

## 🛠️ Tech Stack

### Backend
| Technology | Version | Purpose |
|---|---|---|
| Python | 3.11+ | Core language |
| FastAPI | 0.111 | REST API framework |
| SQLAlchemy | 2.0 | Async ORM |
| PostgreSQL | 16 | Primary database |
| Redis | 7 | Caching & task queue |
| Celery | 5.4 | Distributed task execution |
| Alembic | 1.13 | Database migrations |

### Machine Learning
| Technology | Version | Purpose |
|---|---|---|
| Scikit-Learn | 1.4 | Classification & preprocessing |
| XGBoost | 2.0 | Gradient boosting |
| PyTorch | 2.3 | Deep learning / GNN |
| TensorFlow / Keras | 2.16 | LSTM forecasting |
| SHAP | 0.45 | Explainable AI |
| MLflow | 2.13 | Experiment tracking |

### Agents & Vector DB
| Technology | Version | Purpose |
|---|---|---|
| LangGraph | 0.1 | Multi-agent orchestration |
| LangChain | 0.2 | LLM abstractions |
| LlamaIndex | 0.10 | RAG pipeline |
| ChromaDB | 0.5 | Vector database |

### Frontend
| Technology | Version | Purpose |
|---|---|---|
| React | 18 | UI framework |
| TypeScript | 5 | Type safety |
| TailwindCSS | 3 | Styling |
| ShadCN UI | latest | Component library |
| Recharts | 2 | Interactive charts |
| Vite | 5 | Build tool |

### Infrastructure
| Technology | Purpose |
|---|---|
| Docker + Docker Compose | Containerization |
| Kubernetes | Orchestration |
| Prometheus + Grafana | Monitoring |
| GitHub Actions | CI/CD |
| MinIO | S3-compatible storage |
| Nginx | Reverse proxy |

---

## ⚡ Quick Start

**One-command startup** (Docker required):

```bash
# Clone the repo
git clone https://github.com/bnssaanirudh/OmniViral.git
cd OmniViral

# Copy environment config
cp .env.example .env

# Start all services
docker-compose up -d
```

| Service | URL |
|---|---|
| 🌐 React Dashboard | http://localhost:3000 |
| ⚡ FastAPI Swagger | http://localhost:8000/docs |
| 📊 MLflow UI | http://localhost:5000 |
| 🌸 Flower (Celery) | http://localhost:5555 |
| 📈 Grafana | http://localhost:3001 (admin/admin) |
| 🔭 Prometheus | http://localhost:9090 |
| 🗄️ MinIO | http://localhost:9001 |

---

## 🔧 Installation

### Prerequisites

- Python 3.11+
- Node.js 20+
- Docker & Docker Compose
- PostgreSQL 16 (or use Docker)
- Redis 7 (or use Docker)

### Local Development Setup

```bash
# 1. Clone repository
git clone https://github.com/bnssaanirudh/OmniViral.git
cd OmniViral

# 2. Create virtual environment
python -m venv .venv
source .venv/bin/activate       # Linux/macOS
.venv\Scripts\activate          # Windows

# 3. Install Python dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env with your settings

# 5. Start infrastructure (Postgres + Redis only)
docker-compose up -d postgres redis chromadb

# 6. Run database migrations
alembic upgrade head

# 7. Start the API server
uvicorn backend.app.main:app --reload --port 8000

# 8. Start Celery worker (new terminal)
celery -A backend.app.core.celery_app worker --loglevel=info

# 9. Start Celery beat scheduler (new terminal)
celery -A backend.app.core.celery_app beat --loglevel=info

# 10. Start frontend (new terminal)
cd frontend
npm install
npm run dev
```

### Create Incoming Directories

```bash
mkdir -p incoming/videos incoming/scripts incoming/metadata
mkdir -p data/uploads logs reports
```

---

## 📡 API Reference

Base URL: `http://localhost:8000/api/v1`

Interactive docs: [`/docs`](http://localhost:8000/docs) (Swagger UI)

### Authentication

```bash
# Login (default: admin / admin123)
curl -X POST http://localhost:8000/api/v1/auth/login \
  -d "username=admin&password=admin123"

# Response: { "access_token": "...", "refresh_token": "..." }
```

### Core Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/auth/login` | Login with username/password |
| `POST` | `/auth/register` | Register new user |
| `GET` | `/auth/me` | Current user info |
| `POST` | `/ingest/` | Upload content asset |
| `GET` | `/ingest/` | List all assets |
| `GET` | `/ingest/{id}` | Get asset by ID |
| `POST` | `/predict/` | Run ML prediction |
| `GET` | `/predict/leaderboard` | Model leaderboard |
| `POST` | `/forecast/` | Run 90-day forecast |
| `GET` | `/forecast/asset/{id}` | Get forecasts for asset |
| `POST` | `/optimize/` | Run CARAG agent loop |
| `GET` | `/optimize/logs/{id}` | Agent logs for asset |
| `POST` | `/publish/` | Publish to platforms |
| `GET` | `/metrics/` | System KPI metrics |
| `GET` | `/dashboard/overview` | Dashboard aggregations |
| `GET` | `/dashboard/agent-performance` | Agent performance stats |

### Example: Full Pipeline via API

```bash
TOKEN="Bearer <your_access_token>"

# 1. Ingest a video
ASSET_ID=$(curl -s -X POST http://localhost:8000/api/v1/ingest/ \
  -H "Authorization: $TOKEN" \
  -F "file=@my_video.mp4" \
  -F "title=My Viral Video" \
  -F "platform=youtube" | jq -r '.id')

# 2. Predict virality
curl -X POST http://localhost:8000/api/v1/predict/ \
  -H "Authorization: $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"asset_id\": \"$ASSET_ID\", \"use_ensemble\": true, \"explain\": true}"

# 3. Forecast 90-day lifecycle
curl -X POST http://localhost:8000/api/v1/forecast/ \
  -H "Authorization: $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"asset_id\": \"$ASSET_ID\", \"horizon_days\": 90, \"model\": \"lstm\"}"

# 4. Run CARAG optimization
curl -X POST http://localhost:8000/api/v1/optimize/ \
  -H "Authorization: $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"asset_id\": \"$ASSET_ID\", \"max_iterations\": 3, \"target_score\": 0.75}"

# 5. Publish to YouTube
curl -X POST http://localhost:8000/api/v1/publish/ \
  -H "Authorization: $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"asset_id\": \"$ASSET_ID\", \"platforms\": [\"youtube\"]}"
```

---

## 🤖 ML Pipeline

### Classification Engine

Five baseline classifiers trained on content feature vectors:

```python
classifiers = {
    "LogisticRegression": LogisticRegression(C=1.0, max_iter=1000),
    "DecisionTree":       DecisionTreeClassifier(max_depth=10),
    "NaiveBayes":         GaussianNB(),
    "KNN":                KNeighborisClassifier(n_neighbors=5),
    "SVM":                SVC(kernel='rbf', probability=True),
}
```

**Output:** `High Risk` / `Medium Risk` / `Low Risk` with confidence score.

### Ensemble Engine

```python
ensemble = {
    "RandomForest":       RandomForestClassifier(n_estimators=200),
    "XGBoost":            XGBClassifier(n_estimators=200, learning_rate=0.1),
    "GradientBoosting":   GradientBoostingClassifier(n_estimators=150),
    "AdaBoost":           AdaBoostClassifier(n_estimators=100),
    "VotingClassifier":   VotingClassifier(estimators=[...], voting='soft'),
}
```

**Leaderboard** (`leaderboard.json`) — automatically updated after every training run.

### 90-Day Forecasting

```
Input:  Daily Views, Watch Time, CTR, Engagement
Models: LSTM | Autoformer | Informer | Temporal Fusion Transformer
Output: Growth Curve, Saturation Point, Velocity Score, Plateau Day
```

### Feature Engineering

- **One-Hot Encoding:** category, language, region, platform
- **Collinearity Detection:** Pearson correlation > 0.85 → auto-remove
- **VIF Score:** Variance Inflation Factor > 10 → auto-remove
- **Greedy Selection:** Forward selection + backward elimination

---

## 🧠 Agentic CARAG System

```
┌──────────────────────────────────────────────────────────────┐
│                      CARAG LOOP (LangGraph)                  │
│                                                              │
│  ┌──────────┐    ┌──────────────┐    ┌──────────────────┐   │
│  │  Critic  │───►│  Specialist  │───►│     Editor       │   │
│  │  Agent   │    │    Agent     │    │     Agent        │   │
│  │          │    │              │    │                  │   │
│  │ Detects: │    │  Retrieves:  │    │  Rewrites:       │   │
│  │ •Weakness│    │  •Examples   │    │  •Hook           │   │
│  │ •Dropoff │    │  •ChromaDB   │    │  •Pacing         │   │
│  │ •Pacing  │    │  •Patterns   │    │  •CTA            │   │
│  └──────────┘    └──────────────┘    └────────┬─────────┘   │
│                                               │             │
│                  ┌────────────────────────────▼──────────┐  │
│                  │          Verification Agent            │  │
│                  │  Re-scores → Approve / Retry           │  │
│                  └────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────┘
```

### Optimization Manifest

```json
{
  "trim_intro": 5,
  "add_hook": true,
  "replace_cta": true,
  "scene_reorder": [3, 1, 2],
  "add_broll": [12, 24, 37],
  "improve_thumbnail": true,
  "optimize_title": "7 Secrets Experts Won't Tell You (Revealed)",
  "description_keywords": ["viral", "trending", "2024"]
}
```

---

## 📁 Directory Structure

```
omni-viral/
│
├── backend/                    # FastAPI application
│   ├── app/
│   │   ├── main.py             # App factory, middleware, routers
│   │   ├── api/
│   │   │   ├── deps.py         # Dependency injection (auth, DB)
│   │   │   └── routes/         # auth, ingest, predict, forecast,
│   │   │                       # optimize, publish, metrics, dashboard
│   │   ├── core/
│   │   │   ├── config.py       # Pydantic settings
│   │   │   ├── database.py     # Async SQLAlchemy engine
│   │   │   ├── security.py     # JWT + RBAC
│   │   │   ├── celery_app.py   # Celery + Beat config
│   │   │   └── logging.py      # Loguru structured logging
│   │   ├── models/             # SQLAlchemy ORM (6 tables)
│   │   ├── schemas/            # Pydantic request/response models
│   │   └── tasks/              # Celery async tasks
│   └── alembic/                # Database migrations
│
├── ml_pipeline/                # ML modules
│   ├── ingestion/              # Watchdog service
│   ├── eda/                    # Automated EDA pipeline
│   ├── features/               # Feature engineering
│   ├── classification/         # 5 baseline classifiers
│   ├── gnn/                    # Graph Neural Network
│   ├── explainability/         # SHAP explainer
│   └── drift/                  # Drift detection + retraining
│
├── ensemble_models/            # Bagging, Boosting, Voting ensemble
├── forecasting/                # LSTM, TFT, Autoformer time series
│
├── agents/                     # Multi-agent CARAG system
│   ├── carag/
│   │   ├── orchestrator.py     # LangGraph state machine
│   │   ├── critic_agent.py
│   │   ├── specialist_agent.py
│   │   ├── editor_agent.py
│   │   └── verification_agent.py
│   ├── gatekeeper/             # Threshold-based routing
│   └── publishing/             # YouTube / Instagram / TikTok adapters
│
├── vector_db/                  # ChromaDB client + embeddings
│
├── frontend/                   # React + TypeScript dashboard
│   └── src/
│       ├── pages/              # Overview, Predictions, Forecasting,
│       │                       # AgentLogs, Publishing, Monitoring
│       ├── components/         # Charts, Cards, DataTable, etc.
│       ├── hooks/              # useWebSocket, useMetrics
│       └── api/                # API client + React Query
│
├── monitoring/
│   ├── prometheus/             # prometheus.yml
│   └── grafana/                # Dashboards + provisioning
│
├── docker/                     # Dockerfiles + nginx.conf
├── kubernetes/                 # K8s manifests (Deployment, Service,
│                               # Ingress, ConfigMap, Secret, HPA)
├── .github/workflows/          # CI/CD pipeline (GitHub Actions)
├── tests/                      # Unit + Integration + API tests
├── notebooks/                  # Jupyter notebooks (EDA, modeling)
├── docs/                       # Additional documentation
├── scripts/                    # Utility scripts
│
├── docker-compose.yml          # Full stack (12 services)
├── requirements.txt
├── pyproject.toml
└── .env.example
```

---

## 🔑 Environment Variables

Copy `.env.example` to `.env` and fill in your values:

| Variable | Default | Description |
|---|---|---|
| `SECRET_KEY` | *(required)* | App secret key (32+ chars) |
| `JWT_SECRET_KEY` | *(required)* | JWT signing key |
| `DATABASE_URL` | `postgresql+asyncpg://...` | Async DB connection |
| `REDIS_URL` | `redis://localhost:6379/0` | Redis connection |
| `LLM_PROVIDER` | `mock` | `mock` \| `openai` \| `anthropic` |
| `OPENAI_API_KEY` | *(optional)* | Required if using OpenAI |
| `ANTHROPIC_API_KEY` | *(optional)* | Required if using Anthropic |
| `GATEKEEPER_SCORE_THRESHOLD` | `0.65` | Min score to skip CARAG |
| `GATEKEEPER_MAX_CARAG_ITERATIONS` | `3` | Max agent loop iterations |
| `MLFLOW_TRACKING_URI` | `http://localhost:5000` | MLflow server |
| `CHROMA_HOST` | `localhost` | ChromaDB host |
| `STORAGE_BACKEND` | `local` | `local` \| `s3` |

> **Note:** Set `LLM_PROVIDER=mock` to run without any LLM API keys. All agents will produce realistic mock outputs.

---

## 🚀 Deployment

### Docker Compose (Recommended for local/staging)

```bash
# Start everything
docker-compose up -d

# View logs
docker-compose logs -f backend

# Run migrations
docker-compose exec backend alembic upgrade head

# Scale workers
docker-compose up -d --scale celery_worker=4

# Stop everything
docker-compose down
```

### Kubernetes (Production)

```bash
# Apply all manifests
kubectl apply -f kubernetes/ -n omniviral

# Or apply in order
kubectl apply -f kubernetes/namespace.yaml
kubectl apply -f kubernetes/configmap.yaml
kubectl apply -f kubernetes/secrets.yaml
kubectl apply -f kubernetes/backend-deployment.yaml
kubectl apply -f kubernetes/ingress.yaml

# Check status
kubectl get pods -n omniviral
kubectl get svc -n omniviral

# Watch rollout
kubectl rollout status deployment/omniviral-backend -n omniviral
```

### GitHub Actions CI/CD

Automatic on push to `main`:

```
Push → Lint (Ruff) → Type check (mypy) → Test (pytest)
     → Docker Build & Push → Kubernetes Deploy → Slack notification
```

---

## 📊 Monitoring

### Prometheus Metrics

| Metric | Description |
|---|---|
| `http_requests_total` | Total API requests by endpoint |
| `http_request_duration_seconds` | Request latency histogram |
| `prediction_latency_ms` | ML prediction duration |
| `forecast_accuracy_mape` | Forecast MAPE score |
| `agent_iterations_total` | CARAG loop iteration count |
| `publish_success_total` | Successful publications |
| `drift_score` | Current model drift score |

### Grafana

Import dashboards from `monitoring/grafana/dashboards/`.

Access: `http://localhost:3001` → admin / admin

---

## 🧪 Testing

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=backend --cov=ml_pipeline --cov=agents \
  --cov-report=html --cov-report=term-missing

# Run specific test modules
pytest tests/unit/ -v
pytest tests/integration/ -v
pytest tests/api/ -v

# View HTML coverage report
open htmlcov/index.html
```

**Coverage target: >85%**

---

## 🗺️ Roadmap

- [x] Track A — Backend Core & Infrastructure
- [ ] Track B — ML Pipeline (EDA, Classification, Ensemble, LSTM, GNN, SHAP, Drift)
- [ ] Track C — Agentic CARAG System (ChromaDB, LangGraph, 4 Agents, Publisher)
- [ ] Track D — React Dashboard (6 pages, real-time charts)
- [ ] Track E — Tests & Documentation (>85% coverage, Jupyter notebooks)
- [ ] Real YouTube / Instagram / TikTok API integration
- [ ] Multi-tenant tenant isolation
- [ ] Fine-tuning LLM on domain-specific content data
- [ ] Mobile dashboard (React Native)

---

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch: `git checkout -b feat/amazing-feature`
3. Commit your changes: `git commit -m 'feat: add amazing feature'`
4. Push to the branch: `git push origin feat/amazing-feature`
5. Open a Pull Request

Please follow [Conventional Commits](https://www.conventionalcommits.org/) and ensure tests pass.

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**Built with ❤️ as an enterprise-grade capstone project.**

<sub>OmniViral — Where AI meets Content Intelligence</sub>

</div>
