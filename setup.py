from setuptools import setup, find_packages

setup(name='gtool',
      version='0.1.9',
      author='Ben Sapiro',
      author_email = "https://ca.linkedin.com/in/sapiro",
      license='GPLv3',
      keywords='security risk governance compliance framework',
      description=('A framework for building security governance, risk and compliance tools.'),
      long_description="G.Tool is a framework for building governance, risk and compliance security tools. It's a barebones framework, that is highly extensible but comes with a a lot of common functionality included.",
      download_url = 'https://github.com/gtoolframework/gtool/tarball/0.1.9',
      url='https://gtoolframework.github.io/',
      packages=find_packages(),
      include_package_data=True,
      install_requires=[
          'boltons',
          'click',
          'configparser',
          'decorator',
          'patricia-trie',
          'pluginbase',
          'pyparsing',
          'PyYAML',
          'simpleeval',
          'six',
          'validators',
          'XlsxWriter'
      ],
      package_data = {'gtool': ['core/projecttemplate/*']},
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