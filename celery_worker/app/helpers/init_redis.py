from redis import Redis
from settings import config


def is_backend_running() -> bool:
    try:
        conn = Redis(
            host=config.REDIS["host"],
            port=config.REDIS["port"],
            db=config.REDIS["backend_db_name"],
            password=config.REDIS["pass"]
        )
        conn.client_list()
    except Exception as e:
        print(f"Failed to connect to Redis instance at {config.REDIS_backend}")
        print(repr(e))
        return False
    conn.close()
    return True
