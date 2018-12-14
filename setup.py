import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='stock_prices',
    version='1.0.0',
    author='costajob',
    author_email='costajob@gmail.com',
    description='A simple collector, visualiser and forecaster program for closing stock prices written in Python.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://bitbucket.org/costajob/stock_prices',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
