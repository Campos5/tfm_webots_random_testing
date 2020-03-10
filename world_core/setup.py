from setuptools import setup

setup(
    name='world_core',
    version='1.0',
    packages=[
        'world_core'
    ],
    include_package_data=False,
    install_requires=[
        'hypothesis',
        'Jinja2'
    ],
)
