import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name="factory_trytond",
    version="0.1.0",
    long_description=README,
    long_description_content_type="text/markdown",
    packages=find_packages("factory_trytond"),
    install_requires=["factory_boy", "trytond"]
)
