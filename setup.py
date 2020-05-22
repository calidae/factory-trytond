import pathlib
from setuptools import find_packages
from setuptools import setup

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name="factory_trytond",
    version="0.1.0",
    author="Calidae",
    author_email="dev@calidae.com",
    description="Factory Boy - Trytond integration",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/calidae/factory-trytond",
    packages=find_packages("factory_trytond"),
    install_requires=["factory_boy", "trytond"],
    classifiers=[
        "Framework :: Tryton",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    license='GPL-3',
    python_requires='>=3.5',
)
