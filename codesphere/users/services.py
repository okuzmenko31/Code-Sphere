import binascii
import os


def get_clean_email(email):
    """This function returns email
    without all symbols after @"""
    email = email
    username = email.split('@')[0]
    return username


def generate_token():
    """
    This function returns 32 digits token.
    """
    return binascii.hexlify(os.urandom(16)).decode()
