"""
WSGI config for gdpr_site project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""

import os
from whitenoise.django import DjangoWhiteNoise
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.prod")


class DjangoCompressorWhiteNoise(DjangoWhiteNoise):
    """A sub-class of DjangoWhiteNoise to play nice with django compressor.

    DjangoWhiteNoise by-default doesn't add forever caching headers on the files
    generated with django-compressor as it doen't treat them as immutable. See
    original implementation of `is_immutable_file` for more details.
    """

    def is_immutable_file(self, path, url):
        """Determine whether given URL represents an immutable file.

        Adds a rule to the default implementation so that all the files in the
        COMPRESS_OUTPUT_DIR are recognized as immutable as well.
        """
        is_immutable = super(DjangoCompressorWhiteNoise, self).is_immutable_file(path, url)
        if not is_immutable:
            from django.conf import settings
            if settings.COMPRESS_OUTPUT_DIR in url:
                return True
        return is_immutable


application = DjangoCompressorWhiteNoise(get_wsgi_application())
