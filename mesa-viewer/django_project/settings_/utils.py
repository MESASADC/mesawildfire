# coding=utf-8
"""Helpers for settings.
Source: https://github.com/timlinux/projecta
"""

import os

# Absolute filesystem path to the Django project directory:
DJANGO_ROOT = os.path.dirname(       # django_project
    os.path.dirname(                 # settings
        os.path.abspath(__file__)    # utils.py
    )
)


def absolute_path(*args):
    """Get an absolute path for a file that is relative to the django root.
    """
    return os.path.join(DJANGO_ROOT, *args)


def ensure_secret_key_file():
    """Checks that secret_key.py exists in settings dir.
    If not, creates one with a random generated SECRET_KEY setting.
    """
    secret_path = absolute_path('settings', 'secret_key.py')
    if not os.path.exists(secret_path):
        from django.utils.crypto import get_random_string
        secret_key = get_random_string(
            50, 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)')
        disqus_shortname = get_random_string(
            50, 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)')
        with open(secret_path, 'w') as f:
            f.write("SECRET_KEY = " + repr(secret_key) + "\n")
            f.write("DISQUS_WEBSITE_SHORTNAME = "
                    + repr(disqus_shortname) + "\n")


def get_env(key):
    """Get an environment variable.

    Wrapper for os.environ that handles unset vars gracefully.

    :param key: The environment variable key to fetch.
    :type key: str
    """
    try:
        return os.environ[key]
    except KeyError:
        return None


# Import the secret key
ensure_secret_key_file()
