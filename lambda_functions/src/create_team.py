import json
import boto3
import uuid

dynamodb = boto3.client('dynamodb')

def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])
        team_id = str(uuid.uuid4())

        dynamodb.put_item(
            TableName='Teams',
            Item={
                'id': {'S': team_id},
                'name': {'S': body['name']}
            }
        )

        return {
            "statusCode": 201,
            "body": json.dumps({"id": team_id, "name": body["name"]})
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }

