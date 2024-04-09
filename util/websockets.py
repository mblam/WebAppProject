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
    hashing = sha1.digest()
    encoded = base64.b64encode(hashing)

    return encoded.decode()


def parse_ws_frame(ws_bytes: bytearray):
    
    
    return 0


def generate_ws_frame(ws_bytes):

    pass


def test1():
    my_list = [128, 150, 172, 100, 36, 106, 70]
    test_bytes = bytearray(my_list)
    print(test_bytes)
    parse_ws_frame(test_bytes)

if __name__ == '__main__':
    test1()