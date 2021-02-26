from os import path
from setuptools import setup

with open(path.join(path.dirname(path.abspath(__file__)), 'README.rst')) as f:
    readme = f.read()

setup(
    name             = 'pfdo_med2img',
    version          = '1.0.2',
    description      = 'An app to recursively walk down a directory tree and perform a med2image on files in each directory.',
    long_description = readme,
    author           = 'Arushi Vyas',
    author_email     = 'dev@babyMRI.org',
    url              = 'http://wiki',
    packages         = ['pfdo_med2img'],
    install_requires = ['chrisapp'],
    test_suite       = 'nose.collector',
    tests_require    = ['nose'],
    license          = 'MIT',
    zip_safe         = False,
    python_requires  = '>=3.6',
    entry_points     = {
        'console_scripts': [
            'pfdo_med2img = pfdo_med2img.__main__:main'
            ]
        }
)
