import json
import base64
import urllib.parse
import boto3

def lambda_handler(event, context):
    # Trigger generateCode lambda
    lambda_client = boto3.client('lambda')
    response = lambda_client.invoke(
        FunctionName='generateCode',
        InvocationType='Event',  # Set to 'Event' for asynchronous invocation
        Payload=json.dumps(event)
    )
    
    # Send response back to slack
    return {
        'statusCode': 200,
        'body': 'Generating code, please wait!'
    }