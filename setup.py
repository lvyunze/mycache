#!/usr/bin/env python3

from setuptools import find_packages, setup
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="mycache",
    packages=find_packages(include="mycache"),
    version="0.0.1",
    description="Python Implements Caching",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lvyunze/mycache",
    author="lvyunze",
    author_email="17817462542@163.com",
    license="MIT",

    install_requires=[
    ],
    setup_requires=[
    ],
    tests_require=[
        "freezegun==1.0.0",
        "mypy==0.782",
        "pycodestyle==2.6.0",
        "pylint==2.6.0",
        "pytest-benchmark==3.2.3",
        "pytest-cov==2.10.1",
        "pytest-runner==5.2",
        "pytest==6.0.1",
        "radon==4.3.2",
        "twine==3.1.1",
    ],
    test_suite="tests",
)
