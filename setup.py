# -*- coding: utf-8 -*-

from setuptools import find_packages, setup

package_name = 'openslides-protocol'
module_name = 'openslides_protocol'

# The following commented unique string is used to detect this import.
module = __import__(module_name)  # Peikee0iuv7uhikuashotohch6eec6ohseuNg7su

with open('README.rst') as readme:
    long_description = readme.read()

with open('requirements_production.txt') as requirements:
    install_requires = requirements.readlines()

setup(
    name=package_name,
    version=module.__version__,
    description=module.__verbose_name__,
    long_description=long_description,
    author='Authors of %s, see AUTHORS' % module.__verbose_name__,
    author_email='support@openslides.org',
    url=module.__url__,
    keywords='OpenSlides',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Plugins',
        'Environment :: Web Environment',
        'Framework :: Django',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'],
    license=module.__license__,
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    install_requires=install_requires,
    entry_points={'openslides_plugins': '%s = %s' % (module.__verbose_name__, module_name)})
