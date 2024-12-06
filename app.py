from flask import Flask, jsonify, Response
import pandas as pd

# Sample JSON data
json_data = [
    {
        "EmailID": "Public Access",
        "EndTime": "10/31/2024 10:43 AM",
        "IPAddress": "103.74.16.54",
        "LastUpdate": "2024-10-31T01:13:04.123",
        "ParticipationStatus": "Completed",
        "Q1_Please_rate_your_level_of_agreement_with_this_statement_Companyproductservicebrand_made_it_easy_for_me_to_meet_my_needs": "5 - Somewhat Agree",
        "Q2_How_likely_is_it_that_you_would_recommend_company__product__service__brand_to_a_friend_or_colleague": "6",
        "ResponseNum": 1,
        "SrNO": 1,
        "StartTime": "10/31/2024 10:43 AM"
    },
    {
        "EmailID": "Public Access",
        "EndTime": "10/31/2024 10:43 AM",
        "IPAddress": "103.74.16.54",
        "LastUpdate": "2024-10-31T01:13:09.183",
        "ParticipationStatus": "Completed",
        "Q1_Please_rate_your_level_of_agreement_with_this_statement_Companyproductservicebrand_made_it_easy_for_me_to_meet_my_needs": "4 - Neutral",
        "Q2_How_likely_is_it_that_you_would_recommend_company__product__service__brand_to_a_friend_or_colleague": "7",
        "ResponseNum": 2,
        "SrNO": 2,
        "StartTime": "10/31/2024 10:43 AM"
    }
]

app = Flask(__name__)

@app.route('/')
def service_document():
    service_doc = {
        "@odata.context": "/$metadata",
        "value": [
            {"name": "SurveyData", "kind": "EntitySet", "url": "SurveyData"}
        ]
    }
    return jsonify(service_doc)

@app.route('/$metadata')
def metadata():
    metadata_xml = """<?xml version="1.0" encoding="utf-8"?>
<edmx:Edmx Version="4.0" xmlns:edmx="http://docs.oasis-open.org/odata/ns/edmx">
  <edmx:DataServices>
    <Schema xmlns="http://docs.oasis-open.org/odata/ns/edm" Namespace="ODataService">
      <EntityType Name="SurveyData">
        <Key>
          <PropertyRef Name="SrNO" />
        </Key>
        <Property Name="SrNO" Type="Edm.Int32" Nullable="false" />
        <Property Name="ResponseNum" Type="Edm.Int32" />
        <Property Name="EmailID" Type="Edm.String" />
        <Property Name="ParticipationStatus" Type="Edm.String" />
        <Property Name="IPAddress" Type="Edm.String" />
        <Property Name="StartTime" Type="Edm.String" />
        <Property Name="EndTime" Type="Edm.String" />
        <Property Name="LastUpdate" Type="Edm.String" />
        <Property Name="Q1_Please_rate_your_level_of_agreement_with_this_statement_Companyproductservicebrand_made_it_easy_for_me_to_meet_my_needs" Type="Edm.String" />
        <Property Name="Q2_How_likely_is_it_that_you_would_recommend_company__product__service__brand_to_a_friend_or_colleague" Type="Edm.String" />
      </EntityType>
      <EntityContainer Name="Container">
        <EntitySet Name="SurveyData" EntityType="ODataService.SurveyData" />
      </EntityContainer>
    </Schema>
  </edmx:DataServices>
</edmx:Edmx>
    """
    return Response(metadata_xml, content_type='application/xml')

@app.route('/SurveyData')
def survey_data():
    df = pd.DataFrame(json_data)
    odata_response = {
        "@odata.context": "/$metadata#SurveyData",
        "value": df.to_dict(orient='records')
    }
    return jsonify(odata_response)

if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0", port=5000)
    # app.run(port=5000)
