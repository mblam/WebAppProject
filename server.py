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

    router.add_route("GET","/public/favicon.ico$", paths.serve_favicon)
    router.add_route("GET", "/$", paths.serve_root)
    router.add_route("GET", "/public/style.css$", paths.serve_css)

    # router.add_route("GET", "/public/image/cat.jpg$", paths.serve_image)
    # router.add_route("GET", "/public/image/dog.jpg$", paths.serve_image)
    # router.add_route("GET", "/public/image/eagle.jpg$", paths.serve_image)
    # router.add_route("GET", "/public/image/elephant.jpg$", paths.serve_image)
    # router.add_route("GET", "/public/image/elephant-small.jpg$", paths.serve_image)
    # router.add_route("GET", "/public/image/flamingo.jpg$", paths.serve_image)
    # router.add_route("GET", "/public/image/kitten.jpg$", paths.serve_image)
    router.add_route("GET", "/public/image.", paths.serve_image)

    router.add_route("GET", "/public/functions.js$", paths.serve_js)
    router.add_route("GET", "/public/webrtc.js$", paths.serve_js)

    router.add_route("POST", "/chat-messages$", paths.post_message)
    router.add_route("GET", "/chat-messages$", paths.get_messages)

    def handle(self):
        received_data = self.request.recv(2048)
        print(self.client_address)
        print("--- received data ---")
        print(received_data)
        print("--- end of data ---\n\n")
        request = Request(received_data)

        # TODO: Parse the HTTP request and use self.request.sendall(response) to send your response
        response = self.router.route_request(request)
        # response = b''
        #
        # if request.path == "/public/favicon.ico":
        #     response += (request.http_version + " 200 OK\r\n").encode()
        #
        #     for header in request.headers:
        #         response += (header + ": " + request.headers[header] + "\r\n").encode()
        #
        #     favicon = open("public/favicon.ico", "rb")
        #     favicon_bytes = str(len(favicon.read()))
        #     response += "X-Content-Type-Options: nosniff\r\n".encode()
        #     response += ("Content-Type: image/x-icon\r\nContent-Length: " + favicon_bytes + "\r\n\r\n").encode()
        #
        #     response += open("public/favicon.ico", "rb").read()
        # elif request.path == "/public/functions.js":
        #     response += (request.http_version + " 200 OK\r\n").encode()
        #
        #     for header in request.headers:
        #         response += (header + ": " + request.headers[header] + "\r\n").encode()
        #     response += "X-Content-Type-Options: nosniff\r\n".encode()
        #
        #     response += "Content-Type: text/javascript".encode()
        #
        #     open_file = open("public/functions.js", "rb").read()
        #     byte_num = str(len(open_file))
        #     response += ("\r\nContent Length: " + byte_num).encode()
        #
        #     response += "\r\n\r\n".encode() + open_file
        # elif request.path == "/":
        #     response += (request.http_version + " 200 OK\r\n").encode()
        #
        #     if "visits" not in request.cookies:
        #         request.headers["Set-Cookie"] = "visits=1; Max-Age=3600"
        #         request.cookies["visits"] = "1"
        #     else:
        #         request.headers["Set-Cookie"] = "visits=" + str(int(request.cookies["visits"]) + 1) + "; Max-Age=3600"
        #         request.cookies["visits"] = str(int(request.cookies["visits"]) + 1)
        #
        #     for header in request.headers:
        #         response += (header + ": " + request.headers[header] + "\r\n").encode()
        #
        #     response += "X-Content-Type-Options: nosniff\r\n".encode()
        #
        #     response += "Content-Type: text/html; charset=utf-8".encode()
        #
        #     open_file = open("public/index.html", "rb").read()
        #     edit = open_file.replace("{{visits}}".encode(), request.cookies["visits"].encode())
        #     byte_num = str(len(edit))
        #     response += ("\r\nContent Length: " + byte_num).encode()
        #
        #     response += "\r\n\r\n".encode() + edit
        # elif request.path == "/public/style.css":
        #     response += (request.http_version + " 200 OK\r\n").encode()
        #
        #     for header in request.headers:
        #         response += (header + ": " + request.headers[header] + "\r\n").encode()
        #     response += "X-Content-Type-Options: nosniff\r\n".encode()
        #
        #     response += "Content-Type: text/css".encode()
        #
        #     open_file = open("public/style.css", "rb").read()
        #     byte_num = str(len(open_file))
        #     response += ("\r\nContent Length: " + byte_num).encode()
        #
        #     response += "\r\n\r\n".encode() + open_file
        # elif request.path == "/public/webrtc.js":
        #     response += (request.http_version + " 200 OK\r\n").encode()
        #
        #     for header in request.headers:
        #         response += (header + ": " + request.headers[header] + "\r\n").encode()
        #     response += "X-Content-Type-Options: nosniff\r\n".encode()
        #
        #     response += "Content-Type: text/javascript".encode()
        #
        #     open_file = open("public/webrtc.js", "rb").read()
        #     byte_num = str(len(open_file))
        #     response += ("\r\nContent Length: " + byte_num).encode()
        #
        #     response += "\r\n\r\n".encode() + open_file
        # elif request.path == "/public/image/eagle.jpg":
        #     response += (request.http_version + " 200 OK\r\n").encode()
        #
        #     for header in request.headers:
        #         response += (header + ": " + request.headers[header] + "\r\n").encode()
        #     response += "X-Content-Type-Options: nosniff\r\n".encode()
        #
        #     eagle_img = open("public/image/eagle.jpg", "rb")
        #     eagle_bytes = str(len(eagle_img.read()))
        #     response += ("Content-Type: image/jpeg\r\nContent-Length:" + eagle_bytes + "\r\n\r\n").encode()
        #
        #     response += open("public/image/eagle.jpg", "rb").read()
        # elif request.path == "/public/image/cat.jpg":
        #     response += (request.http_version + " 200 OK\r\n").encode()
        #
        #     for header in request.headers:
        #         response += (header + ": " + request.headers[header] + "\r\n").encode()
        #     response += "X-Content-Type-Options: nosniff\r\n".encode()
        #
        #     img = open("public/image/cat.jpg", "rb")
        #     the_bytes = str(len(img.read()))
        #     response += ("Content-Type: image/jpeg\r\nContent-Length:" + the_bytes + "\r\n\r\n").encode()
        #
        #     response += open("public/image/cat.jpg", "rb").read()
        # elif request.path == "/public/image/dog.jpg":
        #     response += (request.http_version + " 200 OK\r\n").encode()
        #
        #     for header in request.headers:
        #         response += (header + ": " + request.headers[header] + "\r\n").encode()
        #     response += "X-Content-Type-Options: nosniff\r\n".encode()
        #
        #     img = open("public/image/dog.jpg", "rb")
        #     the_bytes = str(len(img.read()))
        #     response += ("Content-Type: image/jpeg\r\nContent-Length:" + the_bytes + "\r\n\r\n").encode()
        #
        #     response += open("public/image/dog.jpg", "rb").read()
        # elif request.path == "/public/image/elephant.jpg":
        #     response += (request.http_version + " 200 OK\r\n").encode()
        #
        #     for header in request.headers:
        #         response += (header + ": " + request.headers[header] + "\r\n").encode()
        #     response += "X-Content-Type-Options: nosniff\r\n".encode()
        #
        #     img = open("public/image/elephant.jpg", "rb")
        #     the_bytes = str(len(img.read()))
        #     response += ("Content-Type: image/jpeg\r\nContent-Length:" + the_bytes + "\r\n\r\n").encode()
        #
        #     response += open("public/image/elephant.jpg", "rb").read()
        # elif request.path == "/public/image/elephant-small.jpg":
        #     response += (request.http_version + " 200 OK\r\n").encode()
        #
        #     for header in request.headers:
        #         response += (header + ": " + request.headers[header] + "\r\n").encode()
        #     response += "X-Content-Type-Options: nosniff\r\n".encode()
        #
        #     img = open("public/image/elephant-small.jpg", "rb")
        #     the_bytes = str(len(img.read()))
        #     response += ("Content-Type: image/jpeg\r\nContent-Length:" + the_bytes + "\r\n\r\n").encode()
        #
        #     response += open("public/image/elephant-small.jpg", "rb").read()
        # elif request.path == "/public/image/flamingo.jpg":
        #     response += (request.http_version + " 200 OK\r\n").encode()
        #
        #     for header in request.headers:
        #         response += (header + ": " + request.headers[header] + "\r\n").encode()
        #     response += "X-Content-Type-Options: nosniff\r\n".encode()
        #
        #     img = open("public/image/flamingo.jpg", "rb")
        #     the_bytes = str(len(img.read()))
        #     response += ("Content-Type: image/jpeg\r\nContent-Length:" + the_bytes + "\r\n\r\n").encode()
        #
        #     response += open("public/image/flamingo.jpg", "rb").read()
        # elif request.path == "/public/image/kitten.jpg":
        #     response += (request.http_version + " 200 OK\r\n").encode()
        #
        #     for header in request.headers:
        #         response += (header + ": " + request.headers[header] + "\r\n").encode()
        #     response += "X-Content-Type-Options: nosniff\r\n".encode()
        #
        #     img = open("public/image/kitten.jpg", "rb")
        #     the_bytes = str(len(img.read()))
        #     response += ("Content-Type: image/jpeg\r\nContent-Length:" + the_bytes + "\r\n\r\n").encode()
        #
        #     response += open("public/image/kitten.jpg", "rb").read()
        # elif (request.path == "/chat-messages") and (request.method == "POST"):
        #     response += (request.http_version + " 200 OK\r\n").encode()
        #
        #     for header in request.headers:
        #         response += (header + ": " + request.headers[header] + "\r\n").encode()
        #     response += "X-Content-Type-Options: nosniff\r\n".encode()
        #
        #     the_body = json.loads(request.body.decode())
        #
        #     numlist = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
        #     i = 0
        #     uniqueID = ""
        #     while i != 10:
        #         uniqueID += random.choices(numlist)[0]
        #         i += 1
        #
        #     message = json.dumps(the_body["message"]).replace('&', "&amp;").replace('<', "&lt;").replace('>', "&gt;")
        #
        #     store_this = {"message": message, "username": "Guest", "id": uniqueID}
        #     chat_collection.insert_one(store_this)
        #
        #     response += "X-Content-Type-Options: nosniff\r\n".encode()
        #     response += "Content-Type: text/plain\r\nContent-Length: 26\r\n\r\nFrontend will ignore this.".encode()
        # elif (request.path == "/chat-messages") and (request.method == "GET"):
        #     response += (request.http_version + " 200 OK\r\n").encode()
        #
        #     for header in request.headers:
        #         response += (header + ": " + request.headers[header] + "\r\n").encode()
        #     response += "X-Content-Type-Options: nosniff\r\n".encode()
        #
        #     the_data = chat_collection.find({}, {"_id": 0})
        #     str_data = []
        #     for elem in the_data:
        #         str_data.append(elem)
        #     json_encoded = json.dumps(str_data).encode()
        #
        #     response += ("Content-Type: application/json\r\nContent-Length: " + str(len(json_encoded)) + "\r\n\r\n").encode() + json_encoded
        # else:
        #     response += (request.http_version + " 404 Not Found\r\n").encode()
        #
        #     for header in request.headers:
        #         response += (header + ": " + request.headers[header] + "\r\n").encode()
        #
        #     response += "X-Content-Type-Options: nosniff\r\n".encode()
        #
        #     response += "Content-Type: text/plain\r\nContent-Length: 54\r\n\r\nThis is an error page. Definitely not what you wanted.".encode()

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
