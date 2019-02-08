import os
import sys

from setuptools import setup
from setuptools.command.test import test as TestCommand

install_requires = [
    'aiofile',
    'aiohttp_session',
    'aiohttp',
    'cryptography',
    'trafaret',
    'trafaret_config',
    'aiocache',
    'graphql-core-next',
    'aiodocker',
    'shortuuid',
    'click'
]

if sys.version_info < (3, 7, 0):
    raise RuntimeError("requires Python 3.7.0+")


def read(f):
    return open(os.path.join(os.path.dirname(__file__), f)).read().strip()


class PyTest(TestCommand):
    user_options = [("pytest-args=", "a", "Arguments to pass to pytest")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = ""

    def run_tests(self):
        import shlex

        # import here, cause outside the eggs aren't loaded
        import pytest

        errno = pytest.main(shlex.split(self.pytest_args))
        sys.exit(errno)

tests_require = install_requires + ['pytest', 'pytest-timeout', 'pytest-asyncio']

args = dict(
    name='pystacker',
    version='0.2.0',
    description='Docker-compose stacks web manager',
    classifiers=['Topic :: Internet :: WWW/HTTP'],
    author='Peter Samoilov',
    author_email='xsserv@gmail.com',
    maintainer='Peter Samoilov',
    maintainer_email='xsserv@gmail.com',
    license='Apache 2',
    packages=['pystacker'],
    install_requires=install_requires,
    tests_require=tests_require,
    include_package_data=True,
    cmdclass=dict(pytest=PyTest),
    entry_points={
        'console_scripts': ['stacker=pystacker.cli:cli'],
    }
)
setup(**args)
