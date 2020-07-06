import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="oyster-BrennanBarker", # Replace with your own username
    version="0.0.1",
    author="Brennan Barker",
    description="A package for conducting causal inference using causal diagrams",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/BrennanBarker/oyster",
    packages=setuptools.find_packages(),
    install_requires=[
        'matplotlib'
        'networkx'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)