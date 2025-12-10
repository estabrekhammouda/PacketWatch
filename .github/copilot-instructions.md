# AI Coding Agent Instructions - PacketWatch

## Project Overview

**PacketWatch** is a FastAPI-based ML inference service for network intrusion detection. The system loads a pre-trained scikit-learn pipeline model and exposes a single prediction endpoint that analyzes network session features to detect potential cyberattacks.

## Architecture

### Core Components
- **FastAPI Application** (`main.py`): Minimal REST API with one prediction endpoint
- **ML Model** (`intrusion_model.pkl`): Pre-trained scikit-learn pipeline containing feature transformations and classifier
- **Request Schema** (`SessionData`): Pydantic model defining the 10 network features required for prediction

### Data Flow
1. Client POST to `/predict` with `SessionData` JSON payload
2. `SessionData` fields extracted into pandas DataFrame (exact column order matches model training)
3. Model pipeline transforms features and outputs binary prediction (0=normal, 1=attack)
4. Response returns original `session_id` and `attack_detected` flag as integer

## Critical Development Patterns

### Model Integration
- The model expects features in specific order (matching DataFrame construction in `predict()`)
- Any new features must be added to: `SessionData` pydantic fields → DataFrame construction → model retraining
- The `.pkl` file is the single source of truth; model code doesn't exist in repo (training occurred externally)

### Pydantic Schema Design
- `encryption_used` and `browser_type` are categorical features requiring model support
- `unusual_time_access` is an integer flag (0/1)
- All fields except `encryption_used` are required (no default suggests it's optional in training)

## Running & Deployment

### Local Development
```bash
# Activate virtual environment
venv\Scripts\activate

# Start development server
uvicorn main:app --reload
```

### Default Configuration
- Server runs on `http://localhost:8000`
- API docs auto-generated at `/docs` (Swagger UI)
- No authentication or rate limiting implemented

## Integration Points & Dependencies

| Dependency | Purpose | Notes |
|---|---|---|
| **fastapi** | Web framework | Minimal; only one POST endpoint |
| **uvicorn** | ASGI server | Production-grade option |
| **pandas** | Feature engineering | Convert input to DataFrame for model pipeline |
| **scikit-learn** | ML framework | Model training/pipeline execution |
| **joblib** | Model persistence | Standard for pickling sklearn objects |

## Code Quality Notes

- Type hints present but incomplete (e.g., `encryption_used: str = None # type: ignore`)
- No validation beyond Pydantic schema (e.g., `ip_reputation_score` range check)
- No logging or error handling for prediction failures
- No tests; verify manually via `/docs` endpoint

## When Adding Features

1. Add field to `SessionData` model with type annotation
2. Include field in DataFrame construction (order matters for model compatibility)
3. Retrain and export model if feature is new to training data
4. Test via Swagger UI at `/docs` after server restart
