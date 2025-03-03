import os
import time
import uuid

from datetime import datetime
from decimal import Decimal
from enum import Enum
from sqlalchemy.orm.state import InstanceState

from app.utils.datetime_utils import strf_timezone

def get_ttl_hash(seconds=86400):
    """
    Return the same value within 'seconds' time period
    :param seconds: default 24hours
    :return:
    """
    return round(time.time() / seconds)

def get_uuid():
    """
    UUID 생성
    :return:
    """
    return str(uuid.uuid4())

def get_api_env():
    return os.getenv("API_ENV", "DEV")

def encode_json(o):
    """객체들을 json 호환 가능한 형태로 변경한다."""
    if isinstance(o, dict):
        return dict(map(lambda x: (x[0], encode_json(x[1])), o.items()))
    if isinstance(o, list):
        return [encode_json(data) for data in o]
    if isinstance(o, Decimal):
        return str(o)
    if isinstance(o, datetime):
        return strf_timezone(o)
    if isinstance(o, tuple):
        return tuple([encode_json(data) for data in o])
    if isinstance(o, set):
        return set([encode_json(data) for data in o])
    if isinstance(o, Enum):
        return o.value
    if isinstance(o, InstanceState):
        return None
    return o
