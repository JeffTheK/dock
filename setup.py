from setuptools import setup, find_packages

setup(
    name='dock',
    version='0.1.0',
    packages=find_packages(),
    include_package_data = True,
    package_data={'dock': ['data/*.png']},
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'dock = dock.main:main',
        ],
    },
)