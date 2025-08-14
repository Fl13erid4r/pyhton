from fastapi import Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

security = HTTPBasic()

# very small in-memory demo credentials
_USERS = {
    "alice": "password1",
    "bob": "password2",
}

def get_current_user_optional(credentials: HTTPBasicCredentials | None = Depends(security)) -> str | None:
    # Accept missing credentials (optional). If credentials provided, validate.
    if not credentials:
        return None
    username = credentials.username
    password = credentials.password
    if username in _USERS and secrets.compare_digest(_USERS[username], password):
        return username
    # invalid credentials -> treat as anonymous
    return None

def get_current_user(credentials: HTTPBasicCredentials = Depends(security)) -> str:
    username = credentials.username
    password = credentials.password
    if username in _USERS and secrets.compare_digest(_USERS[username], password):
        return username
    raise HTTPException(status_code=401, detail="Invalid credentials")

def get_admin_user(credentials: HTTPBasicCredentials = Depends(security)) -> str:
    # For demo, alice is admin
    username = credentials.username
    password = credentials.password
    if username == "alice" and username in _USERS and secrets.compare_digest(_USERS[username], password):
        return username
    raise HTTPException(status_code=403, detail="Admin privileges required")