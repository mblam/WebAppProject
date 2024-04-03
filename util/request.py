class Request:

    def __init__(self, request: bytes):
        # TODO: parse the bytes of the request and populate the following instance variables
        find_bytes = request.split(b'\r\n\r\n', 1)
        # print(find_bytes)
        splitting = find_bytes[0].decode().split('\r\n')
        split_one = splitting[0].split(" ")  # To get method, path, and http version
        # print(split_one)

        # Getting the last item in splitting before removing it
        # end_splitting = splitting[-1]
        # splitting.remove(splitting[-1])

        self.body = b""
        self.method = split_one[0]
        self.path = split_one[1]
        self.http_version = split_one[2]
        # splitting.remove(splitting[0])  # Removes first elem because it is no longer needed

        # self.after_path = splitting  # to help with multipart parsing possibly (just in case)

        self.headers = {}
        self.cookies = {}

        # been_split = decoding.split('\r\n\r\n')  # To get part with only the headers
        # split_headers = been_split[0].split('\r\n')  # Getting each header on its own
        # Loop through to get headers, while making sure all cookies are accounted for
        for elem in splitting:
            if ("ookie" not in elem) and (":" in elem):
                mini_split = elem.split(': ')
                if mini_split[0] not in self.headers.keys():
                    self.headers[mini_split[0]] = mini_split[1]
            elif "ookie" in elem:
                self.headers[elem[:elem.index(":")]] = elem.split(": ")[1]
            else:
                pass

        # Loop through headers to find all cookies
        for key in self.headers:
            if "ookie" in key:
                cookies = self.headers[key].split("; ")
                for elem in cookies:
                    mini_split = elem.split("=")
                    self.cookies[mini_split[0]] = mini_split[1]

        # if (self.headers.get("Content-Type") is not None) and (self.headers.get("Content-Type").startswith("multipart/form-data")):
        #     find_bytes = request.find(b'\r\n\r\n')
        #     self.body += request[find_bytes+4:len(request)-4]
        # else:
        #     self.body += request[find_bytes+4:len(request)]
        self.body = find_bytes[1]

    def add_to_body(self, data):
        self.body += data


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

# def test4():
#     #this test is only for testing with print statements
#     request = Request(b'GET /~mhertz/2024spring/cse442/stylesheet.php?page=tables HTTP/1.1\r\nAccept: text/css,*/*;q=0.1\r\nAccept-Encoding: gzip, deflate, br, zstd\r\nAccept-Language: en-US,en;q=0.9\r\nConnection: keep-alive\r\nCookie: nmstat=20b3e6e3-c053-c0f8-3547-f23cf4757e9f; _ga_CB14SJGJBF=GS1.1.1694821723.8.1.1694822678.0.0.0; _ga_J7VSG6CS88=GS1.1.1695341007.1.1.1695341036.0.0.0\r\nHost: cse.buffalo.edu\r\nPragma: no-cache\r\nReferer: https://cse.buffalo.edu/~mhertz/2024spring/cse442/\r\nSec-Fetch-Dest: style\r\nUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari')
#     # for elem in request.headers:
#     #     print(elem)
#     #     print(request.headers[elem])

def test5():
    # this test is only for testing with multipart
    # request = Request(b'POST /form-path HTTP/1.1\r\nContent-Length: 252\r\nContent-Type: multipart/form-data; boundary=----WebKitFormBoundaryfkz9sCA6fR3CAHN4\r\n------WebKitFormBoundaryfkz9sCA6fR3CAHN4\r\nContent-Disposition: form-data; name="commenter"\r\nJesse\r\n------WebKitFormBoundaryfkz9sCA6fR3CAHN4\r\nContent-Disposition: form-data; name="comment"\r\nGood morning!\r\n------WebKitFormBoundaryfkz9sCA6fR3CAHN4--')
    # request = Request(b'POST /form-path HTTP/1.1\r\nContent-Length: 10000\r\nContent-Type: multipart/form-data; boundary=----thisboundary\r\n\r\n------thisboundary\r\nContent-Disposition: form-data; name="commenter"\r\n\r\nJesse\r\n------thisboundary\r\nContent-Disposition: form-data; name="upload"; filename="cat.png"\r\nContent-Type: image/png\r\n\r\n<bytes_of_file>\r\n------thisboundary--')
    request = Request(b'POST /form-path HTTP/1.1\r\nContent-Length: 9937\r\nContent-Type: multipart/form-data; boundary=----WebKitFormBoundarycriD3u6M0UuPR1ia\r\n\r\n------WebKitFormBoundarycriD3u6M0UuPR1ia\r\nContent-Disposition: form-data; name="commenter"\r\n\r\nJesse\r\n------WebKitFormBoundarycriD3u6M0UuPR1ia\r\nContent-Disposition: form-data; name="upload"; filename="discord.png"\r\nContent-Type: image/png\r\n\r\n<bytes_of_the_file>\r\n------WebKitFormBoundarycriD3u6M0UuPR1ia--\r\n\r\n')
    print(request.body)
    # for elem in request.headers:
    #     print(elem + ": " + request.headers[elem])
    print(request.headers)
    #
    # print(request.after_path)

def test6():
    request = Request(b'POST /profile-pic HTTP/1.1\r\nHost: localhost:8080\r\nConnection: keep-alive\r\nContent-Length: 673\r\nCache-Control: max-age=0\r\nsec-ch-ua: "Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"\r\nsec-ch-ua-mobile: ?0\r\nsec-ch-ua-platform: "Windows"\r\nUpgrade-Insecure-Requests: 1\r\nOrigin: http://localhost:8080\r\nContent-Type: multipart/form-data; boundary=----WebKitFormBoundaryZT0lyGDzNmrp1kg7\r\nUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7\r\nSec-Fetch-Site: same-origin\r\nSec-Fetch-Mode: navigate\r\nSec-Fetch-User: ?1\r\nSec-Fetch-Dest: document\r\nReferer: http://localhost:8080/\r\nAccept-Encoding: gzip, deflate, br, zstd\r\nAccept-Language: en-US,en;q=0.9\r\nCookie: Pycharm-12a42513=00d92b2d-f7fb-4bb8-9356-e0b6e3929d15; visits=1\r\ndnt: 1\r\nsec-gpc: 1\r\n\r\n------WebKitFormBoundaryZT0lyGDzNmrp1kg7\r\nContent-Disposition: form-data; name="upload"; filename="elephant-small.jpg"\r\nContent-Type: image/jpeg\r\n\r\n\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x00\x00\x01\x00\x01\x00\x00\xff\xdb\x00\x84\x00\x10\x10\x10\x10\x11\x10\x12\x14\x14\x12\x19\x1b\x18\x1b\x19%"\x1f\x1f"%8(+(+(8U5>55>5UK[JEJ[K\x87j^^j\x87\x9c\x83|\x83\x9c\xbd\xa9\xa9\xbd\xee\xe2\xee\xff\xff\xff\x01\x10\x10\x10\x10\x11\x10\x12\x14\x14\x12\x19\x1b\x18\x1b\x19%"\x1f\x1f"%8(+(+(8U5>55>5UK[JEJ[K\x87j^^j\x87\x9c\x83|\x83\x9c\xbd\xa9\xa9\xbd\xee\xe2\xee\xff\xff\xff\xff\xc2\x00\x11\x08\x00\x18\x00\x18\x03\x01"\x00\x02\x11\x01\x03\x11\x01\xff\xc4\x00\x16\x00\x01\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x07\x04\x05\xff\xda\x00\x08\x01\x01\x00\x00\x00\x00\xd4\x8e\x9ds\x85\x0b\x8f\x90\x7f\xff\xc4\x00\x15\x01\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\xff\xda\x00\x08\x01\x02\x10\x00\x00\x00\x95?\xff\xc4\x00\x15\x01\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\xff\xda\x00\x08\x01\x03\x10\x00\x00\x00\xa9?\xff\xc4\x00&\x10\x00\x02\x01\x02\x05\x02\x07\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x03\x04\x00\x12\x01\x05\x10\x13B"2\x14!$3\x82\x92\xa2\xff\xda\x00\x08\x01\x01\x00\x01?\x00\xccf\xcc\xdf \xbc\xd0\x03\xdbo*<\xd5\xe3\x16\xfc^^]7V\\\xf7o\xab\x055\xac\x12\xee\xbb\xf5Y\xc4_\x13\t\xb6{\x807\r \x9e\xf1\x08\xf8r=\xbf\xb5C\x84\x98J\xb1\x7f"\xc7HHh\xce\x83\xb9\x10\xd5\xea\xc8\x88\xad\xe3\xd3n\x9f\xff\xc4\x00\x14\x11\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00 \xff\xda\x00\x08\x01\x02\x01\x01?\x00\x1f\xff\xc4\x00\x14\x11\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00 \xff\xda\x00\x08\x01\x03\x01\x01?\x00\x1f\xff\xd9\r\n------WebKitFormBoundaryZT0lyGDzNmrp1kg7--\r\n')
    assert request.path == "/profile-pic"

if __name__ == '__main__':
    test1()
    # test2()
    # test3()
    # test4()
    # test5()
    # test6()
