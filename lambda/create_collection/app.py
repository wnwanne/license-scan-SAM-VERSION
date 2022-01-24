import os
import uuid
import boto3
from crhelper import CfnResource

helper = CfnResource(log_level='WARNING', boto_level='WARNING')
client = boto3.client('rekognition')

def lambda_handler(event, context) -> None:
    """
    Entry point
    :param event: Event body from CloudFormation
    :param context: Context of Lambda runtime
    :return: None
    """
    helper(event, context)

@helper.create
def create(event, context) -> None:
    """
    Run seeding lambda
    :param event: Event body from CloudFormation
    :param context: Context of Lambda runtime
    """
    collection_id = os.environ["STACKPREFIX"] + "-" + str(uuid.uuid1())
    print(f"Create REK Collection {collection_id}")
    response = client.create_collection(CollectionId=collection_id)
    
    return collection_id

@helper.delete
def delete(event, context) -> None:
    print(f"Delete REK Collection {collection_id}")
    response = client.delete_collection(CollectionId=event['PhysicalResourceId'])
