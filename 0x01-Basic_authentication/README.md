# Simple API

Simple HTTP REST API with basic authentication and user management.

## Codebase

### `models/`

- `base.py`: base of the models - handle the database
- `user.py`: user model - handle user data

### `api/v1`

- `app.py`: main file of the API
- `views/index.py`: index endpoint
- `views/users.py`: users endpoints

## Setup

### Requirements

- Python 3.7
- pip

### Install

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
API_HOST=0.0.0.0 API_PORT=5000 python3 -m api.v1.app
```

## Routes

- `GET /api/v1/status`: returns the status of the API
- `GET /api/v1/stats`: returns some stats of the API
- `GET /api/v1/users`: returns the list of users
- `GET /api/v1/users/:id`: returns an user based on the ID
- `DELETE /api/v1/users/:id`: deletes an user based on the ID
- `POST /api/v1/users`: creates a new user (JSON parameters: `email`, `password`, `last_name` (optional) and `first_name` (optional))
- `PUT /api/v1/users/:id`: updates an user based on the ID (JSON parameters: `last_name` and `first_name`)
