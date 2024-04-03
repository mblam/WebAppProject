import socketserver
import json
import random
from util.request import Request
from pymongo import MongoClient
from util.router import Router
from util.the_paths import Paths

# mongo_client = MongoClient("megandatabase")
# db = mongo_client["cse312"]
# chat_collection = db["chat"]


class MyTCPHandler(socketserver.BaseRequestHandler):

    paths = Paths()
    router = Router()

    router.add_route("GET", "/public/favicon.ico$", paths.serve_favicon)
    router.add_route("GET", "/$", paths.serve_root)
    router.add_route("GET", "/public/style.css$", paths.serve_css)

    router.add_route("GET", "/public/image/.", paths.serve_image)
    router.add_route("POST", "/form-path$", paths.post_image)

    router.add_route("GET", "/public/functions.js$", paths.serve_js)
    router.add_route("GET", "/public/webrtc.js$", paths.serve_js)

    router.add_route("POST", "/chat-messages$", paths.post_message)
    router.add_route("GET", "/chat-messages$", paths.get_messages)
    router.add_route("DELETE", "/chat-messages/.", paths.delete_message)

    router.add_route("POST", "/register$", paths.register_request)
    router.add_route("POST", "/login$", paths.login_request)
    router.add_route("POST", "/logout$", paths.logout_request)

    def handle(self):
        received_data = self.request.recv(2048)
        print(self.client_address)
        print("--- received data ---")
        print(received_data)
        print("--- end of data ---\n\n")
        request = Request(received_data)

        if request.headers.get("Content-Length") is not None:
            total_len = int(request.headers["Content-Length"])
            curr_len = len(request.body)

            while curr_len < total_len:
                new_req = self.request.recv(min(2048, total_len - curr_len))
                curr_len += min(2048, total_len - curr_len)
                request.add_to_body(new_req.body)

        # TODO: Parse the HTTP request and use self.request.sendall(response) to send your response
        response = self.router.route_request(request)

        self.request.sendall(response)

def main():
    host = "0.0.0.0"
    port = 8080

    socketserver.TCPServer.allow_reuse_address = True

    server = socketserver.TCPServer((host, port), MyTCPHandler)

    print("Listening on port " + str(port))

    server.serve_forever()


if __name__ == "__main__":
    main()
