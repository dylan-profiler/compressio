from pathlib import Path

from setuptools import find_packages, setup

# Read the contents of README file
source_root = Path(".")
with (source_root / "README.md").open(encoding="utf-8") as f:
    long_description = f.read()

# Read the requirements
with (source_root / "requirements.txt").open(encoding="utf8") as f:
    requirements = f.readlines()

with (source_root / "requirements_test.txt").open(encoding="utf8") as f:
    test_requirements = f.readlines()

__version__ = None
with (source_root / "src/compressio/version.py").open(encoding="utf8") as f:
    exec(f.read())


setup(
    name="compressio",
    version=__version__,
    url="https://github.com/dylan-profiler/compressio",
    description="compressio",
    author="Ian Eaves, Simon Brugman",
    author_email="ian.k.eaves@gmail.com",
    package_data={"src/compressio": ["py.typed"]},
    packages=find_packages("src"),
    package_dir={"": "src"},
    install_requires=requirements,
    include_package_data=True,
    tests_require=test_requirements,
    python_requires=">=3.6",
    long_description=long_description,
    long_description_content_type="text/markdown",
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
