"""Python script for creating requirements.txt file.

Python script for converting poetry dependencies from
pyproject.toml to requirements.txt for legacy support.
"""

from toml import load as toml_load

if __name__ == "__main__":
    parsed_toml = toml_load("pyproject.toml")
    with open("requirements.txt", "w+") as req_file:
        req_file.write(
            "# This file exists for legacy support. "
            + "Do not use for requirements instllations.\r\n"
        )
        for dep in parsed_toml["tool"]["poetry"]["dependencies"]:
            if dep.lower() != "python":
                if (
                    "version"
                    in parsed_toml["tool"]["poetry"]["dependencies"][dep]
                ):
                    req_file.write(
                        "{}=={}\r".format(
                            dep,
                            parsed_toml["tool"]["poetry"]["dependencies"][dep][
                                "version"
                            ],
                        )
                    )
                else:
                    req_file.write("{}\r".format(dep))

    print("requirements.txt was updated, please push to scm.")
