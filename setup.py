# -*- coding: utf-8 -*-
from pathlib import Path

from setuptools import setup

# The text of the README file
with (Path(__file__).parent / "README.md").open(encoding="utf-8") as f:
    README = f.read()

setup(
    name="pysqldbm",
    version="1.0.5",
    url="https://github.com/drewsonne/pysqldbm",
    license="Apache",
    author="Drew J. Sonne",
    author_email="drew.sonne@gmail.com",
    description="A library to wrap SQLdbm API",
    long_description=README,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.10",
    package_dir={"": "src"},
    packages=["pysqldbm_cli", "pysqldbm"],
    include_package_data=True,
    install_requires=["requests", "requests", "backoff"],
    extras_require={"cli": ["click"]},
    entry_points={"console_scripts": ["sqldbm = pysqldbm_cli.run:run"]},
)
