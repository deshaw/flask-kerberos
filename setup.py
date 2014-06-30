"""
Flask-Kerberos
--------------

Provides Kerberos authentication support for Flask applications

Links
`````

* `documentation <https://flask-kerberos.readthedocs.org/en/latest/>`_
* `development version
  <http://github.com/mkomitee/flask-kerberos/zipball/master#egg=Flask-Kerberos-dev>`_

"""

from setuptools import setup

setup(name='Flask-Kerberos',
      version='1.0.3',
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
      classifiers=['Development Status :: 4 - Beta',
                   'Environment :: Web Environment',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: BSD License',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Topic :: Internet :: WWW/HTTP',
                   'Topic :: Software Development :: Libraries :: Python Modules'],
      test_suite='test_flask_kerberos',
      tests_require=['mock'])
