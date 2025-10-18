from redis.asyncio import Redis
from src.config import secrets

JTI_EXPIRY = 3600
token_blocklist = Redis(
    host=secrets.REDIS_HOST,
    port=secrets.REDIS_PORT,
    db=0, decode_responses=True
)

async def add_jti_to_blocklist(jti: str) -> None:
    """
    Add a token's jti to the Redis blocklist with an expiration time.
    """
    await token_blocklist.setex(jti, JTI_EXPIRY, "revoked")


async def token_in_blocklist(jti: str) -> bool:
    """
    Check if a token's jti is in the Redis blocklist.
    """
    result = await token_blocklist.get(jti)
    return result == "revoked"

async def close_redis_connection():
    """
    Close the Redis connection gracefully (call this on app shutdown).
    """
    await token_blocklist.close()