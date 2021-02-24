#!/usr/bin/env python3
from setuptools import setup, find_packages

from itecha import __version__

setup(
    name="itecha",
    version=__version__,
    author="Longern",
    author_email="i@longern.com",
    url="https://github.com/longern/itecha",
    license="MIT",
    packages=find_packages(),
    package_data={"itecha": ["static/**/*"]},
    include_package_data=True,
    python_requires=">=3.6",
    install_requires=[
        "django>=3.1",
        "djangorestframework",
        "django-environ",
        "django-filter",
        "requests",
        "whitenoise",
    ],
)
