"""
Cockerel
--------------------
A Lesson Planner and Prover for Math Classes.
Requires you have Coq 8.2pl1 or higher installed

Links
`````

* `documentation <http://packages.python.org/Cockerel>`_
* `development version
  <http://github.com/dcolish/cockerel/zipball/master#egg=Cockerel-dev>`_

"""
from setuptools import setup, find_packages

setup(name="cockerel",
      version="dev",
      packages=find_packages(),
      namespace_packages=['cockerel', 'coqd'],
      include_package_data=True,
      author='Dan Colish',
      author_email='dcolish@gmail.com',
      description='Simplified Theorem Checker for the Web',
      long_description=__doc__,
      zip_safe=False,
      platforms='any',
      license='BSD',
      url='http://www.github.com/dcolish/cockerel',

      classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'Environment :: Console',
        'Intended Audience :: Education',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Operating System :: Unix',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        ],

      entry_points={
        'console_scripts': [
            'cockerel=cockerel.runserver:main',
            'coqd=coqd.runner:main',
            ],
        },

      extras_require={
        'doc': ['sphinx', 'Sphinx-PyPI-upload'],
        },

      install_requires=[
        'Flask',
        'Flask-Markdown==0.3',
        'Flask-Principal',
        'Flask-SQLAlchemy',
        'Flask-Script',
        'flatland',
        'pexpect',
        'ply',
        'SQLAlchemy',
        'twisted',
        ],

      test_suite="nose.collector",
      tests_require=[
        'nose',
        'alfajor',
        ],
      )
