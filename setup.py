from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="aidep",
    version="0.1.0",
    author="RenierB-dev",
    author_email="",
    description="AI Dependency Doctor - Detect and fix AI framework conflicts",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/RenierB-dev/aidep",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=[
        "click>=8.0.0",
        "anthropic>=0.18.0",
        "rich>=13.0.0",
        "packaging>=23.0",
    ],
    entry_points={
        "console_scripts": [
            "aidep=aidep.cli:main",
        ],
    },
)
