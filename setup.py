from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="aioswitcher",
    version="2019.3.21",
    author="Tomer Figenblat",
    author_email="tomer.figenblat@gmail.com",
    description="Switcher Boiler Bridge and API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tomerfi/aioswitcher",
    packages=find_packages(),
    classifiers=[
        "Framework :: AsyncIO",
        "Framework :: Flake8",
        "Framework :: Pytest",
        "Framework :: tox",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Home Automation",
        "Typing :: Typed"
    ]
)
