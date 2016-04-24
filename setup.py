#!/usr/bin/env python
import os
import sys
import re
from distutils.core import setup
from setuptools import find_packages


def get_long_description():
    path = os.path.join(os.path.dirname(__file__), 'README.md')
    with open(path) as f:
        return f.read()


def get_version():
    setup_py = open('setup.py').read()
    return re.search("version=['\"]([0-9]+\.[0-9]+\.[0-9]+)['\"]", setup_py, re.MULTILINE).group(1)


if sys.argv[-1] == 'publish':
    os.system("python setup.py sdist upload")
    print("You should also add a git tag for this version:")
    print(" git tag {}".format(get_version()))
    print(" git push --tags")
    sys.exit()


setup(
    name='django-csv-export-view',
    version='0.0.1',
    license='BSD',
    description='Django class-based view for CSV exports',
    long_description=get_long_description(),
    url='https://github.com/benkonrath/django-csv-export-view',

    author='Ben Konrath',
    author_email='ben@bagu.org',

    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'django>=1.8',
    ],

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Utilities',
    ],
)
