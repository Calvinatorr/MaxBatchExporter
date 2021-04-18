import setuptools

with open("README.md", "r") as file:
    long_description = file.read()

setuptools.setup(
    name="max-batch-exporter",
    version="0.0.1",
    author="Calvin Simpson",
    author_email="calvinbgood@hotmail.co.uk",
    description="Batch export mesh files from 3ds Max 2021.1",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Calvinatorr/MaxBatchExporter",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "LICENSE :: OTHER/PROPRIETARY LICENSE",
        "Operating System :: Microsoft :: Windows"
    ],
    python_requires='>=3.7',
    entry_points={"3dsMax": "startup=MaxBatchExporter:startup"}
)