from django.core.exceptions import ValidationError
from six import string_types
import re


def phone_validator(number):
    if isinstance(number, string_types):
        rule = re.compile(r'^(?:(?:\+|0{0,2})91(\s*[\-]\s*)?|[0]?)?[789]\d{9}$')
        if not rule.search(number):
            msg = 'Invalid phone number'
            raise ValidationError(msg)
    else:
        raise ValidationError


def aadhar_validator(number):
    if isinstance(number, string_types):
        rule = re.compile(r'^\d{12}$')
        if not rule.search(number):
            msg = 'Invalid aadhar number'
            raise ValidationError(msg)
    else:
        raise ValidationError
