class Request:

    def __init__(self, request: bytes):
        # TODO: parse the bytes of the request and populate the following instance variables

        decoding = request.decode()
        splitting = decoding.split('\r\n')
        split_one = splitting[0].split(' ')
        body = splitting[-1]
        splitting.remove(splitting[-1])
        # print(body)
        # print(splitting)

        self.body = b""
        self.method = split_one[0]
        self.path = split_one[1]
        self.http_version = split_one[2]
        splitting.remove(splitting[0])

        self.headers = {}
        self.cookies = {}

        for elem in splitting:
            if ("ookie" not in elem) and (":" in elem):
                mini_split = elem.split(': ')
                self.headers[mini_split[0]] = mini_split[1]
            elif "ookie" in elem:
                self.headers[elem[:elem.index(":")]] = elem.split(": ")[1]
            else:
                pass

        for key in self.headers:
            if "ookie" in key:
                cookies = self.headers[key].split("; ")
                for elem in cookies:
                    mini_split = elem.split("=")
                    self.cookies[mini_split[0]] = mini_split[1]

        if "Content-Length" in self.headers:
            self.body += body.encode()


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

def test3():
    request = Request(b'POST /path HTTP/1.1\r\nContent-Type: text/plain\r\nCookie: color=pink; day=friday\r\nContent-Length: 5\r\n\r\nhello')
    assert request.method == "POST"
    assert "Content-Type" in request.headers
    assert request.body == b"hello"

def test4():
    #this test is only for testing with print statements
    request = Request(b'GET /~mhertz/2024spring/cse442/stylesheet.php?page=tables HTTP/1.1\r\nAccept: text/css,*/*;q=0.1\r\nAccept-Encoding: gzip, deflate, br, zstd\r\nAccept-Language: en-US,en;q=0.9\r\nConnection: keep-alive\r\nCookie: nmstat=20b3e6e3-c053-c0f8-3547-f23cf4757e9f; _ga_CB14SJGJBF=GS1.1.1694821723.8.1.1694822678.0.0.0; _ga_J7VSG6CS88=GS1.1.1695341007.1.1.1695341036.0.0.0\r\nHost: cse.buffalo.edu\r\nPragma: no-cache\r\nReferer: https://cse.buffalo.edu/~mhertz/2024spring/cse442/\r\nSec-Fetch-Dest: style\r\nUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari')
    # for elem in request.headers:
    #     print(elem)
    #     print(request.headers[elem])

if __name__ == '__main__':
    test1()
    test2()
    test3()
    test4()
