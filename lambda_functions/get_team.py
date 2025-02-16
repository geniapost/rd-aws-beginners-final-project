import json
import boto3

dynamodb = boto3.client('dynamodb')

def lambda_handler(event, context):
    try:
        team_id = event['pathParameters']['id']
        response = dynamodb.get_item(
            TableName='Teams',
            Key={'id': {'S': team_id}}
        )

        if 'Item' not in response:
            return {"statusCode": 404, "body": json.dumps({"error": "Team not found"})}

        team = {
            "id": response['Item']['id']['S'],
            "name": response['Item']['name']['S']
        }

        return {"statusCode": 200, "body": json.dumps(team)}
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}

