import time

def get_ttl_hash(seconds=86400):
    """
    Return the same value within 'seconds' time period
    :param seconds: default 24hours
    :return:
    """
    return round(time.time() / seconds)
