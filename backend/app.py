import os
from flask import Flask, request, jsonify
from google.cloud import dialogflow_v2 as dialogflow
from dotenv import load_dotenv
from flask_cors import CORS # Import the CORS library

load_dotenv()

app = Flask(__name__)
# *** FIX IS HERE ***
# This line enables CORS for all routes on your server, allowing
# your website at farmdepot.ng to communicate with it.
CORS(app)

# --- Dialogflow Configuration ---
# You must have the GOOGLE_APPLICATION_CREDENTIALS environment variable
# set to the path of your JSON key file.
# See the README for instructions.
PROJECT_ID = os.getenv('DIALOGFLOW_PROJECT_ID')
if not PROJECT_ID:
    raise ValueError("DIALOGFLOW_PROJECT_ID environment variable not set.")

session_client = dialogflow.SessionsClient()

@app.route("/")
def index():
    return "<h1>FarmDepot AI Backend is running.</h1>"

@app.route('/detect-intent', methods=['POST'])
def detect_intent():
    """Receives text from the frontend and gets a response from Dialogflow."""
    data = request.get_json()
    if not data or 'text' not in data or 'sessionId' not in data:
        return jsonify({'error': 'Invalid request. "text" and "sessionId" are required.'}), 400

    text_input = data['text']
    session_id = data['sessionId']
    session_path = session_client.session_path(PROJECT_ID, session_id)

    text_input_dialogflow = dialogflow.TextInput(text=text_input, language_code='en-US')
    query_input = dialogflow.QueryInput(text=text_input_dialogflow)

    try:
        response = session_client.detect_intent(request={'session': session_path, 'query_input': query_input})
        query_result = response.query_result

        # Extract relevant information
        fulfillment_text = query_result.fulfillment_text
        action = query_result.action
        
        # Extract parameters
        parameters = {key: value for key, value in query_result.parameters.items()}

        # Extract custom payloads for more complex actions like navigation
        custom_payload = {}
        if query_result.fulfillment_messages:
            for message in query_result.fulfillment_messages:
                if message.payload:
                    payload_fields = message.payload.fields
                    custom_payload = {key: field.string_value for key, field in payload_fields.items()}
        
        return jsonify({
            'fulfillmentText': fulfillment_text,
            'action': action,
            'parameters': parameters,
            'customPayload': custom_payload
        })

    except Exception as e:
        print(f"Error detecting intent: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

