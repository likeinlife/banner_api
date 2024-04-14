import dramatiq
from dramatiq.brokers.redis import RedisBroker


def configure_dramatiq(host: str, port: int):
    broker = RedisBroker(host=host, port=port)
    dramatiq.set_broker(broker)
