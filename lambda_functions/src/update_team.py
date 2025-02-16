import json
import boto3

dynamodb = boto3.client('dynamodb')

def lambda_handler(event, context):
    try:
        team_id = event['pathParameters']['id']
        body = json.loads(event['body'])

        dynamodb.update_item(
            TableName='Teams',
            Key={'id': {'S': team_id}},
            UpdateExpression="SET #n = :name",
            ExpressionAttributeNames={"#n": "name"},
            ExpressionAttributeValues={":name": {"S": body["name"]}}
        )

        return {"statusCode": 200, "body": json.dumps({"id": team_id, "name": body["name"]})}
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}

