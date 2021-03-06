import setuptools

with open("README.md", "r") as fh:

    long_description = fh.read()

setuptools.setup(
    name='FinanceScraper',
    version='0.2.1',
    author='Lukas Budach',
    author_email='lukas.budach@student.hpi.de',
    description='An up-to-date web scraper providing financial data from various sources',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(),
    scripts=['bin/full_example.py'],
    url="https://github.com/LukasBudach/FinanceScraper",
    include_package_data=True,
    install_requires=[
        'requests'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
