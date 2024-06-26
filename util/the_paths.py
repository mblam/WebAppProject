from util.request import Request
from pymongo import MongoClient
from util.auth import extract_credentials
from util.auth import validate_password
from util.multipart import parse_multipart
import string
import bcrypt
import hashlib
import json
import random

mongo_client = MongoClient("megandatabase")
db = mongo_client["cse312"]
chat_collection = db["chat"]
user_collection = db["user-list"]
xsrf_collection = db["xsrf"]


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

        if ("Auth Token" in request.cookies) and (request.cookies["Auth Token"] != ""):
            sha256 = hashlib.sha256()
            sha256.update(request.cookies["Auth Token"].encode())
            hashing = sha256.hexdigest()

            find_user = user_collection.find_one({"authtoken": hashing})

            find_xsrf = xsrf_collection.find_one({"username": find_user["username"]})
            if find_xsrf is None:
                xsrf_token = self.create_xsrf()
                store_this = {"username": find_user["username"], "xsrftoken": xsrf_token}
                xsrf_collection.insert_one(store_this)

            find_xsrf_again = xsrf_collection.find_one({"username": find_user["username"]})
            edited = edit.replace("{{xsrf-token}}".encode(), find_xsrf_again["xsrftoken"].encode())
            byte_num = str(len(edited))
            response += ("\r\nContent Length: " + byte_num).encode()

            response += "\r\n\r\n".encode() + edited
        else:
            byte_num = str(len(edit))
            response += ("\r\nContent Length: " + byte_num).encode()

            response += "\r\n\r\n".encode() + edit

        return response

    def create_xsrf(self):
        big_list = list(string.ascii_letters + string.digits)
        i = 0
        xsrf_token = ""
        while i != 27:
            xsrf_token += random.choices(big_list)[0]
            i += 1

        return xsrf_token

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

        request.headers.pop("Content-Length")
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

        if ("Auth Token" not in request.cookies.keys()) or (request.cookies["Auth Token"] == ""):
            store_this = {"message": message, "username": "Guest", "id": uniqueID}
            chat_collection.insert_one(store_this)
        elif ("Auth Token" in request.cookies.keys()) and (request.cookies["Auth Token"] != ""):
            sha256 = hashlib.sha256()
            sha256.update(request.cookies["Auth Token"].encode())
            hashing = sha256.hexdigest()
            find_user = user_collection.find_one({"authtoken": hashing})
            xsrf_token = json.dumps(the_body["xsrftoken"])
            the_xsrf_token = xsrf_token[1:len(xsrf_token) - 1]

            if find_user is not None:
                find_user_xsrf = xsrf_collection.find_one({"username": find_user["username"]})
                if the_xsrf_token == find_user_xsrf["xsrftoken"]:
                    store_this = {"message": message, "username": find_user["username"], "id": uniqueID}
                    chat_collection.insert_one(store_this)
                else:
                    wrong_response = b''
                    wrong_response += (request.http_version + " 403 Forbidden\r\n").encode()

                    for header in request.headers:
                        wrong_response += (header + ": " + request.headers[header] + "\r\n").encode()
                    wrong_response += "X-Content-Type-Options: nosniff\r\n".encode()

                    wrong_response += "Content-Type: text/plain\r\nContent-Length: 20\r\n\r\nYou can not do that.".encode()

                    return wrong_response
            else:
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

        request.headers.pop("Host")
        request.headers["Content-Length"] = "0"
        for header in request.headers:
            response += (header + ": " + request.headers[header] + "\r\n").encode()
        response += "X-Content-Type-Options: nosniff\r\n".encode()

        credentials = extract_credentials(request)
        credentials[0].replace('&', "&amp;").replace('<', "&lt;").replace('>', "&gt;")
        if validate_password(credentials[1]):
            the_bytes = credentials[1].encode()
            the_salt = bcrypt.gensalt()
            the_hash = bcrypt.hashpw(the_bytes, the_salt)

            store_this = {"username": credentials[0], "hash": the_hash, "authtoken": ""}
            user_collection.insert_one(store_this)

        response += "Content-Type: application/json\r\nLocation: /\r\n\r\n".encode()

        return response

    def login_request(self, request: Request):
        response = b''
        response += (request.http_version + " 302 Found\r\n").encode()

        request.headers.pop("Host")
        request.headers["Content-Length"] = "0"
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
        # hashing auth token
        sha256 = hashlib.sha256()
        sha256.update(auth_token.encode())
        hashing = sha256.hexdigest()

        credentials = extract_credentials(request)
        credentials[0].replace('&', "&amp;").replace('<', "&lt;").replace('>', "&gt;")
        find_user = user_collection.find_one({"username": credentials[0]})
        if find_user is not None:
            the_bytes = credentials[1].encode()
            if bcrypt.checkpw(the_bytes, find_user["hash"]):
                response += ("Set-Cookie: Auth Token=" + auth_token + "; HttpOnly; Max-Age=3600\r\n").encode()

        user_collection.update_one({"username": credentials[0]}, {'$set': {"authtoken": hashing}})

        response += "Content-Type: application/json\r\nLocation: /\r\n\r\n".encode()

        return response

    def logout_request(self, request: Request):
        response = b''
        response += (request.http_version + " 302 Found\r\n").encode()
        auth_token = request.cookies["Auth Token"]
        sha256 = hashlib.sha256()
        sha256.update(auth_token.encode())
        hashing = sha256.hexdigest()

        request.headers.pop("Host")
        request.headers["Content-Length"] = "0"
        request.headers["Set-Cookie"] = "Auth Token= """
        request.cookies["Auth Token"] = ""
        for header in request.headers:
            response += (header + ": " + request.headers[header] + "\r\n").encode()
        response += "X-Content-Type-Options: nosniff\r\n".encode()

        user_collection.update_one({"authtoken": hashing}, {'$set': {"authtoken": ""}})

        response += "Content-Type: application/json\r\nLocation: /\r\n\r\n".encode()

        return response

    def delete_message(self, request: Request):
        response = b''
        response += request.http_version.encode()
        sha256 = hashlib.sha256()

        chat_id = request.path[15:len(request.path)]

        if ("Auth Token" in request.cookies.keys()) and (request.cookies["Auth Token"] != ""):
            sha256.update(request.cookies["Auth Token"].encode())
            hashing = sha256.hexdigest()
            find_user = user_collection.find_one({"authtoken": hashing})
            find_message = chat_collection.find_one({"id": chat_id})
            if find_user["username"] == find_message["username"]:
                chat_collection.delete_one({"id": chat_id})
                response += " 200 OK\r\n".encode()
                for header in request.headers:
                    response += (header + ": " + request.headers[header] + "\r\n").encode()
                response += "X-Content-Type-Options: nosniff\r\n".encode()
                response += "Content-Type: text/plain\r\nContent-Length: 16\r\n\r\nMessage deleted."
            else:
                response += " 403 Forbidden\r\n".encode()

                for header in request.headers:
                    response += (header + ": " + request.headers[header] + "\r\n").encode()
                response += "X-Content-Type-Options: nosniff\r\n".encode()

                response += "Content-Type: text/plain\r\nContent-Length: 20\r\n\r\nYou can not do that.".encode()
        else:
            response += " 403 Forbidden\r\n".encode()

            for header in request.headers:
                response += (header + ": " + request.headers[header] + "\r\n").encode()
            response += "X-Content-Type-Options: nosniff\r\n".encode()

            response += "Content-Type: text/plain\r\nContent-Length: 20\r\n\r\nYou can not do that.".encode()

        return response

    def post_image(self, request: Request):
        the_multipart = parse_multipart(request)
        response = b''
        response += (request.http_version + " 302 Found\r\n").encode()

        request.headers.pop("Host")
        request.headers["Content-Length"] = "0"
        for header in request.headers:
            response += (header + ": " + request.headers[header] + "\r\n").encode()
        response += "X-Content-Type-Options: nosniff\r\n".encode()

        big_list = list(string.ascii_letters + string.digits)
        i = 0
        an_id = ""
        while i != 10:
            an_id += random.choices(big_list)[0]
            i += 1
        filename = "media" + an_id

        for part in the_multipart.parts:
            if part.headers.get("Content-Type") == "image/jpeg":
                filename += ".jpg"
                break
            elif part.headers.get("Content-Type") == "video/mp4":
                filename += ".mp4"
                break

        save_file = open("./public/image/" + filename, "wb")
        for part in the_multipart.parts:
            if part.headers.get("Content-Type") == "image/jpeg":
                save_file.write(part.content)
            elif part.headers.get("Content-Type") == "video/mp4":
                save_file.write(part.content)
        save_file.close()

        if filename.endswith(".jpg"):
            self.for_images(request, an_id, filename)
        elif filename.endswith(".mp4"):
            self.for_videos(request, an_id, filename)

        response += "Content-Type: multipart/form-data\r\nLocation: /\r\n\r\n".encode()

        return response

    def for_images(self, request: Request, an_id: str, filename: str):

        if ("Auth Token" not in request.cookies.keys()) or (request.cookies["Auth Token"] == ""):
            store_this = {"message": "<img src=\"/public/image/" + filename + "\" HEIGHT=150 alt=\"an image\" class=\"my_image\"/>",
                          "username": "Guest", "id": an_id}
            chat_collection.insert_one(store_this)
        elif ("Auth Token" in request.cookies.keys()) and (request.cookies["Auth Token"] != ""):
            sha256 = hashlib.sha256()
            sha256.update(request.cookies["Auth Token"].encode())
            hashing = sha256.hexdigest()
            find_user = user_collection.find_one({"authtoken": hashing})

            if find_user is not None:
                store_this = {"message": "<img src=\"/public/image/" + filename + "\" HEIGHT=150 alt=\"an image\" class=\"my_image\"/>",
                              "username": find_user["username"], "id": an_id}
                chat_collection.insert_one(store_this)
            else:
                store_this = {"message": "<img src=\"/public/image/" + filename + "\" HEIGHT=150 alt=\"an image\" class=\"my_image\"/>",
                              "username": "Guest", "id": an_id}
                chat_collection.insert_one(store_this)

    def for_videos(self, request: Request, an_id: str, filename: str):

        video_message = "<video width=\"400\" controls autoplay muted> <source src=\"/public/image/" + filename.replace("mp4", "mpd") + "\" type=\"application/x-mpegURL\"> <source src=\"/public/image/" + filename.replace("mp4", "m3u8") + "\" type=\"video/hls\"> <source src=\"/public/image/" + filename + "\" type=\"video/mp4\"> Your browser does not support video playback </video>"

        if ("Auth Token" not in request.cookies.keys()) or (request.cookies["Auth Token"] == ""):
            store_this = {"message": video_message, "username": "Guest", "id": an_id}
            chat_collection.insert_one(store_this)
        elif ("Auth Token" in request.cookies.keys()) and (request.cookies["Auth Token"] != ""):
            sha256 = hashlib.sha256()
            sha256.update(request.cookies["Auth Token"].encode())
            hashing = sha256.hexdigest()
            find_user = user_collection.find_one({"authtoken": hashing})

            if find_user is not None:
                store_this = {"message": video_message, "username": find_user["username"], "id": an_id}
                chat_collection.insert_one(store_this)
            else:
                store_this = {"message": video_message, "username": "Guest", "id": an_id}
                chat_collection.insert_one(store_this)

    def serve_error(self, request: Request):
        response = b''
        response += (request.http_version + " 404 Not Found\r\n").encode()

        for header in request.headers:
            response += (header + ": " + request.headers[header] + "\r\n").encode()

        response += "X-Content-Type-Options: nosniff\r\n".encode()

        response += "Content-Type: text/plain\r\nContent-Length: 54\r\n\r\nThis is an error page. Definitely not what you wanted.".encode()

        return response
