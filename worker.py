import django
import os
import redis
import traceback

from rq import Worker, Queue, Connection

listen = ['high', 'default', 'low']

redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')

conn = redis.from_url(redis_url)

if __name__ == '__main__':
    django.setup()

    with Connection(conn):
        worker = Worker(map(Queue, listen))
        try:
            worker.work()
        except redis.exceptions.RedisError:
            traceback.print_exc
