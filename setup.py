from setuptools import setup, find_packages

setup(
    name="adaptive-learning-system",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.20.0",
        "pandas>=1.3.0",
        "scikit-learn>=1.0.0",
        "pytest>=7.0.0",
    ],
)