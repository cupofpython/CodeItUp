import json
import base64
import urllib.parse
import requests

def lambda_handler(event, context):
    # Parse the incoming Slack slash command payload
    event_body_base64 = event['body']
    event_body_bytes = base64.b64decode(event_body_base64)
    event_body = event_body_bytes.decode('utf-8')
    event_body = event_body.split('&')
    payload = {}
    for pair in event_body:
       k, v = pair.split('=')
       payload[k] = urllib.parse.unquote(v).replace('+', ' ')
    
    # Extract relevant information from the payload
    command = payload['command']
    text = payload['text']
    response_url = payload['response_url']
    
    generate_code(response_url, text)


def generate_code(response_url, command_text):
    # Get parameters from the command text
    parameters = parse_parameters(command_text)

    file_name = parameters["file"]
    prompt = "# " + parameters["prompt"]
    #gl_project = parameters["project"]
    token = parameters["token"]
    
    # API call setup
    url = "https://gitlab.com/api/v4/code_suggestions/completions"
    headers = {
    'Authorization': 'Bearer ' + token
    }
    data = {
      "current_file": {
        "file_name": file_name,
        "content_above_cursor": prompt,
        "content_below_cursor": ""
      },
      "intent": "generation"
    }
    
    response = requests.post(url, headers=headers, json=data)

    # Respond to Slack
    message = {
        "text": "Here is your code!" + response.json()['choices'][0]['text']
    }
    
    requests.post(response_url, json=message)
    

def parse_parameters(input_string):
    parameters = {}
    
    inputs = input_string.split("; ")

    for i in inputs:
        key_val = i.split(": ")
        parameters[key_val[0]] = key_val[1]
    
    return parameters