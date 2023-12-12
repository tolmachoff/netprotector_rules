import base64


def encode(text: str) -> str:
    res = base64.encodebytes(text.encode())
    res_str = res.decode()
    return res_str
