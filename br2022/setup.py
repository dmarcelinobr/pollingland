from setuptools import setup

setup(
    name="br2022",
    version="0.0.1",
    description="Package for Brazilian Pollingpoint 2022 Project",
    author="Daniel Marcelino",
    author_email="daniel.marcelino@jota.info",
    packages=['br2022'],
    install_requires=[
        "pandas>=0.24.2",
        "numpy>=1.16.3"
    ])
