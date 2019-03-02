import yaml
import urllib
import json


class OpenapiGenerator():
    types_map = {"int": "integer",
                 "bool": "boolean",
                 "float": "number",
                 "str": "string",
                 "list": "array",
                 "dict": "object"}

    def __init__(self, title, description, version, server=None):
        self.configs = {
            "openapi": "3.0.1",
            "info": {"title": title, "description": description, "version": version},
            "servers": [
                {"url": "https://swapi.co", "description": "Path to server"}
            ]
        }
        self.paths = {}

    def add_response(self, response, description=""):
        parsed_url = urllib.parse.urlparse(response.request.url)
        path_object = {response.request.method.lower(): {}}
        parameters = self._get_parameters(response)
        request_body = self._get_request_body(response)
        responses = self._get_response(response)

        if description:
            path_object[response.request.method.lower()]['description'] = description

        if parameters:
            path_object[response.request.method.lower()]['parameters'] = parameters

        if request_body:
            path_object[response.request.method.lower()]['requestBody'] = request_body

        if responses:
            path_object[response.request.method.lower()]['responses'] = responses

        self.paths[parsed_url.path] = path_object
        self.configs["paths"] = self.paths

    def export(self, filename):
        with open(filename, "w") as output_file:
            output_file.write(yaml.dump(self.configs, default_flow_style=False))

    def _get_request_body(self, response):
        request_body = {}
        if response.request.body:
            if response.request.headers['Content-Type'] == 'application/json':
                try:
                    example = json.loads(response.request.body.decode('utf-8'))
                    request_body['content'] = {
                        'application/json': {
                            'schema': {
                                'type': 'object',
                                'properties': {
                                    k: {'type': self.types_map[v.__class__.__name__]}
                                    for k, v in example.items()}
                            },
                            'example': {k: v for k, v in example.items()}
                        }
                    }
                except ValueError:
                    print("invalid json passed")

        return request_body

    def _get_response(self, response):
        status = "{}".format(response.status_code)
        return {
            status: {
                'description': 'Get this from docstring',
                'content': {
                    response.headers['Content-Type']: {
                        'schema': {
                            'type': 'object',
                            'properties': {
                                k: {'type': self.types_map[v.__class__.__name__]}
                                for k, v in response.json().items()}
                        },
                        'example': {k: v for k, v in response.json().items()}
                    }
                }
            }
        }

    def _get_parameters(self, response):
        # Adding parameters [query, headers, cookie].
        # TODO: implement [path] parameters.
        parameters = []
        qs = urllib.parse.parse_qs(urllib.parse.urlparse(response.request.url).query)
        for k, v in qs.items():
            param = {'name': k,
                     'in': 'query',
                     'schema': {'type': self.types_map[v[0].__class__.__name__]},
                     'example': v[0]}
            parameters.append(param)

        for k, v in response.request.headers.items():
            if k in ['Accept', 'Connection', 'User-Agent', 'Accept-Encoding', 'Content-Length']:
                continue
            param = {'name': k,
                     'in': 'header',
                     'schema': {'type': self.types_map[v.__class__.__name__]},
                     'example': v}
            parameters.append(param)

        for k, v in response.cookies.items():
            param = {'name': k,
                     'in': 'cookie',
                     'schema': {'type': self.types_map[v.__class__.__name__]},
                     'example': v}
            parameters.append(param)
        return parameters
