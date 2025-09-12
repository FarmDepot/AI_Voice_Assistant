FarmDepot.ng AI Voice Assistant - Project Setup Guide
This guide contains all the steps to set up and deploy the AI Voice Assistant for FarmDepot.ng. Please follow each step carefully.
Project Structure:
/
├── backend/
│   ├── app.py              # The Flask server
│   ├── requirements.txt    # Python dependencies
│   └── .env.example        # Environment variable template
└── frontend/
    └── farmdepot-ai-widget.html # The complete frontend widget


Part 1: Google Cloud & Dialogflow Setup (Crucial Step)
This AI is powered by Google Dialogflow. You must configure it correctly for the assistant to understand commands.
Step 1.1: Create a Google Cloud Project
Go to the Google Cloud Console.
Create a new project (e.g., "FarmDepot-AI").
Make sure billing is enabled for the project.
Step 1.2: Enable the Dialogflow API
In your Google Cloud project, go to "APIs & Services" > "Library".
Search for "Dialogflow API" and click Enable.
Step 1.3: Create a Service Account This is required for the Flask backend to securely authenticate with Dialogflow.
Go to "IAM & Admin" > "Service Accounts".
Click "+ CREATE SERVICE ACCOUNT".
Give it a name (e.g., "farmdepot-dialogflow-agent").
Grant it the "Dialogflow API Admin" role.
Click "Done".
Find the newly created service account, click the three dots under "Actions", and select "Manage keys".
Click "ADD KEY" > "Create new key". Choose JSON and click "Create".
A JSON file will be downloaded. This file is your key. Keep it secure. Rename it to google-credentials.json and place it inside the backend/ folder.
Step 1.4: Create a Dialogflow Agent
Go to the Dialogflow ES Console.
Create a new agent. Name it "FarmDepotAssistant".
Select your Google Cloud Project from the dropdown.
Set the default language to English (en) and the timezone to your local one.
Click "Create".
Step 1.5: Configure Dialogflow Intents This is where you teach the AI what to do. You need to create an intent for each action.
Go to "Intents" in the left menu.
Delete the default intents if you wish.
Click "CREATE INTENT" and create the following intents one by one:
Intent Name: Maps.listings
Training Phrases (add these):
Search for listings
Show me the products
I want to buy something
Find agricultural products
Action: Maps
Responses > Text Response: Navigating to the listings page.
Fulfillment > Set this intent as end of conversation.
SAVE
Intent Name: Maps.post_ad
Training Phrases:
I want to post an ad
Sell my products
Create a new listing
Action: Maps.form
Responses > Text Response: Okay, let's create a new ad for you. I will now take you to the listing form.
SAVE
Intent Name: Maps.my_account
Training Phrases:
Open my account
Show me my profile
Go to my account
Action: Maps
Responses > Text Response: Opening your account page.
SAVE
Intent Name: search.product
Training Phrases:
Search for tractors (highlight "tractors" and assign it the @sys.any entity type, name it product_name)
Find me some maize (highlight "maize", assign @sys.any, name it product_name)
I need fertilizer (highlight "fertilizer", assign @sys.any, name it product_name)
Action: search
Parameters: Ensure a parameter named product_name of type @sys.any is created.
Responses > Text Response: Searching for $product_name for you.
SAVE
Intent Name: Default Fallback Intent (This one already exists, just edit it)
Responses > Text Response: Add these:
I'm sorry, I didn't understand. Can you please rephrase?
I'm not sure how to help with that. I can help you search for products or navigate the site.
SAVE
IMPORTANT: For every Maps intent, you must add the corresponding URL. In Dialogflow, go to the "Responses" section of each intent. Click "ADD RESPONSE" -> "Custom Payload" and add this JSON, changing the URL for each intent:
{
  "url": "[https://farmdepot.ng/listings/](https://farmdepot.ng/listings/)"
}


For Maps.my_account, the URL would be https://farmdepot.ng/my-account/.
For Maps.post_ad, it would be https://farmdepot.ng/listing-form/.
After creating all intents, wait for the agent to finish training (a notification will pop up).
Part 2: Backend Setup (Flask)
Navigate to the backend directory.
Create a Python virtual environment:
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate


Install dependencies:
pip install -r requirements.txt


Configure Environment Variables:
Rename .env.example to .env.
Open the .env file and fill in your Google Cloud Project ID.
Make sure the google-credentials.json file you downloaded is in this backend directory.
Run the Flask server:
flask run
The server should now be running on http://127.0.0.1:5000.
Part 3: Frontend Setup (AI Widget)
The frontend is a single, self-contained HTML file.
Open frontend/farmdepot-ai-widget.html in your browser. You can open it directly as a file to test it.
Click the microphone icon at the bottom right.
Allow the browser to use your microphone.
Start speaking commands like "show me the products" or "search for tractors".
To install on your WordPress site:
You can use a plugin like "Insert Headers and Footers".
Copy the entire content of farmdepot-ai-widget.html.
Paste the code into the "Scripts in Footer" section of the plugin.
Save, and the AI widget will appear on your website.
Your AI assistant is now ready to be tested!
