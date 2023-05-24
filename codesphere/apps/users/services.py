import json


def clean_email(email: str) -> str:
    return email.split('@')[0].lower()


def social_media_json():
    return {
        'twitter': '',
        'github': '',
        'facebook': '',
        'instagram': ''
    }


def settings_json():
    return {
        'theme': ''
    }


def get_from_json(json_dict: str):
    if isinstance(json_dict, str):
        return json.loads(json_dict)
    return json_dict
