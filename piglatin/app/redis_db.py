import redis
from app.logger import logger


r = redis.Redis(host='cache', port=6379, decode_responses=True, password="eYVX7EwVmmxKPCDmwMtyKVge8oLd2t81")
logger.info("Connecting to redis for rate limite")
