from setuptools import find_packages
from isc_ops.setup_tools import setup, current_version

setup(name='dynsettings',
    packages=find_packages(),  
    description = 'Stores key/value settings in database, allowing for live updating of settings.',
    url = 'http://github.com/infoscout/dynsettings',
    version = current_version(),    
    install_requires=[
        'django==1.4',
    ]
)
