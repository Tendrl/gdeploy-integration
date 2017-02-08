import re

from setuptools import find_packages
from setuptools import setup


def read_module_contents():
    with open('version.py') as app_init:
        return app_init.read()

module_file = read_module_contents()
metadata = dict(re.findall("__([a-z]+)__\s*=\s*'([^']+)'", module_file))
version = metadata['version']


setup(
    name="python_gdeploy",
    version=version,
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*",
                                    "tests"]),
    url="http://www.redhat.com",
    author="Darshan N",
    author_email="dnarayan@redhat.com",
    license="LGPL-2.1+",
    zip_safe=False,
)
