import json
import boto3

dynamodb = boto3.client('dynamodb')

def lambda_handler(event, context):
    try:
        event_id = event['pathParameters']['id']
        response = dynamodb.get_item(TableName='Events', Key={'id': {'S': event_id}})

        if 'Item' not in response:
            return {"statusCode": 404, "body": json.dumps({"error": "Event not found"})}

        event_data = response['Item']
        return {"statusCode": 200, "body": json.dumps(event_data)}
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}

