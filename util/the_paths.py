from util.request import Request
from pymongo import MongoClient
from util.auth import extract_credentials
from util.auth import validate_password
import string
import bcrypt
import json
import random

mongo_client = MongoClient("megandatabase")
db = mongo_client["cse312"]
chat_collection = db["chat"]
user_collection = db["user-list"]

class Paths:

    def serve_root(self, request: Request):
        response = b''

        response += (request.http_version + " 200 OK\r\n").encode()

        if "visits" not in request.cookies:
            request.headers["Set-Cookie"] = "visits=1; Max-Age=3600"
            request.cookies["visits"] = "1"
        else:
            request.headers["Set-Cookie"] = "visits=" + str(int(request.cookies["visits"]) + 1) + "; Max-Age=3600"
            request.cookies["visits"] = str(int(request.cookies["visits"]) + 1)

        for header in request.headers:
            response += (header + ": " + request.headers[header] + "\r\n").encode()

        response += "X-Content-Type-Options: nosniff\r\nContent-Type: text/html; charset=utf-8".encode()

        open_file = open("public/index.html", "rb").read()
        edit = open_file.replace("{{visits}}".encode(), request.cookies["visits"].encode())
        byte_num = str(len(edit))
        response += ("\r\nContent Length: " + byte_num).encode()

        response += "\r\n\r\n".encode() + edit

        return response

    def serve_js(self, request: Request):
        response = b''

        response += (request.http_version + " 200 OK\r\n").encode()

        for header in request.headers:
            response += (header + ": " + request.headers[header] + "\r\n").encode()
        response += "X-Content-Type-Options: nosniff\r\n".encode()

        response += "Content-Type: text/javascript".encode()

        js_file = request.path[1:len(request.path)]
        js = open(js_file, "rb").read()
        byte_num = str(len(js))

        response += ("\r\nContent Length: " + byte_num).encode()

        response += "\r\n\r\n".encode() + js

        return response

    def serve_image(self, request: Request):
        response = b''

        response += (request.http_version + " 200 OK\r\n").encode()

        for header in request.headers:
            response += (header + ": " + request.headers[header] + "\r\n").encode()
        response += "X-Content-Type-Options: nosniff\r\n".encode()

        image_file = request.path[1:len(request.path)]
        image = open(image_file, "rb")
        the_bytes = str(len(image.read()))
        response += ("Content-Type: image/jpeg\r\nContent-Length:" + the_bytes + "\r\n\r\n").encode()

        response += open(image_file, "rb").read()

        return response

    def serve_favicon(self, request: Request):
        response = b''

        response += (request.http_version + " 200 OK\r\n").encode()

        for header in request.headers:
            response += (header + ": " + request.headers[header] + "\r\n").encode()

        favicon = open("public/favicon.ico", "rb")
        favicon_bytes = str(len(favicon.read()))
        response += "X-Content-Type-Options: nosniff\r\n".encode()
        response += ("Content-Type: image/x-icon\r\nContent-Length: " + favicon_bytes + "\r\n\r\n").encode()

        response += open("public/favicon.ico", "rb").read()

        return response

    def serve_css(self, request: Request):
        response = b''

        response += (request.http_version + " 200 OK\r\n").encode()

        for header in request.headers:
            response += (header + ": " + request.headers[header] + "\r\n").encode()
        response += "X-Content-Type-Options: nosniff\r\n".encode()

        response += "Content-Type: text/css".encode()

        open_file = open("public/style.css", "rb").read()
        byte_num = str(len(open_file))
        response += ("\r\nContent Length: " + byte_num).encode()

        response += "\r\n\r\n".encode() + open_file

        return response

    def post_message(self, request: Request):
        response = b''

        response += (request.http_version + " 200 OK\r\n").encode()

        for header in request.headers:
            response += (header + ": " + request.headers[header] + "\r\n").encode()
        response += "X-Content-Type-Options: nosniff\r\n".encode()

        the_body = json.loads(request.body.decode())

        numlist = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
        i = 0
        uniqueID = ""
        while i != 10:
            uniqueID += random.choices(numlist)[0]
            i += 1

        message = json.dumps(the_body["message"]).replace('&', "&amp;").replace('<', "&lt;").replace('>', "&gt;")

        store_this = {"message": message, "username": "Guest", "id": uniqueID}
        chat_collection.insert_one(store_this)

        response += "X-Content-Type-Options: nosniff\r\n".encode()
        response += "Content-Type: text/plain\r\nContent-Length: 26\r\n\r\nFrontend will ignore this.".encode()

        return response

    def get_messages(self, request: Request):
        response = b''

        response += (request.http_version + " 200 OK\r\n").encode()

        for header in request.headers:
            response += (header + ": " + request.headers[header] + "\r\n").encode()
        response += "X-Content-Type-Options: nosniff\r\n".encode()

        the_data = chat_collection.find({}, {"_id": 0})
        str_data = []
        for elem in the_data:
            str_data.append(elem)
        json_encoded = json.dumps(str_data).encode()

        response += ("Content-Type: application/json\r\nContent-Length: " + str(
            len(json_encoded)) + "\r\n\r\n").encode() + json_encoded

        return response

    def register_request(self, request: Request):
        response = b''
        response += (request.http_version + " 302 Found\r\n").encode()

        for header in request.headers:
            response += (header + ": " + request.headers[header] + "\r\n").encode()
        response += "X-Content-Type-Options: nosniff\r\n".encode()

        credentials = extract_credentials(request)
        if validate_password(credentials[1]):
            the_bytes = credentials[1].encode()
            the_salt = bcrypt.gensalt()
            the_hash = bcrypt.hashpw(the_bytes,the_salt)

            store_this = {"username": credentials[0], "hash": the_hash}
            user_collection.insert_one(store_this)

        response += "Content-Length: 0\r\nLocation: /\r\n\r\n".encode()

        return response

    def login_request(self, request: Request):
        response = b''
        response += (request.http_version + " 302 Found\r\n").encode()

        for header in request.headers:
            response += (header + ": " + request.headers[header] + "\r\n").encode()
        response += "X-Content-Type-Options: nosniff\r\n".encode()

        # making auth token just in case if needed
        big_list = list(string.ascii_letters + string.digits)
        i = 0
        auth_token = ""
        while i != 22:
            auth_token += random.choices(big_list)[0]
            i += 1

        credentials = extract_credentials(request)
        find_user = user_collection.find_one({"username": credentials[0]})
        if find_user is not None:
            the_bytes = credentials[1].encode()
            if bcrypt.checkpw(the_bytes, find_user["hash"]):
                response += ("Set-Cookie: Auth Token=" + auth_token + "; HttpOnly; Max-Age=3600\r\n").encode()

        response += "Content-Length: 0\r\nLocation: /\r\n\r\n".encode()

        return response

    def logout_request(self, request: Request):
        response = b''
        response += (request.http_version + " 302 Found\r\n").encode()


        return response

    def serve_error(self, request: Request):
        response = b''
        response += (request.http_version + " 404 Not Found\r\n").encode()

        for header in request.headers:
            response += (header + ": " + request.headers[header] + "\r\n").encode()

        response += "X-Content-Type-Options: nosniff\r\n".encode()

        response += "Content-Type: text/plain\r\nContent-Length: 54\r\n\r\nThis is an error page. Definitely not what you wanted.".encode()

        return response

