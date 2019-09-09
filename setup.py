from setuptools import setup, find_packages

setup(
    name='openapi_generator',
    version='1.0.0',
    description="A library to generate OpenAPI documentation from requests",
    author='Wael Farhan',
    author_email='wael34218@gmail.com',

    classifiers=[
        'Development Status :: Alpha',
        'Environment :: Console',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
    ],
    keywords='flask framework base class generic',
    packages=['openapi_generator'],
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
