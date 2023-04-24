import binascii
import os

TOKEN_TYPES = (
    ('su', 'Sign Up Token'),
    ('ce', 'Change Email Token'),
    ('pr', 'Password Reset Token')
)


def get_clean_email(email):
    """This function returns email
    without all symbols after @"""
    email = email
    username = email.split('@')[0]
    return username


def generate_unique_token():
    """
    This function returns 32 digits token.
    """
    return binascii.hexlify(os.urandom(16)).decode()
