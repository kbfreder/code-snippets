import requests
import json


url = "https://domino.cda.cslbehring.cloud:443/models/6622caedf676c14b98b21e8b/latest/model"
token = "Teri78bOkXgS5Ff95kH9ftlqkTx5qg7UfKg5eSSBpG3WrZgfHf4UAbiMS4aBW1R5"


headers = {
    'Content-Type': 'application/json'
    ## could also include Auth here: *thought
    # 'Authorization': Basic <base64encoded username + password>
}

text = "Trend noted for Equipment Validation Documentation Errors"

input = {"data":{
    "text": text
}}

response = requests.post(
    url=url,
    auth=(token, token), # or: (username, password)
    ## this is equivalent to:
    # from requests.auth import HTTPBasicAuth
    # auth=HTTPBasicAuth(user, pass)
    headers=headers,
    data=json.dumps(input)
)

parsed_response = response.json()

event_id = parsed_response['result']['event_id']
event_time = parsed_response['result']['event_time']
