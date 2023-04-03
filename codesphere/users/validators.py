from django import forms
import re


class CustomPasswordValidation:

    @staticmethod
    def validate_password_length(password):
        if len(password) < 9:
            raise forms.ValidationError('The password is too short!')
        if len(password) > 15:
            raise forms.ValidationError('The password is too long!')

    @staticmethod
    def validate_numbers(password):
        if not re.findall('\d', password):
            raise forms.ValidationError('In password must be at least 1 number!')

    @staticmethod
    def validate_lowercase(password):
        if not re.findall('[a-z]', password):
            raise forms.ValidationError('In password must be at least one letter in lowercase!')

    @staticmethod
    def validate_uppercase(password):
        if not re.findall('[A-Z]', password):
            raise forms.ValidationError('In password must be at least one letter in uppercase!')

    @staticmethod
    def validate_latin_letters(password):
        if not bool(re.match('[a-zA-Z 0-9]*$', password)):
            raise forms.ValidationError(
                'Password must be in English! It can only contain Latin characters and numbers.')

    def validate_password(self, password):
        self.validate_password_length(password)
        self.validate_numbers(password)
        self.validate_lowercase(password)
        self.validate_uppercase(password)
        self.validate_latin_letters(password)
