import os
import boto3

def lambda_handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    pho_path = event['Records'][0]['s3']['object']['key']
    pic_id = pho_path.split('/')[1]

    # add collection ID
    col_id = os.environ["REK_COLLECTION_ID"]

    # add DynamoDB table name
    table_name = os.environ["DDB_TABLE_NAME"]

    index_faces(bucket=bucket, photo=pho_path, pic_id=pic_id, collection_id=col_id, table_name=table_name)


def index_faces(bucket, photo, pic_id, collection_id, table_name):
    client = boto3.client('rekognition')

    print(f"Process {bucket} file {photo}")
    print(f"Collection ID {collection_id} Pic ID {pic_id}")

    col_resp = client.index_faces(CollectionId=collection_id,
                                  Image={'S3Object': {'Bucket': bucket, 'Name': photo}},
                                  ExternalImageId=pic_id,
                                  MaxFaces=1,
                                  QualityFilter="AUTO",
                                  DetectionAttributes=['ALL'])

    # Parse features from response
    age_low = col_resp['FaceRecords'][0]['FaceDetail']['AgeRange']['Low']
    age_high = col_resp['FaceRecords'][0]['FaceDetail']['AgeRange']['High']
    response_Smile = col_resp['FaceRecords'][0]['FaceDetail']['Smile']['Value']
    response_Eyeglasses = col_resp['FaceRecords'][0]['FaceDetail']['Eyeglasses']['Value']
    response_Sunglasses = col_resp['FaceRecords'][0]['FaceDetail']['Sunglasses']['Value']
    response_Gender = col_resp['FaceRecords'][0]['FaceDetail']['Gender']['Value']
    response_Beard = col_resp['FaceRecords'][0]['FaceDetail']['Beard']['Value']
    response_Mustache = col_resp['FaceRecords'][0]['FaceDetail']['Mustache']['Value']
    response_EyesOpen = col_resp['FaceRecords'][0]['FaceDetail']['EyesOpen']['Value']
    response_MouthOpen = col_resp['FaceRecords'][0]['FaceDetail']['MouthOpen']['Value']
    response_Emotions = col_resp['FaceRecords'][0]['FaceDetail']['Emotions']
    face_id = col_resp['FaceRecords'][0]['Face']['FaceId']

    emo_dict = {}
    for resp in response_Emotions:
        emo_type = resp['Type']
        emo_conf = resp['Confidence']
        emo_dict[emo_type] = emo_conf

    emotion = max(emo_dict, key=emo_dict.get)

    put_stats(table_name=table_name, pic_name=pic_id, age_low=age_low, age_high=age_high, response_Smile=response_Smile,
              response_Eyeglasses=response_Eyeglasses, response_Sunglasses=response_Sunglasses,
              response_Gender=response_Gender, response_Beard=response_Beard,
              response_Mustache=response_Mustache,
              response_EyesOpen=response_EyesOpen, response_MouthOpen=response_MouthOpen, emotion=emotion,
              face_id=face_id)


def put_stats(table_name, pic_name, age_low, age_high, response_Smile,
              response_Eyeglasses, response_Sunglasses,
              response_Gender, response_Beard, response_Mustache,
              response_EyesOpen, response_MouthOpen, emotion, face_id, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table(table_name)
    response = table.put_item(
        Item={
            'pic_id': pic_name,
            'age_low': age_low,
            'age_high': age_high,
            'response_Smile': response_Smile,
            'response_Eyeglasses': response_Eyeglasses,
            'response_Sunglasses': response_Sunglasses,
            'response_Gender': response_Gender,
            'response_Beard': response_Beard,
            'response_Mustache': response_Mustache,
            'response_EyesOpen': response_EyesOpen,
            'response_MouthOpen': response_MouthOpen,
            'emotion': emotion,
            'face_id': face_id
        }
    )
    return response

