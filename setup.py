# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from setuptools import Command, find_packages, setup


with open('VERSION', 'r') as f:
    version = f.read().strip()


class TestCommand(Command):

    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        import django
        from django.conf import settings
        from django.core.management import call_command

        settings.configure(
            DATABASES={
                'default': {
                    'NAME': ':memory:',
                    'ENGINE': 'django.db.backends.sqlite3',
                },
            },
            INSTALLED_APPS=(
                'django.contrib.admin',
                'django.contrib.auth',
                'django.contrib.contenttypes',
                'django.contrib.messages',
                'django.contrib.sessions',
                'dynsettings',
                'dynsettings.tests',
            ),
            TEMPLATES=[
                {
                    'BACKEND': 'django.template.backends.django.DjangoTemplates',  # noqa: E501
                    'APP_DIRS': True,
                    'OPTIONS': {
                        'context_processors': [
                            'django.contrib.auth.context_processors.auth',
                            'django.contrib.messages.context_processors.messages',  # noqa: E501
                        ],
                    },
                },
            ],
            MIDDLEWARE=(
                'django.middleware.common.CommonMiddleware',
                'django.contrib.sessions.middleware.SessionMiddleware',
                'django.contrib.auth.middleware.AuthenticationMiddleware',
                'django.contrib.messages.middleware.MessageMiddleware',
            ),
            MIDDLEWARE_CLASSES=(
                'django.contrib.sessions.middleware.SessionMiddleware',
                'django.contrib.messages.middleware.MessageMiddleware',
            ),  # Django < 1.10
            ROOT_URLCONF='dynsettings.tests.urls',
            SECRET_KEY="test_secret_key",
        )
        django.setup()
        call_command('test', 'dynsettings')


setup(
    name='dynsettings',
    packages=find_packages(),
    include_package_data=True,
    description=(
        'Stores key/value settings in database, allowing for live updating '
        'of settings.'
    ),
    url='http://github.com/infoscout/dynsettings',
    version=version,
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
        'Framework :: Django :: 1.10',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.0',
        'Framework :: Django :: 3.0',
        'Framework :: Django :: 4.0',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.9',
        'Topic :: Utilities',
    ],
    install_requires=[
        'Django >= 1.8, < 4.1a0', 'six'
    ],
    tests_require=[
        'mock',
    ],
    cmdclass={'test': TestCommand}
)
