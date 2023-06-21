import re

import setuptools

with open("README.md", "r") as f:
    LONG_DESCRIPTION = f.read()

with open("requirements.txt", "r") as f:
    REQUIREMENTS = f.read().splitlines()

version = ""
with open("kick/__init__.py") as f:
    version = re.search(
        r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE
    ).group(
        1
    )  # type: ignore

if not version:
    raise RuntimeError("version is not set")


if version.endswith(("a", "b", "rc")):
    # append version identifier based on commit count
    try:
        import subprocess

        p = subprocess.Popen(
            ["git", "rev-list", "--count", "HEAD"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        out, err = p.communicate()
        if out:
            version += out.decode("utf-8").strip()
        p = subprocess.Popen(
            ["git", "rev-parse", "--short", "HEAD"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        out, err = p.communicate()
        if out:
            version += "+g" + out.decode("utf-8").strip()
    except Exception:
        pass


setuptools.setup(
    name="kick.py",
    author="cibere",
    author_email="contact@cibere.dev",
    url="https://github.com/cibere/kick.py",
    project_urls={
        "Code": "https://github.com/cibere/kick.py",
        "Issue tracker": "https://github.com/cibere/kick.py/issues",
    },
    version="0.0.1",
    python_requires=">=3.11",
    requires=REQUIREMENTS,
    packages=["kick"],
    description="",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    license="MIT",
)
