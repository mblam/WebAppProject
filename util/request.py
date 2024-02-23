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
            mini_split = elem.split(' ')
            if mini_split[0].endswith(":"):
                self.headers[mini_split[0].rstrip(":")] = mini_split[1]
            if (mini_split[0].lower() == "set-cookie:") or (mini_split[0].lower() == "cookie:"):
                further_split = mini_split[1].split("=")
                self.cookies[further_split[0]] = further_split[1]


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


if __name__ == '__main__':
    test1()
