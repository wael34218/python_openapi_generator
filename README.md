# Python OpenAPI (Swagger) Generator
This library facilitates creating OpenAPI (Swagger) document for Python projects.

I worked for a long time in making APIs and services, and I can tell you that one thing I got sick of hearing was "Why are your code is not documented?".
I searched long and hard for a library that generates documentation them without me going back and forth editing text files ... its enough that I worry about writting unit and integration tests.
After long search I found 0 libraries that does that.
I was wondering why nobody has yet exploited this gap in a very lucrative market, wonder no longer. Help is at hand.

## Generate your API using simple script

```
from openapi_generator import OpenapiGenerator
import requests

# Step 1: Create an instance of the generator
gen = OpenapiGenerator("Title", "This is a testing description", "v0.0.1")

# Step 2: Add all responses
response = requests.get("https://swapi.co/api/planets/", params={"page": 2})
gen.add_response(response)

# Step 3:Export
gen.export("example.yml")

# Step 4: Profit
```

## Quirks

Dont depend on this, it is in its very early stage.
