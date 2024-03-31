from util.request import Request


class the_multiparts:

    def __init__(self, the_boundary):
        self.boundary = the_boundary
        self.parts = []

    def add_a_part(self, a_part):
        return self.parts.append(a_part)


class individual_part:

    def __init__(self, the_headers, the_name, the_content):
        self.headers = the_headers
        self.name = the_name
        self.content = the_content


def parse_multipart(request: Request):

    splitting = request.headers["Content-Type"].split('; ')[1].split("boundary=")[1]
    parsed_multipart = the_multiparts(splitting)

    decoded = request.body.decode()
    # print(decoded)
    split_body = decoded.split("--" + splitting)
    split_body.pop(0)
    split_body.pop(-1)

    for elem in split_body:
        new_part = individual_part({}, "", b'')
        mini_split = elem.split('\r\n')
        mini_split.pop(0)
        mini_split.pop(-1)

        get_bytes = []
        for item in mini_split:
            if ": " in item:
                split_more = item.split(": ")
                new_part.headers[split_more[0]] = split_more[1]
            else:
                get_bytes.append(item)

        get_name = new_part.headers["Content-Disposition"].split('"')
        new_part.name = get_name[1]

        get_bytes.pop(0)
        for thing in get_bytes:
            if thing == '':
                new_part.content += "\r\n\r\n".encode()
            else:
                new_part.content += thing.encode()

        parsed_multipart.add_a_part(new_part)

    return parsed_multipart


def test1():
    request = Request(b'POST /form-path HTTP/1.1\r\nContent-Length: 9937\r\nContent-Type: multipart/form-data; boundary=----WebKitFormBoundarycriD3u6M0UuPR1ia\r\n\r\n------WebKitFormBoundarycriD3u6M0UuPR1ia\r\nContent-Disposition: form-data; name="commenter"\r\n\r\nJesse\r\n------WebKitFormBoundarycriD3u6M0UuPR1ia\r\nContent-Disposition: form-data; name="upload"; filename="discord.png"\r\nContent-Type: image/png\r\n\r\n<bytes_of\r\n\r\n_the_file>\r\n------WebKitFormBoundarycriD3u6M0UuPR1ia--\r\n\r\n')
    testing = parse_multipart(request)
    assert testing.boundary == "----WebKitFormBoundarycriD3u6M0UuPR1ia"

    # print(testing.parts[0].headers)
    # print(testing.parts[0].name)
    # print(testing.parts[0].content)
    #
    # print(testing.parts[1].headers)
    # print(testing.parts[1].name)
    # print(testing.parts[1].content)


if __name__ == '__main__':
    test1()
