from redis import Redis
from settings import config
import logging

redis = Redis(host=config.REDIS["host"],
              port=config.REDIS["port"],
              password=config.REDIS["pass"],
              db=config.REDIS["backend_db_name"])

redis.ping()

# print('connected to redis "{}"'.format(redis))
