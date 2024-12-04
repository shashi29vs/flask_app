from flask import Flask, jsonify, request
import requests
import logging
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests (required for Tableau)
logging.basicConfig(level=logging.INFO)

# Static API URL
API_URL = "https://www.sogolytics.com/serviceAPI/service/GetDataTranspose"


@app.route("/odata/DynamicEntities", methods=["GET"])
def get_dynamic_entities():
    """
    Fetch data dynamically using token and intsurveyno from query parameters.
    """
    try:
        # Get 'token' and 'intsurveyno' from query parameters
        token = request.args.get("token")
        intsurveyno = request.args.get("intsurveyno")

        if not token or not intsurveyno:
            return jsonify({"error": "Both 'token' and 'intsurveyno' are required"}), 400

        # Dynamic payload
        payload = {
            "token": token,
            "intsurveyno": intsurveyno,
            "ParticipationStatus": 3,
            "LastUpdate": "",
            "isincludeincompleteresponses": "true",
            "getassigncodes": "false",
            "intstartno": "1",
            "intendno": "0"
        }

        # Fetch data from the API
        logging.info(f"Fetching data for token={token} and intsurveyno={intsurveyno}")
        response = requests.post(API_URL, json=payload)
        if response.status_code != 200:
            logging.error(f"API request failed with status code {response.status_code}: {response.text}")
            return jsonify({"error": f"API request failed with status code {response.status_code}"}), response.status_code

        data = response.json()
        records = data.get("Data", [])

        # Add the @odata.context key
        odata_response = {
            "@odata.context": f"{request.url_root}odata/$metadata#DynamicEntities",
            "value": records
        }

        return jsonify(odata_response)  # Return OData-compliant JSON
    except Exception as e:
        logging.error(f"Error fetching dynamic entities: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/odata/$metadata", methods=["GET"])
def get_metadata():
    """
    Dynamically generate OData metadata based on the API response.
    """
    metadata_template = """<?xml version="1.0" encoding="utf-8"?>
    <edmx:Edmx Version="4.0" xmlns:edmx="http://docs.oasis-open.org/odata/ns/edmx">
      <edmx:DataServices>
        <Schema Namespace="DynamicOData" xmlns="http://docs.oasis-open.org/odata/ns/edm">
          <EntityType Name="DynamicEntity">
            {fields}
          </EntityType>
          <EntityContainer Name="Container">
            <EntitySet Name="DynamicEntities" EntityType="DynamicOData.DynamicEntity"/>
          </EntityContainer>
        </Schema>
      </edmx:DataServices>
    </edmx:Edmx>"""

    try:
        # Static payload for metadata sampling
        sample_payload = {
            "token": "f5439ee9-2a4e-4bec-b345-aa3a240cf3f8",  # Replace with any valid token for sampling
            "intsurveyno": "4",  # Replace with any valid survey number for sampling
            "ParticipationStatus": 3,
            "LastUpdate": "",
            "isincludeincompleteresponses": "true",
            "getassigncodes": "false",
            "intstartno": "1",
            "intendno": "1"  # Fetch only one record for metadata
        }

        # Fetch a sample response to determine dynamic schema
        logging.info("Fetching metadata sample response...")
        response = requests.post(API_URL, json=sample_payload)
        if response.status_code != 200:
            logging.error(f"API request for metadata failed with status code {response.status_code}: {response.text}")
            return jsonify({"error": f"API request failed with status code {response.status_code}"}), response.status_code

        sample_data = response.json().get("Data", [])[0]

        # Determine data types dynamically (all fields are treated as Edm.String for simplicity)
        fields = "\n".join([f'<Property Name="{key}" Type="Edm.String"/>' for key in sample_data.keys()])

        # Generate metadata using the dynamic fields
        metadata = metadata_template.format(fields=fields)
        return metadata, 200, {"Content-Type": "application/xml"}
    except Exception as e:
        logging.error(f"Error fetching metadata: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000)
