from redis.asyncio import Redis


def create_redis_connection(host: str, port: int) -> Redis:
    return Redis(host=host, port=port)
