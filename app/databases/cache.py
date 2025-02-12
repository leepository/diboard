import redis

from app.common.constants import AWS_SECRET_NAME
from app.utils.aws_utils import get_aws_secret_value

def get_redis_client():

    secret_value = get_aws_secret_value(secret_name=AWS_SECRET_NAME['CACHE'])
    host = secret_value['HOST']
    port = secret_value['PORT']
    password = secret_value['PASSWORD']

    print(f"host : {host}, port: {port}, password: {password}")

    redis_connection_pool = redis.ConnectionPool(
        host=host,
        port=port,
        db=0,
        password=password,
        decode_responses=True
    )

    redis_client = redis.Redis(connection_pool=redis_connection_pool)
    return redis_client
