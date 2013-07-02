"""
Flask-Kerberos
------------

Provides Kerberos authentication support for Flask applications
"""

from setuptools import setup

setup(name='Flask-Kerberos',
      version='1.0.0',
      url='http://github.com/mkomitee/flask-kerberos',
      license='BSD',
      author='Michael Komitee',
      author_email='mkomitee@gmail.com',
      description='Kerberos authentication support for Flask',
      long_description=__doc__,
      py_modules=['flask_kerberos'],
      zip_safe=False,
      include_package_data=True,
      package_data={'': ['LICENSE', 'AUTHORS']},
      platforms='any',
      install_requires=['Flask', 'kerberos'],
      classifiers=['Environment :: Web Environment',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: BSD License',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Topic :: Internet :: WWW/HTTP',
                   'Topic :: Software Development :: Libraries :: Python Modules'])
