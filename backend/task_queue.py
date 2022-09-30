from redis import Redis
from rq import Queue

redis_connection = Redis()
build_task_queue = Queue(connection=redis_connection)
execution_task_queue = Queue(connection=redis_connection)
