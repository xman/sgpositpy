from setuptools import setup, find_packages


setup(
    name='sgposit',
    version='0.0.1.dev1',
    description='Posit arithmetic library for python',
    keywords='posit arithmetic',
    author='SpeedGo Computing',
    author_email='shinyee@speedgocomputing.com',
    url='https://github.com/xman/sgpositpy',
    license='MIT',
    install_requires=[],
    extras_require={
        'dev' : [],
        'test': [],
    },
    tests_require=['mpmath'],
    test_suite="tests",
    packages=find_packages('src'),
    package_dir={'': 'src'},
)
