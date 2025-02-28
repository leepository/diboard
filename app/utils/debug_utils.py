import ujson

from datetime import datetime, timedelta
from typing import List

from app.utils.common_utils import encode_json

def dpp(s, v = None, t = None):
    """
    Debug용 print
    :param s:
    :param v: value
    """

    t = f"[{(datetime.utcnow() + timedelta(hours=9)).strftime('%Y-%m-%d %H:%M:%S')}]" if t is True else ""

    if isinstance(s, str):
        if v is None:
            print(f"{t} {s}")
        else:
            if isinstance(v, dict):
                encoded_v = encode_json(v)
                print(f"[Dict] {s}", ujson.dumps(encoded_v, sort_keys=True, indent=4))
            elif isinstance(v, List):
                print(f"[List] {s}")
                for itm in v:
                    if isinstance(itm, dict):
                        encoded_itm = encode_json(itm)
                        print(ujson.dumps(encoded_itm, sort_keys=True, indent=4))
                    else:
                        print(str(itm))
            else:
                print(s, v)
    if isinstance(s, dict):
        print("[Dict]")
        encoded_s = encode_json(s)
        print(ujson.dumps(encoded_s, sort_keys=True, indent=4))

    if isinstance(s, List):
        print("[List]")
        for itm in s:
            if isinstance(itm, dict):
                encoded_itm = encode_json(itm)
                print(ujson.dumps(encoded_itm, sort_keys=True, indent=4))
            else:
                print(str(itm))
