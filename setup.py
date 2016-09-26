from setuptools import setup, find_packages
import os

#TODO add version checking for Python

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(name='g.tool',
      version='0.1.0',
      author='Ben Sapiro',
      author_email = "https://ca.linkedin.com/in/sapiro",
      license='GPLv3',
      keywords='security risk governance compliance framework',
      description=('A framework for building security governance, risk and compliance tools.'),
      long_description=read('README.MD'),
      url='https://github.com/bsapiro/gtool',
      packages=find_packages(),
      include_package_data=True,
      install_requires=[
          'boltons >= 16.5.0',
          'click >= 6.6',
          'configparser >= 3.5',
          'decorator >= 4.0.10',
          'patricia-trie >= 10',
          'pluginbase >= 0.4',
          'pyparsing >= 2.1.5',
          'PyYAML >= 3.11',
          'simpleeval >= 0.8.7',
          'six >= 1.10.0',
          'validators >= 0.10.3',
          'XlsxWriter >= 0.9.3'
      ],
      classifiers=[
          "Development Status :: 4 - Beta",
          "Topic :: Utilities",
          "Topic :: Software Development :: Libraries :: Application Frameworks",
          "Environment :: Console",
          "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
          "Intended Audience :: Information Technology",
          "Natural Language :: English",
          "Operating System :: OS Independent",
          "Programming Language :: Python :: 3.5"
       ],
      entry_points={
          'console_scripts': [
              'gtool = gtool.core.utils.command:cli'
          ]
      },
      )