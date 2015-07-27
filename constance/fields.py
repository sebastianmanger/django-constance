# -*- coding: utf-8 -*-
from django.core.validators import EmailValidator
from django.forms import CharField, Textarea
from django.utils.translation import ugettext_lazy as _

from . import settings


class EmailListValue(CharField):
    """Validate a list of emails, display it as a single string."""
    widget = Textarea

    def validate(self, value):
        super(EmailListValue, self).validate(value)
        # map(lambda email: validate_email(email.strip()), value)
        # This probably is more explicit than the above.
        for email_value in value:
            EmailValidator(_('%s is not a valid email address') % email_value)(email_value.strip())
        return value

    def prepare_value(self, value):
        return settings.EMAIL_VALUES_SEPARATOR.join(value) if isinstance(value, list) else value

    def to_python(self, value):
        if not value:
            return
        if isinstance(value, list):
            return value
        return value.split(settings.EMAIL_VALUES_SEPARATOR)
