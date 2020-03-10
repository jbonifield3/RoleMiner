import os

from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='RoleMiner',
    version='0.1.0',
    author='James Bonifield',
    author_email='jameslbonifield@gmail.io',
    packages=['RoleMiner'],
    url='https://github.com/jbonifield3/django-whoshere',
    license='MIT',
    description='Utilities for Role Based Access Control',
    long_description=README,
    include_package_data=True,
    install_requires=['pandas', 'numpy'],
    # test_suite='RoleMiner.tests',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: MacOS X',
        'Framework :: Jupyter',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Scientific/Engineering :: Mathematics',
    ]
) 