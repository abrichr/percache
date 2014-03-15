from distutils.core import setup
import os.path

README = os.path.join(os.path.dirname(__file__), 'README.rst')

version = '0.2.1'

with open(README) as fp:
    longdesc = fp.read()

setup(name='percache',
      version=version,
      description='Persistently cache results of callables',
      long_description=longdesc,
      classifiers=[
            'Development Status :: 4 - Beta',
            'License :: OSI Approved :: MIT License',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Programming Language :: Python :: 2',
            'Programming Language :: Python :: 2.6',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.3',
            'Topic :: Software Development',
            'Intended Audience :: Developers'
      ],
      author='Oben Sonne',
      author_email='obensonne@googlemail.com',
      license='MIT License',
      url='http://bitbucket.org/obensonne/percache',
      py_modules=['percache']
     )

