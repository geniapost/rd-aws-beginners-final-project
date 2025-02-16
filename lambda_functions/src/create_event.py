import json
import boto3
import uuid

dynamodb = boto3.client('dynamodb')

def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])
        event_id = str(uuid.uuid4())

        host_team = dynamodb.get_item(TableName='Teams', Key={'id': {'S': body['hostTeamId']}})
        guest_team = dynamodb.get_item(TableName='Teams', Key={'id': {'S': body['guestTeamId']}})

        if 'Item' not in host_team or 'Item' not in guest_team:
            return {"statusCode": 400, "body": json.dumps({"error": "Invalid team IDs"})}

        event = {
            'id': {'S': event_id},
            'hostTeam': {'S': body['hostTeamId']},
            'guestTeam': {'S': body['guestTeamId']},
            'hostTeamScore': {'N': str(body.get('hostTeamScore', 0))},
            'guestTeamScore': {'N': str(body.get('guestTeamScore', 0))},
            'status': {'S': body.get('status', 'waiting')}
        }

        dynamodb.put_item(TableName='Events', Item=event)

        return {"statusCode": 201, "body": json.dumps(event)}
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}

