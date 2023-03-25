import base64
from rest_framework.authentication import TokenAuthentication


class Bearer(TokenAuthentication):
    keyword = "Bearer"


def code_decoder(code, decode=False):
    if decode:
        return base64.b64decode(code).decode()
    else:
        return base64.b64encode(f"{code}".encode("utf-8")).decode()


# print(code_decoder("123"))
# print(code_decoder("MTIz", decode=True))
