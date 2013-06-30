"""
Flask-GSSAPI
------------

Provides GSSAPI authentication support for Flask applications
"""

from setuptools import setup

setup(name='Flask-GSSAPI',
      version='1.0.0',
      url='http://github.com/mkomitee/flask-gssapi',
      license='BSD',
      author='Michael Komitee',
      author_email='mkomitee@gmail.com',
      description='GSSAPI authentication support for Flask',
      long_description=__doc__,
      packages=['flask_gssapi'],
      zip_safe=False,
      include_package_data=True,
      platforms='any',
      install_requires=['Flask', 'kerberos'],
      classifiers=['Environment :: Web Environment',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: BSD License',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Topic :: Internet :: WWW/HTTP',
                   'Topic :: Software Development :: Libraries :: Python Modules'])
