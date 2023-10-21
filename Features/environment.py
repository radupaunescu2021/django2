import os
import subprocess

import django
from django.contrib.auth import get_user_model


def before_scenario(context,scenario):
    print("before_all is being executed")
    os.environ['DJANGO_SETTINGS_MODULE'] = 'myproject.settings'
    django.setup()


def after_feature(context,feature):
    os.environ['DJANGO_SETTINGS_MODULE'] = 'djangoProject2.settings'
    django.setup()
    # Run the command
    result = subprocess.run(['python3.9', 'manage.py', 'flush', '--noinput'], capture_output=True, text=True)

    # Optionally, check the result
    if result.returncode != 0:
        print(f"Failed to run command: {result.stderr}")
    else:
        print(f"Command ran successfully-Database has been erased: {result.stdout}")

