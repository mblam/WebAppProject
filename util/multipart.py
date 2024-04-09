from util.request import Request



class individual_part:

    def __init__(self, the_headers: dict, the_name: str, the_content: bytes):
        self.headers = the_headers
        self.name = the_name
        self.content = the_content


class the_multiparts:

    def __init__(self, the_boundary: str, the_parts: list):
        self.boundary = the_boundary
        self.parts = the_parts


def parse_multipart(request: Request):
    get_key = request.headers.get("Content-Type", None)
    if not get_key:
        error_response = (request.http_version + " 404 Not Found\r\n").encode()
        for header in request.headers:
            error_response += (header + ": " + request.headers[header] + "\r\n").encode()
        error_response += "X-Content-Type-Options: nosniff\r\n".encode()
        error_response += "Content-Type: text/plain\r\nContent-Length: 54\r\n\r\nThis is an error page. Definitely not what you wanted.".encode()
        return error_response

    parts_list = []  # a list for the parts of the multipart

    boundary = "--" + get_key.split("boundary=")[1]
    fst_bound = boundary + "\r\n"
    fin_bound = "\r\n" + boundary + "--"
    gen_bound = "\r\n" + boundary + "\r\n"
    data = request.body.replace(fst_bound.encode(), b'', 1)
    data2 = data.replace(fin_bound.encode(), b'')
    splitting = data2.split(gen_bound.encode())

    for elem in splitting:
        elem_split = elem.split(b'\r\n\r\n', 1)
        elem_dict = {}
        elem_content = b''

        elem_headers = elem_split[0].split(b'\r\n')
        for item in elem_headers:
            if ": ".encode() in item:
                elem_dict[item.split(": ".encode())[0].decode()] = item.split(": ".encode())[1].decode()

        elem_content += elem_split[1]

        # print(elem_dict["Content-Disposition"])
        i = 17
        elem_name = ""
        while elem_dict["Content-Disposition"][i] != '"':
            elem_name += elem_dict["Content-Disposition"][i]
            i += 1
        # print(elem_name)

        new_part = individual_part(elem_dict, elem_name, elem_content)
        parts_list.append(new_part)

    parsed_multipart = the_multiparts(get_key.split("boundary=")[1], parts_list)

    return parsed_multipart


def test1():
    request = Request(b'POST /form-path HTTP/1.1\r\nContent-Length: 9937\r\nContent-Type: multipart/form-data; boundary=----WebKitFormBoundarycriD3u6M0UuPR1ia\r\n\r\n------WebKitFormBoundarycriD3u6M0UuPR1ia\r\nContent-Disposition: form-data; name="commenter"\r\n\r\nJesse\r\n------WebKitFormBoundarycriD3u6M0UuPR1ia\r\nContent-Disposition: form-data; name="upload"; filename="discord.png"\r\nContent-Type: image/png\r\n\r\n<bytes_of_\r\n\r\nthe_file>\r\n------WebKitFormBoundarycriD3u6M0UuPR1ia--\r\n\r\n')
    testing = parse_multipart(request)
    assert testing.boundary == "----WebKitFormBoundarycriD3u6M0UuPR1ia"

    # print(testing.parts[0].headers)
    # print(testing.parts[0].name)
    # print(testing.parts[0].content)
    #
    # print(testing.parts[1].headers)
    # print(testing.parts[1].name)
    # print(testing.parts[1].content)

def test2():
    request = Request(b'POST /profile-pic HTTP/1.1\r\nHost: localhost:8080\r\nConnection: keep-alive\r\nContent-Length: 673\r\nCache-Control: max-age=0\r\nsec-ch-ua: "Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"\r\nsec-ch-ua-mobile: ?0\r\nsec-ch-ua-platform: "Windows"\r\nUpgrade-Insecure-Requests: 1\r\nOrigin: http://localhost:8080\r\nContent-Type: multipart/form-data; boundary=----WebKitFormBoundaryZT0lyGDzNmrp1kg7\r\nUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7\r\nSec-Fetch-Site: same-origin\r\nSec-Fetch-Mode: navigate\r\nSec-Fetch-User: ?1\r\nSec-Fetch-Dest: document\r\nReferer: http://localhost:8080/\r\nAccept-Encoding: gzip, deflate, br, zstd\r\nAccept-Language: en-US,en;q=0.9\r\nCookie: Pycharm-12a42513=00d92b2d-f7fb-4bb8-9356-e0b6e3929d15; visits=1\r\ndnt: 1\r\nsec-gpc: 1\r\n\r\n------WebKitFormBoundaryZT0lyGDzNmrp1kg7\r\nContent-Disposition: form-data; name="upload"; filename="elephant-small.jpg"\r\nContent-Type: image/jpeg\r\n\r\n\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x00\x00\x01\x00\x01\x00\x00\xff\xdb\x00\x84\x00\x10\x10\x10\x10\x11\x10\x12\x14\x14\x12\x19\x1b\x18\x1b\x19%"\x1f\x1f"%8(+(+(8U5>55>5UK[JEJ[K\x87j^^j\x87\x9c\x83|\x83\x9c\xbd\xa9\xa9\xbd\xee\xe2\xee\xff\xff\xff\x01\x10\x10\x10\x10\x11\x10\x12\x14\x14\x12\x19\x1b\x18\x1b\x19%"\x1f\x1f"%8(+(+(8U5>55>5UK[JEJ[K\x87j^^j\x87\x9c\x83|\x83\x9c\xbd\xa9\xa9\xbd\xee\xe2\xee\xff\xff\xff\xff\xc2\x00\x11\x08\x00\x18\x00\x18\x03\x01"\x00\x02\x11\x01\x03\x11\x01\xff\xc4\x00\x16\x00\x01\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x07\x04\x05\xff\xda\x00\x08\x01\x01\x00\x00\x00\x00\xd4\x8e\x9ds\x85\x0b\x8f\x90\x7f\xff\xc4\x00\x15\x01\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\xff\xda\x00\x08\x01\x02\x10\x00\x00\x00\x95?\xff\xc4\x00\x15\x01\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\xff\xda\x00\x08\x01\x03\x10\x00\x00\x00\xa9?\xff\xc4\x00&\x10\x00\x02\x01\x02\x05\x02\x07\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x03\x04\x00\x12\x01\x05\x10\x13B"2\x14!$3\x82\x92\xa2\xff\xda\x00\x08\x01\x01\x00\x01?\x00\xccf\xcc\xdf \xbc\xd0\x03\xdbo*<\xd5\xe3\x16\xfc^^]7V\\\xf7o\xab\x055\xac\x12\xee\xbb\xf5Y\xc4_\x13\t\xb6{\x807\r \x9e\xf1\x08\xf8r=\xbf\xb5C\x84\x98J\xb1\x7f"\xc7HHh\xce\x83\xb9\x10\xd5\xea\xc8\x88\xad\xe3\xd3n\x9f\xff\xc4\x00\x14\x11\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00 \xff\xda\x00\x08\x01\x02\x01\x01?\x00\x1f\xff\xc4\x00\x14\x11\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00 \xff\xda\x00\x08\x01\x03\x01\x01?\x00\x1f\xff\xd9\r\n------WebKitFormBoundaryZT0lyGDzNmrp1kg7--\r\n')
    testing = parse_multipart(request)
    assert testing.boundary == "----WebKitFormBoundaryZT0lyGDzNmrp1kg7"
    # print(testing.boundary)
    # print(testing.parts)
    # print(testing.parts[0].headers)
    # print(testing.parts[0].content)
    # print(testing.parts[0].name)

def test3():
    request = Request(b'POST /form-path HTTP/1.1\r\nHost: localhost:8080\r\nConnection: keep-alive\r\nContent-Length: 673\r\nCache-Control: max-age=0\r\nsec-ch-ua: "Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"\r\nsec-ch-ua-mobile: ?0\r\nsec-ch-ua-platform: "Windows"\r\nUpgrade-Insecure-Requests: 1\r\nOrigin: http://localhost:8080\r\nContent-Type: multipart/form-data; boundary=----WebKitFormBoundarydzEiGtKXmrZVnEAJ\r\nUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7\r\nSec-Fetch-Site: same-origin\r\nSec-Fetch-Mode: navigate\r\nSec-Fetch-User: ?1\r\nSec-Fetch-Dest: document\r\nReferer: http://localhost:8080/\r\nAccept-Encoding: gzip, deflate, br, zstd\r\nAccept-Language: en-US,en;q=0.9\r\nCookie: Pycharm-12a42513=00d92b2d-f7fb-4bb8-9356-e0b6e3929d15; visits=2\r\ndnt: 1\r\nsec-gpc: 1\r\n\r\n------WebKitFormBoundarydzEiGtKXmrZVnEAJ\r\nContent-Disposition: form-data; name="upload"; filename="elephant-small.jpg"\r\nContent-Type: image/jpeg\r\n\r\n\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x00\x00\x01\x00\x01\x00\x00\xff\xdb\x00\x84\x00\x10\x10\x10\x10\x11\x10\x12\x14\x14\x12\x19\x1b\x18\x1b\x19%"\x1f\x1f"%8(+(+(8U5>55>5UK[JEJ[K\x87j^^j\x87\x9c\x83|\x83\x9c\xbd\xa9\xa9\xbd\xee\xe2\xee\xff\xff\xff\x01\x10\x10\x10\x10\x11\x10\x12\x14\x14\x12\x19\x1b\x18\x1b\x19%"\x1f\x1f"%8(+(+(8U5>55>5UK[JEJ[K\x87j^^j\x87\x9c\x83|\x83\x9c\xbd\xa9\xa9\xbd\xee\xe2\xee\xff\xff\xff\xff\xc2\x00\x11\x08\x00\x18\x00\x18\x03\x01"\x00\x02\x11\x01\x03\x11\x01\xff\xc4\x00\x16\x00\x01\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x07\x04\x05\xff\xda\x00\x08\x01\x01\x00\x00\x00\x00\xd4\x8e\x9ds\x85\x0b\x8f\x90\x7f\xff\xc4\x00\x15\x01\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\xff\xda\x00\x08\x01\x02\x10\x00\x00\x00\x95?\xff\xc4\x00\x15\x01\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\xff\xda\x00\x08\x01\x03\x10\x00\x00\x00\xa9?\xff\xc4\x00&\x10\x00\x02\x01\x02\x05\x02\x07\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x03\x04\x00\x12\x01\x05\x10\x13B"2\x14!$3\x82\x92\xa2\xff\xda\x00\x08\x01\x01\x00\x01?\x00\xccf\xcc\xdf \xbc\xd0\x03\xdbo*<\xd5\xe3\x16\xfc^^]7V\\\xf7o\xab\x055\xac\x12\xee\xbb\xf5Y\xc4_\x13\t\xb6{\x807\r \x9e\xf1\x08\xf8r=\xbf\xb5C\x84\x98J\xb1\x7f"\xc7HHh\xce\x83\xb9\x10\xd5\xea\xc8\x88\xad\xe3\xd3n\x9f\xff\xc4\x00\x14\x11\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00 \xff\xda\x00\x08\x01\x02\x01\x01?\x00\x1f\xff\xc4\x00\x14\x11\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00 \xff\xda\x00\x08\x01\x03\x01\x01?\x00\x1f\xff\xd9\r\n------WebKitFormBoundarydzEiGtKXmrZVnEAJ--\r\n')
    testing = parse_multipart(request)
    assert testing.boundary == "----WebKitFormBoundarydzEiGtKXmrZVnEAJ"

if __name__ == '__main__':
    test1()
    test2()
    test3()
