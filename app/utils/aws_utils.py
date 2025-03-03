import base64
import boto3
import orjson

from botocore.config import Config
from fastapi import File

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

def get_s3():
    s3 = boto3.resource(
        's3',
        endpoint_url="https://s3.ap-northeast-2.amazonaws.com",
        config=Config(signature_version='s3v4'),
        region_name=AWS_REGION
    )
    return s3, s3.meta.client

async def s3_upload_file(
        upload_file_obj: File,
        s3_bucket_name: str,
        s3_key: str
):
    """
    S3 file upload
    :param upload_file_obj:
    :param s3_bucket_name:
    :param s3_key:
    :return:
    """
    _, s3_client = get_s3()

    file_upload_result = False
    try:
        file_content = await upload_file_obj.read()
        s3_client.put_object(
            Bucket=s3_bucket_name,
            Key=s3_key,
            Body=file_content,
            ContentType=upload_file_obj.content_type
        )
        file_upload_result = True
    except Exception as ex:
        print("[EX] aws_util.s3_upload_file : ", str(ex.args))

    return file_upload_result

async def s3_read_file(s3_bucket_name: str, s3_key: str):
    """
    Read and return s3 object body
    :param s3_bucket_name:
    :param s3_key:
    :return:
    """
    s3, _ = get_s3()
    try:
        return s3.Object(bucket_name=s3_bucket_name, key=s3_key).get()['Body'].read()
    except Exception as ex:
        print("[EX] aws_utils.s3_read_file : ", str(ex.args))
        raise ex
