from setuptools import setup, find_packages

setup(
    name='htp',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'pandas',
    ],
    entry_points={
        'console_scripts': [
            'htp=scripts.index:cli',
        ],
    },
)