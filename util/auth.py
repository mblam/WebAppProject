from util.request import Request
import string


def extract_credentials(the_request: Request):
    credentials = []
    encoded = {"%21": "!", "%40": "@", "%23": "#", "%24": "$", "%25": "%", "%5E": "^", "%26": "&", "%28": "(", "%29": ")", "%2D": "-", "%5F": "_", "%3D": "="}

    request_body = the_request.body.decode()
    splitting = request_body.split("&")

    username = splitting[0].split("=")[1]
    credentials.append(username)

    password = splitting[1].split("=")[1]
    real_password = ""
    i = 0
    while i < len(password):
        if password[i] != "%":
            real_password += password[i]
        elif password[i] == "%":
            encode_char = password[i:i+3]
            real_password += encoded[encode_char]
            i += 2
        i += 1
    credentials.append(real_password)

    # print(credentials)
    return credentials


def validate_password(password: str):
    # checks password length
    if len(password) < 8:
        return False

    # checks for lowercase letters
    low_counter = 0
    for letter in string.ascii_lowercase:
        if letter in password:
            low_counter += 1
    if low_counter < 1:
        return False

    # checks for uppercase letters
    up_counter = 0
    for letter in string.ascii_uppercase:
        if letter in password:
            up_counter += 1
    if up_counter < 1:
        return False

    # checks for numbers
    num_counter = 0
    for num in string.digits:
        if num in password:
            num_counter += 1
    if num_counter < 1:
        return False

    # checks for special characters
    spec_chars = ['!', '@', '#', '$', '%', '^', '&', '(', ')', '-', '_', '=']
    spec_counter = 0
    for c in spec_chars:
        if c in password:
            spec_counter += 1
    if spec_counter < 1:
        return False

    # checks for invalid characters
    big_list = string.ascii_letters + string.digits + "".join(spec_chars)
    for letter in password:
        if letter not in big_list:
            return False

    return True

def test1():
    test_request = Request(b'POST /register HTTP/1.1\r\nHost: localhost:8080\r\nConnection: keep-alive\r\nContent-Length: 36\r\nCache-Control: max-age=0\r\nsec-ch-ua: "Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"\r\nsec-ch-ua-mobile: ?0\r\nsec-ch-ua-platform: "Windows"\r\nUpgrade-Insecure-Requests: 1\r\nOrigin: http://localhost:8080\r\nContent-Type: application/x-www-form-urlencoded\r\nUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7\r\nSec-Fetch-Site: same-origin\r\nSec-Fetch-Mode: navigate\r\nSec-Fetch-User: ?1\r\nSec-Fetch-Dest: document\r\nReferer: http://localhost:8080/\r\nAccept-Encoding: gzip, deflate, br, zstd\r\nAccept-Language: en-US,en;q=0.9\r\nCookie: Phpstorm-2f0d3793=51c22351-a32b-4b89-a59a-2b147e02533c; Pycharm-12a42513=00d92b2d-f7fb-4bb8-9356-e0b6e3929d15; Idea-1ae471f0=e383e67c-538c-462a-a6d1-65b7e321a710; visits=3\r\ndnt: 1\r\nsec-gpc: 1\r\n\r\nusername_reg=test&password_reg=c%25y')
    extract_credentials(test_request)

if __name__ == '__main__':
    test1()