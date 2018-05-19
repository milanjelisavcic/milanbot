#!/usr/bin/python3.5


from setuptools import setup, find_packages

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except (IOError, ImportError):
    long_description = open('README.md').read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

version = '0.1'

setup(
    name='milanbot',
    version=version,
    install_requires=requirements,
    author='Milan Jelisavcic',
    author_email='milan.jelisavcic@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    url='https://github.com/milanjelisavcic/milanbot',
    license='Unlicense',
    description='A bot-kit for fixing data on Wikidata and Wikipedia.',
    long_description=long_description,
    entry_points={
        'console_scripts': [
            'milanbot = milanbot:cli',
        ]
    },
)