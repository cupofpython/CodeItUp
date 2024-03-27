from flask import Flask, request, jsonify
from slack import WebClient
import os
import requests
import threading

app = Flask(__name__)
slack_token = os.environ["SLACK_BOT_TOKEN"]
client = WebClient(token=slack_token)
channel = "making-a-bot"

@app.route("/generate", methods=["POST"])
def generate():
    # Extract parameters from the slash command
    command_text = request.form.get('text')

    t = threading.Thread(target=generate_code, args=(request.form, command_text,))
    t.start()

    # Process the command and generate a response
    response_text = f'Generating code... please wait!'

    # Respond to Slack
    return jsonify({'response_type': 'in_channel', 'text': response_text})

def generate_code(request, command_text):
    # Get parameters from the command text
    parameters = parse_parameters(command_text)
    print(parameters)

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

    # Send POST request to code suggestions API
    response = requests.post(url, headers=headers, json=data)

    print(response)

    # Respond to Slack
    message = {
        "text": "Here is your code!" + response.json()['choices'][0]['text']
    }
    res = requests.post(request["response_url"], json=message)

def parse_parameters(input_string):
    parameters = {}
    
    print(input_string)
    inputs = input_string.split("; ")

    for i in inputs:
        key_val = i.split(": ")
        parameters[key_val[0]] = key_val[1]
    
    return parameters

if __name__ == "__main__":
    app.run(port=5000)