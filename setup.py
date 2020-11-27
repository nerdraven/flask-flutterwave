import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="flask-flutterwave-pay", # Replace with your own username
    version="0.0.1",
    author="Damian Akpan",
    author_email="damianakpan2001@gmail.com",
    description="An simple extension to handle flutterwave payment in flask",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Framework :: Flask",
    ],
    python_requires='>=3.6',
)