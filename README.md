# Python OpenAPI (Swagger) Generator
This library facilitates creating OpenAPI (Swagger) document for Python projects.

I worked for a long time in building APIs and services, and I can tell you that one thing I got sick of hearing was "Why your APIs are not documented?".
I searched long and hard for a library that generates documentation without me going back and forth editing yaml/json/markdown files ... its enough that I worry about writting unit and integration tests.
After long search I found 0 libraries that does that.
I was wondering why nobody has yet exploited this gap in a very lucrative market, wonder no longer. Help is at hand.

## Installation

```
pip install git+git://github.com/wael34218/python_openapi_generator
```

## Generate your API using simple script

```
from openapi_generator.openapi_generator import OpenapiGenerator
import requests

# Step 1: Create an instance of the generator
gen = OpenapiGenerator("Title", "This is a testing description", "v0.0.1", server="https://swapi.co/")

# Step 2: Add all responses
response = requests.get("https://swapi.co/api/planets/", params={"page": 2})
gen.add_response(response, description="Retrieving planets")

response = requests.get("https://swapi.co/api/people/", params={"page": 3}, description="Retrieving people")
gen.add_response(response, description="Retrieving people")

# Step 3:Export
gen.export("example.yml", extension="yaml")
# Also can set the extension to `json`

# Step 4: Profit
```
