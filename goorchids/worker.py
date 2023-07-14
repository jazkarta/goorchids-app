import django
import os
import logging
import redis

from rq import Worker, Queue, Connection

logger = logging.getLogger(__name__)
listen = ['high', 'default', 'low']

redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')

conn = redis.from_url(redis_url)

if __name__ == '__main__':
    django.setup()

    with Connection(conn):
        worker = Worker(map(Queue, listen))
        try:
            worker.work()
        except redis.exceptions.RedisError:
            logger.exception('Error connecting to redis')
            pass
