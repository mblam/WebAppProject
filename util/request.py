class Request:

    def __init__(self, request: bytes):
        # TODO: parse the bytes of the request and populate the following instance variables

        decoding = request.decode()
        splitting = decoding.split('\r\n')
        split_one = splitting[0].split(' ')

        self.body = b""
        self.method = split_one[0]
        self.path = split_one[1]
        self.http_version = split_one[2]
        splitting.remove(splitting[0])

        self.headers = {}
        self.cookies = {}

        for elem in splitting:
            if "ookie" not in elem:
                mini_split = elem.split(' ')
                if mini_split[0].endswith(":"):
                    self.headers[mini_split[0].rstrip(":")] = mini_split[1]
            else:
                self.headers[elem[:elem.index(":")]] = elem.split(": ")[1]

        for key in self.headers:
            if "ookie" in key:
                cookies = self.headers[key].split("; ")
                for elem in cookies:
                    mini_split = elem.split("=")
                    self.cookies[mini_split[0]] = mini_split[1]


def test1():
    request = Request(b'GET / HTTP/1.1\r\nHost: localhost:8080\r\nConnection: keep-alive\r\n\r\n')
    assert request.method == "GET"
    assert "Host" in request.headers
    assert request.headers["Host"] == "localhost:8080"  # note: The leading space in the header value must be removed
    assert request.body == b""  # There is no body for this request.
    # When parsing POST requests, the body must be in bytes, not str

    # This is the start of a simple way (ie. no external libraries) to test your code.
    # It's recommended that you complete this test and add others, including at least one
    # test using a POST request. Also, ensure that the types of all values are correct


def test2():
    request = Request(b'GET / HTTP/1.1\r\nHost: www.example.re\r\nCookie: animal=cat; candy=chocolate\r\n\r\n')
    assert request.method == "GET"
    assert "Host" in request.headers
    assert request.body == b""  # There is no body for this request.
    assert "Cookie" in request.headers
    assert request.headers["Cookie"] == "animal=cat; candy=chocolate"
    assert "animal" in request.cookies
    assert request.cookies["animal"] == "cat"

# Request(b'POST /path HTTP/1.1\r\nContent-Type: text/plain\r\nCookie: color=pink; day=friday\r\nContent-Length: 5\r\n\r\nhello')
# assert request.method == "POST"
# assert "Content-Type" in request.headers
# assert request.body == b"hello"
# my header dict should look as following

if __name__ == '__main__':
    test1()
    test2()
