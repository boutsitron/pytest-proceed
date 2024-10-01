"""Setup script for the pytest-proceed package."""

from setuptools import find_packages, setup

# Read the contents of your README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pytest-proceed",
    version="0.1.3",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "pytest-proceed=pytest_proceed:main",
        ],
    },
    install_requires=[
        "pytest",
        "argparse",  # This is included in the standard library from Python 2.7 and 3.2 onwards, so it's generally not needed unless you support older versions.
    ],
    python_requires=">=3.6",  # Adjust based on the Python versions you want to support.
    long_description=long_description,
    long_description_content_type="text/markdown",
)
