import os

from distutils.core import setup
from setuptools import find_packages

requirements = [
    # Job queue for export/import
    'redis',
    'rq',
    'honcho',
    'Collectfast',
]

packages = find_packages()
package_data = {package: ['templates/*.*']
                    for package in packages}
package_data['goorchids'].append('static/*.*')
package_data['goorchids'].append('media/*.*')

setup(
    name='goorchids',
    packages=packages,
    package_data=package_data,
    install_requires=requirements,
)
