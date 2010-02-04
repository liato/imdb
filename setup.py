import os
try:
    from setuptools import setup 
except ImportError: 
    from distutils.core import setup 

#doc_dir = os.path.join(os.path.dirname(__file__), 'docs')
#index_filename = os.path.join(doc_dir, 'index.rst')
#long_description = long_description + open(index_filename).read().split('split here', 1)[1]

setup(name='imdb',
      author='liato',
      author_email='x@x00.us',
      url='http://www.github.com/liato/imdb',
      license='MIT',
      version=0.1,
      description="A simple python interface to the Internet Movie Database.",
      long_description="AWESOME",
      classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Database :: Front-Ends',
        'Topic :: Software Development :: Libraries :: Python Modules',
      ],
      keywords='imdb scraping movie database',
      py_modules=['imdb'],
      install_requires=['lxml'])
