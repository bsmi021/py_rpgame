"""rpgame setup script."""
from datetime import datetime as dt

from setuptools import setup, find_packages

PROJECT_NAME = 'MMORPG Demo App'
PROJECT_PACKAGE_NAME = 'rpgame'
PROJECT_LICENSE = 'Apached License 2.0'
PROJECT_AUTHOR = 'Brian W. Smith'
PROJECT_COPYRIGHT = ' 2018-{}, {}'.format(dt.now().year, PROJECT_AUTHOR)
PROJECT_URL = ''
PROJECT_EMAIL = ''

PACKAGES = find_packages(exclude=['test', 'tests.*'])

REQUIRES = [
    'pytz>=2018.04',
    'confluent_kafka>=0.11.6',
    'jsonpickle>=1.0'
]

setup(
    name=PROJECT_NAME,
    version='1',
    packages=PACKAGES,
    url=PROJECT_URL,
    license=PROJECT_LICENSE,
    author=PROJECT_AUTHOR,
    author_email=PROJECT_EMAIL,
    include_package_data=True,
    description='Open project used to simulate rpg game',
    install_requires=REQUIRES,
    entry_points={
        'console_scripts': [
            'rpggame = rpggame.__main__:main'
        ]
    }
)
