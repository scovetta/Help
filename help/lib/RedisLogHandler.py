import redis
import logging

class RedisLogHandler:
    """
    Log handler, that logs data into a Redis list for later bulk writing to disk.
    """
    def __init__(self, host='localhost', port=3796, db=0, redis_key='log', backup_log_handler=None):
        self.formatter = logging.Formatter()
        self.redis = redis.StrictRedis(host=host, port=port)
        self.redis_key = redis_key
        self.log_level = logging.DEBUG
        self.backup_log_handler = backup_log_handler
    
    def handle(self, record):
        try:
            self.redis.lpush(self.redis_key, self.formatter.format(record))
        except:
            try:
                # Try the backup handler, in case Redis is down or something
                backup_log_handler.handle(record)
            except:
                # Nothing works, sadness
                pass
            
    def setFormatter(self, formatter):
        self.formatter = formatter
    
    @property
    def level(self):
        return self.log_level
    
    def setLevel(self, value):
        self.log_level = value
