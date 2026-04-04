from app.utils.redis_client import redis_client


def blacklist_token(token: str, ttl: int):
    redis_client.setex(f"blacklist:{token}", ttl, "1")


def is_token_blacklisted(token: str) -> bool:
    return redis_client.exists(f"blacklist:{token}") == 1