# coding=utf-8
"""
registration_backends.custom.forms
"""
from django import forms
from django.contrib.auth import authenticate
from django.core.validators import email_re
from django.utils.translation import ugettext, ugettext_lazy as _

__author__ = 'George - Kartoza'


class CustomLoginForm(forms.Form):
    """
    This form was copied from django.contrib.auth.forms

    A hacky quick-fix for the long email as username issue. Works in conjunction
        with the custom registration form which inserts the submitted email -
        truncated if more than 30 chars - into the username field. We therefore
        pass this form to the login view in order to truncate email addresses
        which are more than 30 chars.

    """
    username = forms.CharField(label=_("Username"))
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput)

    error_messages = {
        'invalid_login': _("Please enter a correct username and password. "
                           "Note that both fields are case-sensitive."),
        'no_cookies': _("Your Web browser doesn't appear to have cookies "
                        "enabled. Cookies are required for logging in."),
        'inactive': _("This account is inactive."),
    }

    def __init__(self, request=None, *args, **kwargs):
        """
        If request is passed in, the form will validate that cookies are
        enabled. Note that the request (a HttpRequest object) must have set a
        cookie with the key TEST_COOKIE_NAME and value TEST_COOKIE_VALUE before
        running this validation.
        """
        self.request = request
        self.user_cache = None
        super(CustomLoginForm, self).__init__(*args, **kwargs)

    def clean(self):
        ## HACKY FIX APPLIED HERE
        username = self.cleaned_data.get('username')[:30]
        password = self.cleaned_data.get('password')

        if email_re.search(username):
            # If the submitted username is an email address, force to lower case
            username = username.lower()

        if username and password:
            self.user_cache = authenticate(username=username,
                                           password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'])
            elif not self.user_cache.is_active:
                raise forms.ValidationError(self.error_messages['inactive'])
        self.check_for_test_cookie()
        return self.cleaned_data

    def check_for_test_cookie(self):
        if self.request and not self.request.session.test_cookie_worked():
            raise forms.ValidationError(self.error_messages['no_cookies'])

    def get_user_id(self):
        if self.user_cache:
            return self.user_cache.id
        return None

    def get_user(self):
        return self.user_cache