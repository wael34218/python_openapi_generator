import unittest
import yaml
from openapi_spec_validator import openapi_v3_spec_validator


class TestOpenapiGenerator(unittest.TestCase):
    def test_schema(self):
        with open("example.yml") as f:
            spec = yaml.load(f)
        errors_iterator = openapi_v3_spec_validator.iter_errors(spec)
        self.assertEqual(len(list(errors_iterator)), 0)
