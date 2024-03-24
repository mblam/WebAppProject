from util.request import Request


class the_multipart:

    def __int__(self, boundary, parts):
        self.boundary = boundary
        self.parts = parts


def parse_multipart(request: Request):
    the_boundary = ""
    the_parts = []

    parsed_multipart = the_multipart()
    parsed_multipart.boundary = the_boundary
    parsed_multipart.parts = the_parts

    return parsed_multipart
