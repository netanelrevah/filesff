from setuptools import setup

main_namespace = {}
with open("uploader/version.py") as version_file:
    exec(version_file.read(), main_namespace)
version = main_namespace["__version__"]

setup(
    name="filesff",
    version=version,
    packages=["filesff"],
)
