#!/usr/bin/env python
import os
import re
import sys
from codecs import open
from distutils.core import setup
from os import path

from setuptools import find_packages


def get_long_description():
    current_dir = path.abspath(path.dirname(__file__))
    readme_path = path.join(current_dir, 'README.md')
    with open(readme_path, encoding='utf-8') as f:
        try:
            import pypandoc
            long_description = pypandoc.convert_text(f.read(), 'rst', 'markdown_github').replace('\r', '')
        except(OSError, ImportError):
            print('\n\n!!! pandoc not found. long_description is not correct. Do not upload this to PyPI. !!!\n\n')
            long_description = f.read()
    return long_description


def get_version():
    version_file = open(path.join('csv_export', '__init__.py'),  encoding='utf-8').read()
    version_match = re.search('__version__ = [\'"]([0-9]+\.[0-9]+\.[0-9]+)[\'"]', version_file, re.MULTILINE)
    if version_match:
        return version_match.group(1)
    raise RuntimeError('Unable to find version string.')


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    print('You should also add a git tag for this version:')
    print(' git tag {}'.format(get_version()))
    print(' git push --tags')
    sys.exit()


setup(
    name='django-csv-export-view',
    version=get_version(),
    license='BSD',
    description='Django class-based view for CSV exports',
    long_description=get_long_description(),
    url='https://github.com/benkonrath/django-csv-export-view',

    author='Ben Konrath',
    author_email='ben@bagu.org',

    packages=find_packages(exclude=['tests*']),
    include_package_data=True,
    data_files=[('', ['README.md'])],
    zip_safe=False,
    install_requires=[
        'django>=1.8',
    ],
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, <4',

    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Utilities',
    ],
)
