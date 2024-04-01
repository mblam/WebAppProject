from util.request import Request
from util.the_paths import Paths


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
    paths = Paths()  # just to return error if needed
    get_key = request.headers.get("Content-Type", None)
    if not get_key:
        return paths.serve_error(request)

    parts_list = []

    boundary = "--" + get_key.split("boundary=")[1]
    parsed_multipart = the_multiparts(get_key.split("boundary=")[1], [])
    fst_bound = boundary + "\r\n"
    fin_bound = "\r\n" + boundary + "--"
    gen_bound = "\r\n" + boundary + "\r\n"
    data = request.body.replace(fst_bound.encode(), b'', 1)
    data2 = data.replace(fin_bound.encode(), b'')
    splitting = data2.split(gen_bound.encode())

    for elem in splitting:
        elem_split = elem.split(b'\r\n\r\n')
        elem_dict = {}
        elem_content = b''

        elem_headers = elem_split[0].split(b'\r\n')
        for item in elem_headers:
            if ": ".encode() in item:
                elem_dict[item.split(": ".encode())[0].decode()] = item.split(": ".encode())[1].decode()

        find_bytes = elem.find(b'\r\n\r\n')
        elem_content += elem[find_bytes+4:]

        elem_name = elem_dict["Content-Disposition"].split('"')[1]

        new_part = individual_part(elem_dict, elem_name, elem_content)
        parts_list.append(new_part)

    return parsed_multipart


def test1():
    request = Request(b'POST /form-path HTTP/1.1\r\nContent-Length: 9937\r\nContent-Type: multipart/form-data; boundary=----WebKitFormBoundarycriD3u6M0UuPR1ia\r\n\r\n------WebKitFormBoundarycriD3u6M0UuPR1ia\r\nContent-Disposition: form-data; name="commenter"\r\n\r\nJesse\r\n------WebKitFormBoundarycriD3u6M0UuPR1ia\r\nContent-Disposition: form-data; name="upload"; filename="discord.png"\r\nContent-Type: image/png\r\n\r\n<bytes_of_the_file>\r\n------WebKitFormBoundarycriD3u6M0UuPR1ia--\r\n\r\n')
    testing = parse_multipart(request)
    assert testing.boundary == "----WebKitFormBoundarycriD3u6M0UuPR1ia"

#     print(testing.parts[0].headers)
#     print(testing.parts[0].name)
#     print(testing.parts[0].content)
#
#     print(testing.parts[1].headers)
#     print(testing.parts[1].name)
#     print(testing.parts[1].content)
#
# def test2():
#     request = Request(b'POST /form-path HTTP/1.1\r\nContent-Length: 252\r\nContent-Type: multipart/form-data; boundary=----WebKitFormBoundaryfkz9sCA6fR3CAHN4\r\n\r\n------WebKitFormBoundaryfkz9sCA6fR3CAHN4\r\nContent-Disposition: form-data; name="commenter"\r\n\r\nJesse\r\n------WebKitFormBoundaryfkz9sCA6fR3CAHN4--\r\n\r\n')
#     testing = parse_multipart((request))
#     print(testing.boundary)
#     print(testing.parts)
#     print(testing.parts[0].headers)
#     print(testing.parts[0].content)


if __name__ == '__main__':
    test1()
    # test2()
