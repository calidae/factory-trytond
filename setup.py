import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name="factory-trytond",
    version="1.0.0",
    long_description=README,
    long_description_content_type="text/markdown",
    packages=["factory-trytond"],
)