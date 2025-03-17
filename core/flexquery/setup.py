#!/usr/bin/env python
import os
import sys

if sys.version_info < (3, 9):
    print("Error: flex-query does not support this version of Python.")
    print("Please upgrade to Python 3.9 or higher.")
    sys.exit(1)

from setuptools import setup

try:
    from setuptools import find_namespace_packages
except ImportError:
    # the user has a downlevel version of setuptools.
    print("Error: flex-query requires setuptools v40.1.0 or higher.")
    print('Please upgrade setuptools with "pip install --upgrade setuptools" ' "and try again")
    sys.exit(1)

this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, "README.md")) as f:
    long_description = f.read()

package_name = "flex-query"
package_version = "1.0.0"
description = """A flexible, parameter-driven SQL query execution tool that connects to multiple database environments."""

setup(
    name=package_name,
    version=package_version,
    description=description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="mirosalwsteblik",
    packages=find_namespace_packages(include=["flexquery", "flexquery.*"]),
    include_package_data=True,
    test_suite="test",
    entry_points={
        "console_scripts": ["flexquery = flexquery.cli.main:cli"],
    },
    install_requires=[
        "pandas",
        "python-dotenv",
        "click",
        "pyyaml",
        "sqlalchemy",
        "duckdb-engine",
        "pyodbc",
    ],

    zip_safe=False,
    classifiers=[
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.9",
)