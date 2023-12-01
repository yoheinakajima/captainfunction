# setup.py

from setuptools import setup, find_packages

setup(
    name='captainfunction',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        # Add your dependencies here, e.g., 'requests', 'numpy', etc.
    ],
    package_data={
        'captainfunction': ['functions/*.py'],
    },
    include_package_data=True,
    description='A Python package to dynamically load functions for OpenAI Assistant',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Yohei Nakajima',
    author_email='info@untapped.vc',
    url='https://github.com/yoheinakajima',
    # More metadata can be added here (license, classifiers, etc.)
)
