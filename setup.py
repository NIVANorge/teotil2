import os

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

lib_fold = os.path.dirname(os.path.realpath(__file__))
requirements_path = lib_fold + "/requirements.txt"
install_requires = []
if os.path.isfile(requirements_path):
    with open(requirements_path) as f:
        install_requires = f.read().splitlines()

setuptools.setup(
    name="teotil2",
    version="0.0.1",
    author="James Sample",
    author_email="james.sample@niva.no",
    description="The TEOTIL2 model for estimating riverine fluxes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://nivanorge.github.io/teotil2/",
    packages=setuptools.find_packages(),
    install_requires=install_requires,
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU GPLv3",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
    ],
)
