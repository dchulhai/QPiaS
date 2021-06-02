import setuptools
from dimpy._version import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="qpias",
    version=__version__,
    author="Dhabih V. Chulhai",
    author_email="chulhaid@uindy.edu",
    description="Quantum Particle-in-a-Sandbox",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dchulhai/QPiaS",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
