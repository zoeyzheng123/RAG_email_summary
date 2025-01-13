import setuptools

setuptools.setup(
    name='predictor',
    version='0.0.1',
    description='Predictor pipeline',
    install_requires=['dynaconf==3.1.12', 'sentry-sdk==1.31.0', "backoff==2.2.1"],
    packages=setuptools.find_packages(exclude=['*.tests', 'tests']),
)
