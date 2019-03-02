from openapi_generator import OpenapiGenerator
import requests

# Step 1: Create an instance of the generator
gen = OpenapiGenerator("Title", "This is a testing description", "0.0.1")

# Step 2: Add all responses
response = requests.get("https://swapi.co/api/planets/", params={"page": 2})
gen.add_response(response)

# Step 3:Export
gen.export("example.yml")

# Step 4: Profit
