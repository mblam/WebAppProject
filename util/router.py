from util.request import Request
import util.the_paths
import re


class Router:

    all_routes = {}

    def add_route(self, method: str, path: str, action):

        method_path = [method, path]
        self.all_routes[method_path] = action

    def route_request(self, the_request: Request):


        return b''
