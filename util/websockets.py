import hashlib
import base64


class websocket_frame:

    def __init__(self, fin, op, pl_len, pl):
        self.fin_bit = fin
        self.opcode = op
        self.payload_length = pl_len
        self.payload = pl


def compute_accept(key: str):
    sha1 = hashlib.sha1()
    hash_this = key + "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
    sha1.update(hash_this.encode())
    hashing = sha1.hexdigest()
    encoded = base64.b64encode(hashing)

    return str(encoded)


def parse_ws_frame(ws_bytes: bytearray):
    the_bytes = ws_bytes.decode('utf-8').encode('utf-8')
    
    pass


def generate_ws_frame(ws_bytes):

    pass

