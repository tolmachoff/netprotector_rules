import re


MESSAGE_PATTERN = r".*msg:\s*\"(.*?)\".*"


def get_message(text: str):
    res = re.search(MESSAGE_PATTERN, text)
    if res:
        msg = res.groups()[0]
    else:
        msg = "ERROR MESSAGE"

    return msg


def get_protocol(text: str):
    words = text.split()
    if len(words) > 1:
        protocol = words[1]
    else:
        protocol = ""

    return protocol
