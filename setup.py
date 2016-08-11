from setuptools import find_packages, setup


with open('VERSION','r') as f:
    version = f.read().strip()


setup(
    name='dynsettings',
    packages=find_packages(),
    include_package_data=True,
    description='Stores key/value settings in database, allowing for live updating of settings.',
    url='http://github.com/infoscout/dynsettings',
    version=version,
    install_requires=[
        'django>=1.5.12',
    ]
)
