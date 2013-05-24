from setuptools import setup, find_packages

setup(name='dynsettings',
    packages=find_packages(),  
    description = 'Stores key/value settings in database, allowing for live updating of settings.',
    url = 'http://github.com/infoscout/dynsettings',
    version = '1.0',    
    install_requires=[
        'django==1.4',
    ]
)

