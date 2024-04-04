from util.request import Request
from util.the_paths import Paths
import re


class Router:

    paths = Paths()
    all_routes = {}

    def add_route(self, method: str, path: str, action):

        method_path = method + " " + path
        self.all_routes[method_path] = action

    def route_request(self, the_request: Request):

        response = b''

        # method_path = the_request.method + the_request.path
        for elem in self.all_routes:
            split = elem.split(" ")
            if re.match(split[0], the_request.method):
                if re.match(split[1], "/public/image/."):
                    the_request.path = the_request.path[0:14] + the_request.path[14:].replace("/", "")
                if re.match(split[1], the_request.path):
                    func = self.all_routes[elem]
                    response = func(the_request)
                    break

        if response == b'':
            response = self.paths.serve_error(the_request)

        return response
