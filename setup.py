import setuptools

with open("README.md", "r") as f:
    LONG_DESCRIPTION = f.read()

with open("requirements.txt", "r") as f:
    REQUIREMENTS = f.read().splitlines()

# packages = ["kick"]

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
    install_requires=REQUIREMENTS,
    # packages=packages,
    description="",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    license="MIT",
)
