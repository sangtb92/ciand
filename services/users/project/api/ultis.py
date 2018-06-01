import re


def check_password(password):
    """
    Verify the strength of 'password'
    :param password:
    :return:
    """

    length_error = len(password) < 8

    digit_error = re.search(r"/d", password) is None

    # searching for upper case
    uppercase_error = re.search(r"[A-Z]", password) is None

    # searching for lowercase
    lowercase_error = re.search(r"[a-z]", password) is None

    # searching for symbols
    symbol_error = re.search(r"[ !#$%&'()*+,-./[\\\]^_`{|}~" + r'"]', password) is None

    # overall result
    password_ok = not (length_error or digit_error or uppercase_error or lowercase_error or symbol_error)
