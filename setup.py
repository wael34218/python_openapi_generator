from setuptools import setup, find_packages

setup(
    name='openapi_generator',
    version='1.0.5',
    description="A library to generate OpenAPI documentation from requests",
    author='Wael Farhan',
    author_email='wael34218@gmail.com',
    python_requires='>=3.5',

    classifiers=[
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.5',
        "License :: OSI Approved :: MIT License",
    ],
    keywords='flask framework base class generic',
    packages=['openapi_generator'],
    download_url='https://github.com/wael34218/python_openapi_generator/archive/v1.0.5.tar.gz',
    url='https://github.com/wael34218/python_openapi_generator',
    install_requires=[
        'pyyaml',
        'openapi-spec-validator',
        'requests',
        'pyOpenSSL'
    ],
    test_suite='nose2.collector.collector',
    extras_require={
        'test': ['nose2'],
    },
    include_package_data=True,
)
