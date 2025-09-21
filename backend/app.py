import os
from flask import Flask, request, jsonify
from google.cloud import dialogflow_v2 as dialogflow
from dotenv import load_dotenv
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)
CORS(app)

PROJECT_ID = os.getenv('DIALOGFLOW_PROJECT_ID')
if not PROJECT_ID:
    raise ValueError("DIALOGFLOW_PROJECT_ID environment variable not set.")

session_client = dialogflow.SessionsClient()

@app.route("/")
def index():
    return "<h1>FarmDepot AI Backend is running.</h1>"

@app.route('/detect-intent', methods=['POST'])
def detect_intent():
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

        fulfillment_text = query_result.fulfillment_text
        action = query_result.action
        parameters = {key: value for key, value in query_result.parameters.items()}
        
        custom_payload = {}
        if query_result.fulfillment_messages:
            for message in query_result.fulfillment_messages:
                # *** THE FIX IS HERE ***
                # This correctly handles the modern payload structure from Dialogflow
                # by treating the payload object like a dictionary.
                if message.payload:
                    custom_payload = {key: value.string_value for key, value in message.payload.items()}
                    # We only need to find the first payload.
                    if custom_payload:
                        break
        
        return jsonify({
            'fulfillmentText': fulfillment_text,
            'action': action,
            'parameters': parameters,
            'customPayload': custom_payload
        })

    except Exception as e:
        # This will now log the specific error to Render for debugging.
        print(f"Error detecting intent: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)


        
