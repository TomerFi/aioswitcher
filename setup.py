import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aioswitcher",
    version="2019.02.05",
    author="Tomer Figenblat",
    author_email="tomer.figenblat@gmail.com",
    description="Switcher Boiler Bridge and API Tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tomerfi/aioswitcher",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.5",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Framework :: AsyncIO",
        "Framework :: Flake8",
        "Intended Audience :: Developers",
        "Topic :: System :: Networking :: Monitoring :: Hardware Watchdog"
    ]
)