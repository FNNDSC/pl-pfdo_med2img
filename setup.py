from os import path
from setuptools import setup

with open(path.join(path.abspath(path.dirname(__file__)), 'README.rst')) as f:
    readme = f.read()

setup(
    name             = 'pfdo_med2img',
    version          = '0.1',
    description      = 'An app to ...',
    long_description = readme,
    author           = 'FNNDSC',
    author_email     = 'dev@babyMRI.org',
    url              = 'http://wiki',
    packages         = ['pfdo_med2img'],
    install_requires = ['chrisapp~=1.1.6'],
    test_suite       = 'nose.collector',
    tests_require    = ['nose'],
    license          = 'MIT',
    zip_safe         = False,
    python_requires  = '>=3.8',
    entry_points     = {
        'console_scripts': [
            'pfdo_med2img = pfdo_med2img.__main__:main'
            ]
        }
)
