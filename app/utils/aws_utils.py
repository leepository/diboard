import base64
import boto3
import orjson

from app.common.constants import AWS_REGION

def get_aws_secret_value(secret_name: str):
    """
    Get secrets manager value
    :param secret_name:
    :return:
    """

    session = boto3.session.Session()
    client = session.client(
        service_name="secretsmanager",
        region_name=AWS_REGION
    )

    secret_string = None
    try:
        get_secret_value = client.get_secret_value(SecretId=secret_name)
        secret_string = get_secret_value['SecretString'] if "SecretString" in get_secret_value \
            else base64.b64decode(get_secret_value['SecretBinary'])
    except Exception as e:
        print("[EX] aws_utils.get_secret : ", str(e.args))

    try:
        secret_value = orjson.loads(secret_string) if secret_string is not None else None
    except:
        secret_value = secret_string

    return secret_value
