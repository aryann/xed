import os
import setuptools


with open(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                       'README.md')) as f:
    long_description = f.read()


setuptools.setup(
    name='xed',
    version='0.0.2',
    author='Aryan Naraghi',
    author_email='aryan.naraghi@gmail.com',
    description=('A utility for performing basic text transformations.'),
    long_description=long_description,
    long_description_content_type='text/markdown',
    project_urls={
        'Source Code': 'https://github.com/aryann/xed',
        "Author's Website": 'https://aryan.app',
    },
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Utilities',
    ],
    entry_points={
        'console_scripts': [
            'xed=xed.xed:cli',
        ],
    },
)
