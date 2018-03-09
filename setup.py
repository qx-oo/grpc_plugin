from setuptools import setup
from setuptools import find_packages


setup(name='grpc_plugin',
      version='0.1',
      description='Grpc Plugin',
      url='',
      author='Shawn',
      author_email='q-x64@live.com',
      license='',
      packages=find_packages(exclude=['example*']),
      install_requires=[
          'grpcio==1.9.1'
      ],
      zip_safe=False)
