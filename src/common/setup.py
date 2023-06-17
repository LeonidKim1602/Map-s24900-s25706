import setuptools

with open("README.md") as buffer:
    long_description = buffer.read()

setuptools.setup(
    name="pjait_map_common",
    version="0.0.1",
    author="Lev Koliadich",
    author_email="s25706@pjwstk.edu.pl",
    description="Interactive map of PJAIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
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
