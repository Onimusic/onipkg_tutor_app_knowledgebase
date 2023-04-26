# boot_django.py
#
# This file sets up and configures Django. It's used by scripts that need to
# execute as if running in a Django server.
import os
import django
from django.conf import settings

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "receipts"))


def boot_django():
    settings.configure(
        BASE_DIR=BASE_DIR,
        SECRET_KEY='Not a secret key at all, actually',
        DEBUG=True,
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.postgresql",
                "NAME": "postgres",
                "USER": "postgres",
                "PASSWORD": "example",
                "HOST": "localhost",
                "PORT": "5432",
            }
        },
        INSTALLED_APPS=(
            'django.contrib.auth',
            'django.contrib.admin',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.staticfiles',
            'django.contrib.messages',
            'nested_admin',
            'knowledgebase',
        ),
        TIME_ZONE="UTC",
        USE_TZ=True,
        STATIC_URL='/static/',
        MIDDLEWARE=[
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
        ],
        TEMPLATES=(
            {
                'BACKEND': 'django.template.backends.django.DjangoTemplates',
                'OPTIONS': {
                    'context_processors': [
                        'django.contrib.auth.context_processors.auth',
                        'django.contrib.messages.context_processors.messages',
                    ],
                }
            },
        )
    )
    django.setup()
