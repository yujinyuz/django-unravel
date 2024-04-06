==============
django-unravel
==============

django-unravel is a Django app to automatically open emails in the web browser.


Quick start
-----------

1. Add "django_unravel" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...,
        'django_unravel',
    ]

2. Set the ``EMAIL_BACKEND`` and ``EMAIL_FILE_PATH``::

    import tempfile
    ...
    EMAIL_BACKEND = 'django_unravel.mail.backends.filebased.EmailBackend'
    EMAIL_FILE_PATH = tempfile.gettempdir()
    ...
