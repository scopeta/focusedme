#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()

requirements = []

setup_requirements = [
    "pytest-runner",
]

test_requirements = [
    "pytest>=3",
]

setup(
    author="Fabio Scopeta",
    author_email="scopeta@gmail.com",
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    description="A minimalist Pomodoro timer that runs in your terminal",
    install_requires=requirements,
    license="MIT license",
    package_data={"": ["*.rst", "*.wav"]},
    long_description=readme + "\n\n" + history,
    include_package_data=True,
    keywords="focusedme timer pomodoro",
    name="focusedme",
    packages=find_packages(),
    setup_requires=setup_requirements,
    entry_points={"console_scripts": ["focusedme = focusedme.__main__:main"]},
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/scopeta/focusedme",
    version="0.1.29",
    zip_safe=False,
)
