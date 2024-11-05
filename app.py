from flask import Flask, request, jsonify
from flask_cors import CORS;
import requests
import re

app = Flask(__name__)
allowed_origins = ["http://localhost:5173"]
# CORS(app, resources={r"/api/*": {"origins": allowed_origins}})
# CORS(app)  # Update to match your frontend's origin
CORS(app, resources={r"/api/*": {"origins": re.compile(r"^https?://(localhost:5173|your-production-domain\.com)(:\d+)?$")}})


# Your Coresignal API URL and headers
CORESIGNAL_URL = "https://api.coresignal.com/enrichment/companies"
HEADERS = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer eyJhbGciOiJFZERTQSIsImtpZCI6IjA0OTUxNzgxLTQ0ZDYtMWViOC0zNjk2LTA4NjBiMDUzZjFkMyJ9.eyJhdWQiOiJpZXRkYXZ2LmVkdS5pbiIsImV4cCI6MTc2MjM1ODY3OCwiaWF0IjoxNzMwODAxNzI2LCJpc3MiOiJodHRwczovL29wcy5jb3Jlc2lnbmFsLmNvbTo4MzAwL3YxL2lkZW50aXR5L29pZGMiLCJuYW1lc3BhY2UiOiJyb290IiwicHJlZmVycmVkX3VzZXJuYW1lIjoiaWV0ZGF2di5lZHUuaW4iLCJzdWIiOiJmYTBjNGM5Yy1jMjFjLWZmZGYtYzBiOS00OGFlZDVhZjljMTYiLCJ1c2VyaW5mbyI6eyJzY29wZXMiOiJjZGFwaSJ9fQ.6NEfsLKxDXchrHoDKw63snWDRIjswsiyJ6uBLpKvAhFzWtoS54dePD77PBJPtK-kblZhslIJC_-dfqyenlCcDw'  # Replace with your actual token
}

@app.route('/')
def index():
    return 'Hello, World!'

@app.route('/api/enrich', methods=['POST'])

def enrich_company_data():
    data = request.json
    website = data.get('website')

    # Validate input
    if not website:
        return jsonify({"error": "Website is required."}), 400

    # Call the Coresignal API using GET
    try:
        response = requests.get(f"{CORESIGNAL_URL}?website={website}&lookalikes=true", headers=HEADERS)
        
        if response.status_code != 200:
            return jsonify({"error": response.json().get("message", "Failed to retrieve data")}), response.status_code

        # Return the enriched data to the frontend
        return jsonify(response.json())

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
