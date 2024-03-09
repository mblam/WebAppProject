from util.request import Request


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

    def serve_image(self, request: Request):
        response = b''

        return response

    def serve_favicon(self, request: Request):
        response = b''

        return response
