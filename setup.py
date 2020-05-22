import pathlib
from setuptools import find_packages
from setuptools import setup

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name="factory_trytond",
    version="0.1.1",
    author="Calidae",
    author_email="dev@calidae.com",
    description="Factory Boy - Trytond integration",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/calidae/factory-trytond",
    packages=find_packages("factory_trytond"),
    install_requires=["factory_boy", "trytond"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)
