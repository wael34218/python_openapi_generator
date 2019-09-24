from openapi_generator import OpenapiGenerator
import requests

# Step 1: Create an instance of the generator
gen = OpenapiGenerator("Title", "This is a testing description", "0.0.1", "https://swapi.co")

# Step 2: Add all responses
response = requests.get("https://swapi.co/api/planets/", params={"page": 2})
gen.add_response(response)

response = requests.get("https://swapi.co/api/planets/")
gen.add_response(response)

response = requests.post("https://swapi.co/api/planets/", json={"page": 4})
gen.add_response(response)

response = requests.get("https://swapi.co/api/people/", params={"page": 3})
gen.add_response(response)

# Step 3:Export
gen.export("example.json", extension="json")

# Step 4: Profit
