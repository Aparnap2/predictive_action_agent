# Predictive Action Engine

Agentic AI SaaS for employee churn risk prediction and actioning.

## Overview

This project demonstrates a complete agentic AI system that:
1. **Predicts** employee churn risk using rule-based scoring
2. **Reasons** about risk factors using a LangGraph agent workflow
3. ** Recommends** actionable retention strategies
4. **Tracks** outcomes to measure intervention effectiveness

## Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | FastAPI + Python 3.12 |
| Agent | LangGraph (StateGraph) |
| LLM | Ollama (local) - exaone4.0:1.2b |
| Database | PostgreSQL (via Prisma) |
| Frontend | React + Vite + TypeScript |
| Styling | Tailwind CSS |
| Testing | pytest + httpx |

## Quick Start

### Prerequisites

- Docker & Docker Compose
- or: Python 3.12+, Node.js 20+, Ollama

### Option 1: Docker (Recommended)

```bash
# Start all services
docker-compose up --build

# API will be at http://localhost:8000
# Frontend will be at http://localhost:5173
```

### Option 2: Local Development

```bash
# Backend
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m app.main

# Frontend (in another terminal)
cd frontend
npm install
npm run dev
```

### Ollama Setup

```bash
# Install and run Ollama
ollama serve

# Pull the model
docker exec ollama ollama pull ingu627/exaone4.0:1.2b
```

## Project Structure

```
predictive-action/
├── backend/
│   ├── app/
│   │   ├── main.py           # FastAPI entrypoint
│   │   ├── api/routes.py     # API endpoints
│   │   ├── models/
│   │   │   ├── churn.py      # Prediction logic
│   │   │   └── schemas.py    # Pydantic models
│   │   ├── agent/
│   │   │   ├── graph.py      # LangGraph workflow
│   │   │   ├── state.py      # State definitions
│   │   │   └── tools.py      # Action tools
│   │   └── services/
│   │       └── outcome_tracker.py
│   ├── tests/                # TDD test suite
│   └── prisma/               # Database schema
├── frontend/
│   ├── src/
│   │   ├── App.tsx
│   │   ├── pages/
│   │   ├── api/
│   │   └── types/
│   └── package.json
├── data/
│   └── sample_churn_data.csv
├── docker-compose.yml
└── README.md
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Health check |
| POST | `/api/predict` | Single prediction |
| POST | `/api/predict/upload` | Batch CSV upload |
| POST | `/api/act` | Agent reasoning & actions |
| GET | `/api/outcomes` | List outcomes |
| POST | `/api/outcomes` | Create outcome |

## Testing

```bash
# Backend tests
cd backend
source .venv/bin/activate
pytest tests/ -v

# Frontend tests
cd frontend
npm test
```

## Risk Factors

The prediction model considers:

| Factor | Weight | Description |
|--------|--------|-------------|
| Tenure | 25% | New employees are higher risk |
| Satisfaction | 30% | Low satisfaction increases risk |
| Absence | 20% | High absence indicates issues |
| Performance | 25% | Low performance correlates with churn |

## Agent Workflow

```
ingest_prediction → analyze_context → generate_reasoning →
select_actions → execute_actions → track_outcome
```

## License

MIT
