import os
import uuid
from google.cloud import dialogflow_v2 as dialogflow
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- Configuration ---
# Set the path to your service account key file
# Ensure this file is in your backend directory and named correctly.
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "google-credentials.json"

# Get project ID from environment variables
DIALOGFLOW_PROJECT_ID = os.getenv("DIALOGFLOW_PROJECT_ID")
if not DIALOGFLOW_PROJECT_ID:
    raise ValueError("DIALOGFLOW_PROJECT_ID environment variable not set.")

# Set a default language code
DIALOGFLOW_LANGUAGE_CODE = "en"

# --- Flask App Initialization ---
app = Flask(__name__)
# Enable CORS to allow requests from your website
CORS(app)

# --- Dialogflow Client Initialization ---
# We create one session client and reuse it for efficiency.
session_client = dialogflow.SessionsClient()

@app.route("/")
def index():
    """A simple route to check if the server is running."""
    return "FarmDepot AI Backend is running."

@app.route('/detect-intent', methods=['POST'])
def detect_intent():
    """
    Receives a text query from the frontend and passes it to Dialogflow.
    Returns a structured response from Dialogflow.
    """
    data = request.get_json()
    
    if not data or 'text' not in data:
        return jsonify({"error": "Invalid request. 'text' field is required."}), 400
        
    query_text = data['text']
    # Use a unique session ID for each user. Here we use a random UUID for simplicity.
    # In a real app, you might manage this session ID more carefully.
    session_id = data.get('sessionId', str(uuid.uuid4()))
    
    session = session_client.session_path(DIALOGFLOW_PROJECT_ID, session_id)
    
    text_input = dialogflow.TextInput(text=query_text, language_code=DIALOGFLOW_LANGUAGE_CODE)
    query_input = dialogflow.QueryInput(text=text_input)
    
    try:
        response = session_client.detect_intent(request={"session": session, "query_input": query_input})
    except Exception as e:
        print(f"Error calling Dialogflow API: {e}")
        return jsonify({"error": f"Failed to connect to Dialogflow: {e}"}), 500

    # --- Parse Dialogflow's Response ---
    query_result = response.query_result
    
    # Extract key information
    intent = query_result.intent.display_name
    action = query_result.action
    fulfillment_text = query_result.fulfillment_text
    
    # Extract parameters (entities)
    parameters = {}
    for key, value in query_result.parameters.items():
        parameters[key] = value

    # Extract custom payload (for URLs, etc.)
    custom_payload = {}
    if query_result.fulfillment_messages:
        for message in query_result.fulfillment_messages:
            if message.payload:
                fields = message.payload.fields
                for key, value in fields.items():
                    # Handle different value types from Dialogflow's Struct
                    if value.HasField('string_value'):
                        custom_payload[key] = value.string_value
                    elif value.HasField('number_value'):
                        custom_payload[key] = value.number_value
                    elif value.HasField('bool_value'):
                        custom_payload[key] = value.bool_value

    # --- Construct the JSON response for the frontend ---
    result = {
        "intent": intent,
        "action": action,
        "parameters": parameters,
        "fulfillmentText": fulfillment_text,
        "customPayload": custom_payload,
        "sessionId": session_id
    }

    return jsonify(result)

if __name__ == '__main__':
    # Use a default port of 5000, which is standard for Flask.
    app.run(debug=True, port=5000)

