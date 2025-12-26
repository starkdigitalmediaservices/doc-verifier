from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, HTTPException, status
from functools import wraps
import os


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        token = os.getenv("BEARER_TOKEN")

        if not token:
            raise RuntimeError("BEARER_TOKEN not configured")

        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authorization header missing or invalid",
            )

        bearer_token = auth_header.split(" ", 1)[1]

        if bearer_token != token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )

        return await call_next(request)


def verify_bearer_token(request: Request) -> None:
    token = os.getenv("BEARER_TOKEN")

    if not token:
        raise RuntimeError("BEARER_TOKEN not configured")

    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header missing or invalid",
        )

    bearer_token = auth_header.split(" ", 1)[1]

    if bearer_token != token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )


def require_bearer_auth(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        request: Request = kwargs.get("request")

        if request is None:
            raise RuntimeError(
                "Request object must be passed as a keyword argument"
            )

        verify_bearer_token(request)

        return await func(*args, **kwargs)

    return wrapper
