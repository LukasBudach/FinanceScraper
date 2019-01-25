from setuptools import setup

setup(
    name='finance-scraper',
    version='0.0.1',
    author='Lukas Budach',
    description='An up-to-date web scraper providing financial data from various sources',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    packages=['finance_scraper'],
    include_package_data=True,
    install_requires=[
        'requests'
    ],
)
