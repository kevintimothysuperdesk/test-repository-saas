import jwt
import json
from decouple import config
from psycopg2 import sql
from datetime import datetime, timedelta
from flask_cors import CORS
from flask import Flask, json, request, make_response
from slackeventsapi import SlackEventAdapter
import os
import dotenv
import threading
from validation import validation_function, validation_function_interactivity

dotenv.load_dotenv()

app = Flask(__name__)
CORS(app)

slack_events_adapter = SlackEventAdapter(
    os.getenv("SIGNING-SECRET-DEV"), "/poc/slack/events", app
)

@slack_events_adapter.on("message")
def slack_analysis(payload):
    print(payload, "payload in slack_analysis")
    def sample_function(payload):
        try:
            print(payload, "payload----")
            validation_function(payload)
        except Exception as e:
            print(str(e))
            return "An unknown error occurred"

    # Start a thread to process the payload
    threading.Thread(target=sample_function, args=(payload,)).start()

    # Return a 200 OK response immediately
    return make_response("OK", 200)

@app.route("/poc/slack/interactivity", methods=["POST"])
def handle_interactivity():
    payload = request.form.get("payload")
    print("payload in lambda_function for interaction: ", payload, type(payload))
    if payload:
        if isinstance(payload, str):
            payload = json.loads(payload)
        return validation_function_interactivity(payload)
    return make_response("Invalid payload", 400)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)