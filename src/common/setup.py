import setuptools

<<<<<<< HEAD
=======
with open("README.md") as buffer:
    long_description = buffer.read()

>>>>>>> 3cd6c0a33f07ec9fcf38baaf7ee0092ee5a90fd3
setuptools.setup(
    name="pjait_map_common",
    version="0.0.1",
    author="Lev Koliadich",
    author_email="s25706@pjwstk.edu.pl",
    description="Interactive map of PJAIT",
<<<<<<< HEAD
=======
    long_description=long_description,
    long_description_content_type="text/markdown",
>>>>>>> 3cd6c0a33f07ec9fcf38baaf7ee0092ee5a90fd3
    url="https://github.com/LeonidKim1602/Map-s24900-s25706",
    packages=setuptools.find_packages(),
    classifiers=[
        "Intended Audience :: End Users/Desktop",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.10",
        "Typing :: Typed",
    ],
    python_requires=">=3.10",
)
