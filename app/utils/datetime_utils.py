from datetime import datetime

def dt2ts(dt: datetime) -> int:
    """
    datetime format을 timestamp(milliseconds) 타입으로 변환
    """
    return int(dt.timestamp() * 1000)
