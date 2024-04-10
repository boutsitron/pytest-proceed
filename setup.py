from setuptools import find_packages, setup

setup(
    name="pytest-proceed",
    version="0.1.0",
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
)
