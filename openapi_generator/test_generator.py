import unittest
import yaml
from openapi_generator import OpenapiGenerator
import requests
import json
from openapi_spec_validator import openapi_v3_spec_validator


class TestOpenapiGenerator(unittest.TestCase):
    def test_yaml_schema(self):
        gen = OpenapiGenerator("Title", "Testing description", "0.0.1", "https://swapi.co")
        response = requests.get("https://swapi.co/api/planets/", params={"page": 2})
        gen.add_response(response)
        gen.export("example.yml", extension="yaml")

        with open("example.yml") as f:
            spec = yaml.load(f)
        errors_iterator = openapi_v3_spec_validator.iter_errors(spec)
        self.assertEqual(len(list(errors_iterator)), 0)

    def test_json_schema(self):
        gen = OpenapiGenerator("Title", "Testing description", "0.0.1", "https://swapi.co")
        response = requests.get("https://swapi.co/api/planets/", params={"page": 2})
        gen.add_response(response)
        gen.export("example.json", extension="json")

        with open("example.json") as f:
            spec = json.load(f)
        errors_iterator = openapi_v3_spec_validator.iter_errors(spec)
        self.assertEqual(len(list(errors_iterator)), 0)

    def test_audio_file(self):
        gen = OpenapiGenerator("Title", "Testing description", "0.0.1",
                               "test.audio.upload")
        lnk = "test.audio.upload"
        with open('test.wav', 'rb') as f:
            aud = f.read()

        response = requests.post(lnk, data=aud, headers={
            'Content-Type': 'application/body-data;rate={};channels={}'.format(16000, 1)})

        gen.add_response(response)
        gen.export("wav.json", extension="json")

        with open("wav.json") as f:
            spec = json.load(f)
        errors_iterator = openapi_v3_spec_validator.iter_errors(spec)
        self.assertEqual(len(list(errors_iterator)), 0)
