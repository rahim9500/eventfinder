from setuptools import setup, find_packages

setup(
    name="eventfinder",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "flask",
        "sqlalchemy",
        "requests",
        "flake8",
        "black",
    ],
)
# This is a new line at the end of the file
