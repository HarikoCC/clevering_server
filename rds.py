import redis
from const import Redis_addr, Redis_pass


class RedisSession:
    def __init__(self):
        self.rds = redis.Redis(host=Redis_addr, port=6379, db=0, password=Redis_pass)

    def __del__(self):
        self.rds.connection_pool.disconnect()
        self.rds.close()
        