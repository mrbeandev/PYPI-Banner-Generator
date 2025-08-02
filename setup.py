from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="pypi-banner-generator",
    version="2.0.0",
    author="mrbeandev",
    author_email="mrbeandev@gmail.com",
    description="A professional banner generator for PyPI packages with multiple themes and styles",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mrbeandev/PYPI-Banner-Generator",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Multimedia :: Graphics",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "pypi-banner-generator=banner_generator:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.ttf", "*.png"],
    },
)
