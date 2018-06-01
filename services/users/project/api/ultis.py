import re

from flask import make_response, jsonify
from validate_email import validate_email
from project.api.constant import BAD_REQUEST, ACCESS_FORBIDDEN, MSG_EMAIL_EMPTY_ERROR, MSG_EMAIL_INVALID, \
    MSG_USER_TOO_SHORT, PASSWORD_ERROR, PASSWORD_ERROR_NOT_MATCH


def validate_user_data(email, user_name, password, re_password):
    print(email, user_name, password, re_password)
    response_object = None
    if not email:
        response_object = {
            'code': BAD_REQUEST,
            'message': MSG_EMAIL_EMPTY_ERROR
        }

    email_is_valid = validate_email(email)
    if not email_is_valid:
        response_object = {
            'code': BAD_REQUEST,
            'message': MSG_EMAIL_INVALID
        }

    if len(user_name) < 6:
        response_object = {
            'code': BAD_REQUEST,
            'message': MSG_USER_TOO_SHORT
        }

    password_ok = check_password(password)
    if not password_ok:
        response_object = {
            'code': BAD_REQUEST,
            'message': PASSWORD_ERROR
        }

    password_match = check_re_password(password, re_password)
    if password_match is False:
        response_object = {
            'code': BAD_REQUEST,
            'message': PASSWORD_ERROR_NOT_MATCH
        }
    return response_object



def make_response_user_service(http_code, message, status):
    """

    :param http_code:
    :param message:
    :param status:
    :return:
    """
    pass


def check_password(password):
    """
    Verify the strength of 'password'
    :param password
    :return: boolean
    """
    # check length
    length_error = len(password) < 8
    # searching for
    number_error = re.search(r"[0-9]", password) is None
    # searching for upper case
    uppercase_error = re.search(r"[A-Z]", password) is None
    # searching for lowercase
    lowercase_error = re.search(r"[a-z]", password) is None
    # searching for symbols
    symbol_error = re.search(r"[ !#$%@&'()*+,-./[\\\]^_`{|}~" + r'"]', password) is None
    print(length_error, number_error, uppercase_error, lowercase_error, symbol_error)
    # overall result
    password_ok = not (length_error or number_error or uppercase_error or lowercase_error or symbol_error)

    return password_ok


def check_re_password(password, re_password):
    """
    Compare password
    :param password:
    :param re_password:
    :return: boolean
    """
    if password == re_password:
        return True
    return False
