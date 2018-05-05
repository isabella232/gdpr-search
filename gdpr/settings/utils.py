"""This module contains the some useful methods to read the settings from ENV vriables"""

import os

from django.core.exceptions import ImproperlyConfigured


def get_env_variable(var_name, **kwargs):
    """
    Try to get the settings in the current os environment using the given name.
    Raise if the name is not found, except if the 'default' key is given in
    kwargs (using kwargs allows to pass a default to None, which is different
    as not passing any default):
    get_env_variable('foo') # raise if `foo` not defined
    get_env_variable('foo', default='bar') # will return 'bar' if `foo` is not defined
    get_env_variable('foo', default=None) # will return `None` if `foo` is not defined
    """
    try:
        return os.environ[var_name]
    except KeyError:
        if 'default' in kwargs:
            return kwargs['default']
        raise ImproperlyConfigured(
            "Please set the '%s' environment variable." % var_name
        )


TRUTHY_VALUES = ['1', 'TRUE', 'YES']


def get_bool_env_variable(var_name, **kwargs):
    """
    Same here, except that the result is understood as a boolean value.
    """
    try:
        return True if os.environ[var_name].upper() in TRUTHY_VALUES else False
    except KeyError:
        if 'default' in kwargs:
            return kwargs['default']
        raise ImproperlyConfigured(
            "Please set the '%s' environment variable." % var_name
        )
