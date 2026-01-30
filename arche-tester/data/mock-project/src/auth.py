"""Authentication module for the mock project.

Handles user authentication, sessions, and authorization.
"""

import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Any

from src.models import User, UserRole


# Session storage
_sessions: dict[str, dict[str, Any]] = {}

# Configuration
SESSION_DURATION_HOURS = 24
SECRET_KEY = "mock-secret-key-for-testing"


def hash_password(password: str) -> str:
    """Hash password using SHA-256."""
    salted = f"{SECRET_KEY}{password}"
    return hashlib.sha256(salted.encode()).hexdigest()


def verify_password(password: str, hashed: str) -> bool:
    """Verify password against hash."""
    return hash_password(password) == hashed


def create_session(user: User) -> str:
    """Create new session for user."""
    token = secrets.token_urlsafe(32)
    _sessions[token] = {
        "user_id": user.id,
        "username": user.username,
        "role": user.role.value,
        "created_at": datetime.now(),
        "expires_at": datetime.now() + timedelta(hours=SESSION_DURATION_HOURS),
    }
    return token


def get_session(token: str) -> dict[str, Any] | None:
    """Get session by token."""
    session = _sessions.get(token)
    if not session:
        return None
    if datetime.now() > session["expires_at"]:
        del _sessions[token]
        return None
    return session


def invalidate_session(token: str) -> bool:
    """Invalidate session."""
    if token in _sessions:
        del _sessions[token]
        return True
    return False


def require_auth(token: str | None) -> dict[str, Any]:
    """Require valid authentication."""
    if not token:
        raise PermissionError("Authentication required")
    session = get_session(token)
    if not session:
        raise PermissionError("Invalid or expired session")
    return session


def require_role(token: str | None, required_role: UserRole) -> dict[str, Any]:
    """Require specific role."""
    session = require_auth(token)
    if session["role"] != required_role.value:
        raise PermissionError(f"Role {required_role.value} required")
    return session


def require_admin(token: str | None) -> dict[str, Any]:
    """Require admin role."""
    return require_role(token, UserRole.ADMIN)


# Login/logout functions
def login(username: str, password: str) -> str:
    """Authenticate user and create session."""
    from src.api import list_users

    users = list_users()
    for user in users:
        if user.username == username:
            # In real app, would check password hash
            return create_session(user)
    raise PermissionError("Invalid credentials")


def logout(token: str) -> bool:
    """Logout user by invalidating session."""
    return invalidate_session(token)


def get_current_user(token: str) -> User | None:
    """Get current user from session."""
    session = get_session(token)
    if not session:
        return None
    from src.api import get_user

    return get_user(session["user_id"])
