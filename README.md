# Glint

## Key Components

### 1. Agent Module (`agent/`)
Contains all AI agent-related functionality:
- Core logic for agent operations
- Data processing and analysis modules

### 2. API Module (`api/`)
Handles web interface and agent interactions:
- `views.py`: Main controller for API endpoints
  - Processes HTTP requests
  - Orchestrates agent calls
  - Returns formatted responses
- RESTful endpoint design

### 3. URL Configuration (`Gint/urls.py`)
Central routing configuration:
- Aggregates all API endpoints
- Routes requests to appropriate views