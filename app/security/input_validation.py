import re


def sanitize_input(value):

    value = value.strip()

    value = re.sub(r'[<>]', '', value)

    return value