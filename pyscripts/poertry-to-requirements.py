"""Python script for creating requirements.txt file.

Python script for converting poetry dependencies from
poetry.lock to requirements.txt for legacy support.
"""

from toml import load as toml_load

if __name__ == "__main__":
    parsed_toml = toml_load("poetry.lock")
    with open("requirements.txt", "w+") as req_file:
        req_file.write(
            "# This file exists for legacy support. "
            + "Do not use for requirements instllations.\r\n"
        )
        for pkg in parsed_toml["package"]:
            req_file.write("{}=={}\r\n".format(pkg["name"], pkg["version"]))

    print("requirements.txt was updated, please push to scm.")
