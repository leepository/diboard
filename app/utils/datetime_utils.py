from datetime import datetime

def dt2ts(dt: datetime) -> int:
    """
    datetime format을 timestamp(milliseconds) 타입으로 변환
    """
    return int(dt.timestamp() * 1000)

def strf_timezone(dt):
    return dt.strftime('%Y-%m-%dT%H:%M:%S+00:00') if dt is not None else None
