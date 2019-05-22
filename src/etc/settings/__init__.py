import os
import sys

CONF = os.environ.get('DJANGO_SETTINGS_MODULE')

if CONF == 'etc.settings':
    print(
        '\n\n  [WARNING] DJANGO_SETTINGS_MODULE=bin.local\n'
        '  Will use settings/local.py\n\n', file=sys.stderr)
    try:
        from .local import *  # NOQA
    except ModuleNotFoundError as e:
        exit(e)
