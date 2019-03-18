import yaml
import urllib
import json


class OpenapiGenerator():
    types_map = {"int": "integer",
                 "bool": "boolean",
                 "float": "number",
                 "str": "string",
                 "list": "array",
                 "dict": "object",
                 "NoneType": "string"}

    def __init__(self, title, description, version, server, server_description=""):
        """
        Initialize the OpenAPI Generator

        Parameters:
            title (str): Title of the API documentation
            description (str): A brief description about the entire service (API application)
            version (str): Version of application
            server (str): Server URL with root path
            server_description (str): Description of the server staging/production, default: ""
        """
        self.configs = {
            "openapi": "3.0.1",
            "info": {"title": title, "description": description, "version": version},
            "servers": [
                {"url": server, "description": server_description}
            ]
        }
        self.paths = {}

    def add_response(self, response, description=""):
        """
        Augment current OpenAPI configuration with the passed request

        Parameters:
            response (Response): requests Response object.
            description (str): A brief description about the API call
        """
        path_object = {}
        parameters = self._get_parameters(response)
        request_body = self._get_request_body(response)
        responses = self._get_response(response)

        if description:
            path_object['description'] = description

        if parameters:
            path_object['parameters'] = parameters

        if request_body:
            path_object['requestBody'] = request_body

        if responses:
            path_object['responses'] = responses

        '''
        Merging paths multiple path objects. Priority goes in chronological order first response
        will make up the base of the documentation, later responses will augment and add what
        is missing in the first one.
        '''
        parsed_url = urllib.parse.urlparse(response.request.url)
        method = response.request.method.lower()
        status = "{}".format(response.status_code)
        if parsed_url.path in self.paths:
            if method in self.paths[parsed_url.path]:
                if status not in self.paths[parsed_url.path][method]["responses"]:
                    status_response = path_object["responses"][status]
                    self.paths[parsed_url.path][method]["responses"][status] = status_response
            else:
                self.paths[parsed_url.path][method] = path_object

            if "description" not in self.paths[parsed_url.path][method] and description:
                self.paths[parsed_url.path][method]["description"] = description
        else:
            self.paths[parsed_url.path] = {method: path_object}
        self.configs["paths"] = self.paths

    def export(self, filename):
        """
        Export configuration into a yaml OpenAPI format

        Parameters:
            filename (str): Output file path.
        """
        with open(filename, "w") as output_file:
            output_file.write(yaml.dump(self.configs, default_flow_style=False))

    @staticmethod
    def _get_props(item, example=False):
        """
        A recursive function that unfolds an item to its leaves and returns a dictionary describing
        the item

        Parameters:
            item (any type of types_map): An object will be added to the openAPI
            example (bool): Whether to add an example of the item

        Returns:
            props (dict): Object properties that describes item
        """
        item_type = OpenapiGenerator.types_map[item.__class__.__name__]
        props = {'type': item_type}
        if example:
            props['example'] = item
        if item_type == "array":
            properties = []
            for i in item:
                i_type = OpenapiGenerator.types_map[i.__class__.__name__]
                if i_type not in [x['type'] for x in properties]:
                    properties.append(OpenapiGenerator._get_props(i))

            if len(properties) > 0:
                props['items'] = {"oneOf": properties}
            else:
                props['items'] = {}
        if item_type == "object":
            props['properties'] = {k: OpenapiGenerator._get_props(v) for k, v in item.items()}
        return props

    @staticmethod
    def _get_request_body(response):
        """


        Parameters:
            response (Response): requests Response object.

        Returns:
            request_body (dict): Object properties that describes the response
        """
        # TODO: Handle xml, plain text and other formats
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
                                    k: OpenapiGenerator._get_props(v, example=True)
                                    for k, v in example.items()
                                }
                            }
                        }
                    }
                except ValueError:
                    print("invalid json passed")

        return request_body

    @staticmethod
    def _get_response(response):
        """
        Structure response object compatible with OpenAPI documentation

        Parameters:
            response (Response): requests Response object.

        Returns:
            response_body (dict): Object properties that describes the response
        """

        # TODO: Find a way to pass/get description for the response
        status = "{}".format(response.status_code)
        return {
            status: {
                # TODO: pass description
                'description': '',
                'content': {
                    response.headers['Content-Type']: {
                        'schema': {
                            'type': 'object',
                            'properties': {
                                k: OpenapiGenerator._get_props(v, example=True)
                                for k, v in response.json().items()
                            }
                        }
                    }
                }
            }
        }

    @staticmethod
    def _get_parameters(response):
        """
        Structure parameters object compatible with OpenAPI documentation

        Parameters:
            response (Response): requests Response object.

        Returns:
            response_body (dict): Object properties that describes API parameters
        """
        # Adding parameters [query, headers, cookie].
        # TODO: implement [path] parameters.
        parameters = []

        def create_param_dict(k, v, param_type):
            return {
                'name': k,
                'in': param_type,
                'schema': {'type': OpenapiGenerator.types_map[v.__class__.__name__]},
                'example': v
            }

        qs = urllib.parse.parse_qs(urllib.parse.urlparse(response.request.url).query)
        for k, v in qs.items():
            parameters.append(create_param_dict(k, v[0], 'query'))

        for k, v in response.request.headers.items():
            if k in ['Accept', 'Connection', 'User-Agent', 'Accept-Encoding', 'Content-Length']:
                continue
            parameters.append(create_param_dict(k, v, 'header'))

        for k, v in response.cookies.items():
            parameters.append(create_param_dict(k, v, 'cookie'))

        return parameters
