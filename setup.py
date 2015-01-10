import re

from setuptools import setup

with open('rdoc/__init__.py') as f:
    version = re.findall(r"^__version__ = '(.*)'", f.read(), re.M)[0]

with open('README') as f:
    README = f.read()

setup(
    name='rdoc',
    version=version,
    author='Stanis Trendelenburg',
    author_email='stanis.trendelenburg@gmail.com',
    url='https://github.com/trendels/rdoc',
    description='Tools to build the Rhino documentation.',
    long_description=README,
    packages=['rdoc'],
    package_dir={'rdoc': 'rdoc'},
    package_data={'rdoc': [
        'data/Makefile',
        'data/meta.yml',
        'data/modules',
        'data/filters/*.py',
        'data/templates/*',
        'data/src/*',
        'data/static/*',
    ]},
    entry_points={
        'console_scripts': [
            'rdoc-init = rdoc:init',
            'rdoc-relpath = rdoc:relpath',
            'rdoc-make-index = rdoc:make_index',
            'rdoc-make-links = rdoc:make_links',
            'rdoc-make-rules = rdoc:make_rules',
            'rdoc-extract = rdoc.extract:extract',
        ],
    },
    install_requires=['pandocfilters'],
)
