from setuptools import setup, find_packages
import re

# Read version from file without loading the module
with open('JenkinsLibrary/version.py', 'r') as version_file:
    version_match = re.search(r"^VERSION ?= ?['\"]([^'\"]*)['\"]", version_file.read(), re.M)

with open("README.md", "r") as fh:
    long_description = fh.read()

if version_match:
    VERSION = version_match.group(1)
else:
    VERSION = '0.1'

REQUIREMENTS = [
    'requests'
]

setup(
    name="robotframework-jenkinslibrary",
    version=VERSION,
    author="Panchorn Lertvipada",
    author_email="nonpcn@gmail.com",
    description="Jenkins wrapper library for robotframework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Panchorn/robotframework-jenkinslibrary.git",
    license="MIT",
    packages=find_packages(),
    install_requires=['requests'],
    # tests_require=['tox', 'coverage', 'wheel', 'requests_mock', 'pytest'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        # "Programming Language :: Python :: 2",
        # "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ]
)
