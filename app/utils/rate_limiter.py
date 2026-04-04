from fastapi import HTTPException
from app.utils.redis_client import redis_client


def rate_limit(key: str, limit: int = 5, window: int = 60):
    current = redis_client.get(key)

    if current and int(current) >= limit:
        raise HTTPException(status_code=429, detail="Too many requests")

    pipe = redis_client.pipeline()
    pipe.incr(key, 1)
    pipe.expire(key, window)
    pipe.execute()