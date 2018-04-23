import config
import hashlib
import boto3
import base64
hash_md5 = hashlib.md5()

# s3 = boto3.client(
#     's3',
#     aws_access_key_id=config.AWS_ID,
#     aws_secret_access_key=config.AWS_SECRET,
# )


def hash_function(value):
    hash_md5.update((value + config.SECRET_SALT).encode('utf-8'))
    return hash_md5.hexdigest()


def from_global_id(global_id):
    '''
    Takes the "global ID" created by toGlobalID, and retuns the type name and ID
    used to create it.
    '''
    unbased_global_id = base64.b64decode(global_id).decode('utf-8')
    _type, _id = unbased_global_id.split(':', 1)
    return int(_id)
