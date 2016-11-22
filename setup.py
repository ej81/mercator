from setuptools import setup, find_packages


setup(name='mercator',
      version='1.0',
      description='Spherical mercator projection for matplotlib',
      url='https://github.com/ej81/mercator',
      author='Eric Jansen',
      author_email='eric.jansen@cmcc.it',
      license='BSD',
      packages=find_packages(),
      install_requires=['matplotlib>=1.3.1', 'pyshp'],
      test_suite='nose.collector',
      tests_require=['nose'])

