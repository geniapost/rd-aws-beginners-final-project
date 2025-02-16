import json
import boto3

dynamodb = boto3.client('dynamodb')

def lambda_handler(event, context):
    try:
        event_id = event['pathParameters']['id']
        body = json.loads(event['body'])

        update_expression = []
        expression_attribute_values = {}
        expression_attribute_names = {}

        if "hostTeamScore" in body:
            update_expression.append("hostTeamScore = :hostTeamScore")
            expression_attribute_values[":hostTeamScore"] = {"N": str(body["hostTeamScore"])}

        if "guestTeamScore" in body:
            update_expression.append("guestTeamScore = :guestTeamScore")
            expression_attribute_values[":guestTeamScore"] = {"N": str(body["guestTeamScore"])}

        if "status" in body:
            expression_attribute_names["#status"] = "status"
            update_expression.append("#status = :status")
            expression_attribute_values[":status"] = {"S": body["status"]}

        if not update_expression:
            return {"statusCode": 400, "body": json.dumps({"error": "No valid fields to update"})}

        if expression_attribute_names:
            dynamodb.update_item(
                TableName='Events',
                Key={'id': {'S': event_id}},
                UpdateExpression="SET " + ", ".join(update_expression),
                ExpressionAttributeValues=expression_attribute_values,
                ExpressionAttributeNames=expression_attribute_names  # Псевдонимы для зарезервированных слов
            )
        else:
            dynamodb.update_item(
                TableName='Events',
                Key={'id': {'S': event_id}},
                UpdateExpression="SET " + ", ".join(update_expression),
                ExpressionAttributeValues=expression_attribute_values
            )

        return {"statusCode": 200, "body": json.dumps({"id": event_id})}
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}
