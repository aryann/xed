import os
import setuptools


with open(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                       'README.md')) as f:
    long_description = f.read()


setuptools.setup(
    name='xed',
    version='0.0.1',
    author='Aryan Naraghi',
    author_email='aryan.naraghi@gmail.com',
    description=('A utility for performing basic text transformations.'),
    long_description=long_description,
    long_description_content_type='text/markdown',
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'xed=xed.xed:cli',
        ],
    },
)
