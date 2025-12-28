from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="codexo",
    version="0.1.0",
    author="Imran Nathani",
    author_email="imran.nathani@gmail.com",
    description="A code complexity analyzer to keep your codebase maintainable and LLM-friendly",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/imran-nathani/codexo",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Quality Assurance",
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
        "radon>=6.0.0",
        "pathspec>=0.11.0",
        "toml>=0.10.0",
    ],
    entry_points={
        "console_scripts": [
            "codexo=codexo.main:cli",
        ],
    },
)
