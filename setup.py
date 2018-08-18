import os
from setuptools import setup
from setuptools.command.test import test as TestCommand

__author__ = 'Satoshi Terajima <sleepy.st818@gmail.com>'
__version__ = '0.2.0'

requires = ['pycryptodome==3.6.6']

entry_points={
    "console_scripts": ["pww=pww.pww:main"]
}

class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_test(self):
        import pytest
        pytest.main(self.test_args)

setup(
    name = "pww",
    version = __version__,
    author = __author__,
    author_email = "sleepy.st818@gmail.com",
    packages = ["pww"],
    tests_require = ['pytest'],
    cmdclass = {'test': PyTest},
    long_description = open(os.path.join(os.path.dirname(__file__), 'README.md')).read(),
    install_requires = requires,
    entry_points = entry_points,
    classifiers = ["License :: OSI Approved :: MIT License",
                   "Topics :: Security"],
    url = 'https://github.com/meganehouser/pww')
