import config
import hashlib
import boto3
hash_md5 = hashlib.md5()

# s3 = boto3.client(
#     's3',
#     aws_access_key_id=config.AWS_ID,
#     aws_secret_access_key=config.AWS_SECRET,
# )

def hash_function(value):
    hash_md5.update((value + config.SECRET_SALT).encode('utf-8'))
    return hash_md5.hexdigest()
