#!/usr/bin/env python3
import distutils.cmd
import os
import re

from setuptools import find_packages, setup

from itecha import __version__


class DeployCommand(distutils.cmd.Command):
    user_options = []

    def initialize_options(self):
        """Set default values for options."""
        pass

    def finalize_options(self):
        """Post-process options."""
        pass

    def run(self) -> None:
        import fc2

        function_compute_arn = os.getenv("FUNCTION_COMPUTE_ARN")
        assert function_compute_arn
        match_pattern = r"^acs:fc:([^:]*):(\d+):services/([^.]*)\..*/functions/(.*)$"
        service_site, account_id, service_name, function_name = re.match(
            match_pattern, function_compute_arn
        ).groups()

        client = fc2.Client(
            endpoint=f"http://{account_id}.{service_site}.fc.aliyuncs.com",
            accessKeyID=os.getenv("ACCESS_KEY_ID"),
            accessKeySecret=os.getenv("SECRET_ACCESS_KEY"),
            Timeout=300,
        )
        client.update_function(service_name, function_name, codeDir="dist/fc")


setup(
    name="itecha",
    version=__version__,
    author="Longern",
    author_email="i@longern.com",
    url="https://github.com/longern/itecha",
    license="MIT",
    packages=find_packages(),
    package_data={
        "itecha": ["static/*", "static/*/*", "static/*/*/*", "static/*/*/*/*"]
    },
    include_package_data=True,
    python_requires=">=3.6",
    install_requires=[
        "django>=3.1",
        "djangorestframework",
        "djangorestframework-queryfields",
        "django-environ",
        "django-filter",
        "requests",
        "whitenoise",
    ],
    extras_require={
        "fc": [
            "django-import-export",
            "djanble @ git+https://github.com/longern/djanble.git@main",
        ],
    },
    entry_points={
        "console_scripts": [
            "itecha = itecha.__main__:main",
        ],
    },
    cmdclass={"deploy": DeployCommand},
)
