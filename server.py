import socketserver
from util.request import Request


class MyTCPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        received_data = self.request.recv(2048)
        print(self.client_address)
        print("--- received data ---")
        print(received_data)
        print("--- end of data ---\n\n")
        request = Request(received_data)

        # TODO: Parse the HTTP request and use self.request.sendall(response) to send your response
        response = b''

        if request.path == "/public/favicon.ico":
            response += (request.http_version + " 200 OK\r\n").encode()

            favicon = open("public/favicon.ico", "rb")
            favicon_bytes = str(len(favicon.read()))
            response += ("Content-Type: image/x-icon\r\nContent-Length: " + favicon_bytes + "\r\n\r\n").encode()

            response += open("public/favicon.ico", "rb").read()

        if request.path == "/public/functions.js":
            response += (request.http_version + " 200 OK\r\n").encode()

            for header in request.headers:
                response += (header + ": " + request.headers[header] + "\r\n").encode()

            response += "Content-Type: text/javascript".encode()

            open_file = open("public/functions.js", "rb").read()
            byte_num = str(len(open_file))
            response += ("\r\nContent Length: " + byte_num).encode()

            response += "\r\n\r\n".encode() + open_file

        if request.path == "/":
            response += (request.http_version + " 200 OK\r\n").encode()

            for header in request.headers:
                response += (header + ": " + request.headers[header] + "\r\n").encode()

            response += "Content-Type: text/html".encode()

            open_file = open("public/index.html", "rb").read()
            byte_num = str(len(open_file))
            response += ("\r\nContent Length: " + byte_num).encode()

            response += "\r\n\r\n".encode() + open_file

        if request.path == "/public/style.css":
            response += (request.http_version + " 200 OK\r\n").encode()

            for header in request.headers:
                response += (header + ": " + request.headers[header] + "\r\n").encode()

            response += "Content-Type: text/css".encode()

            open_file = open("public/style.css", "rb").read()
            byte_num = str(len(open_file))
            response += ("\r\nContent Length: " + byte_num).encode()

            response += "\r\n\r\n".encode() + open_file

        if request.path == "/public/webrtc.js":
            response += (request.http_version + " 200 OK\r\n").encode()

            for header in request.headers:
                response += (header + ": " + request.headers[header] + "\r\n").encode()

            response += "Content-Type: text/javascript".encode()

            open_file = open("public/webrtc.js", "rb").read()
            byte_num = str(len(open_file))
            response += ("\r\nContent Length: " + byte_num).encode()

            response += "\r\n\r\n".encode() + open_file

        if request.path == "/public/image/eagle.jpg":
            response += (request.http_version + " 200 OK\r\n").encode()

            eagle_img = open("public/image/eagle.jpg", "rb")
            eagle_bytes = str(len(eagle_img.read()))
            response += ("Content-Type: image/jpeg\r\nContent-Length:" + eagle_bytes + "\r\n\r\n").encode()

            response += open("public/image/eagle.jpg", "rb").read()

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
