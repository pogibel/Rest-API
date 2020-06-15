import requests

url = "http://localhost:8000/api/get_data"

payload = "{\n\t\"data type\" : \"all\"\n}"
headers = {'content-type': 'application/json'}

response = requests.request("GET", url, data=payload, headers=headers)

print(response.text)