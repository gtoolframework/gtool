from setuptools import setup, find_packages

setup(name='gtool',
      version='0.1.4',
      author='Ben Sapiro',
      author_email = "https://ca.linkedin.com/in/sapiro",
      license='GPLv3',
      keywords='security risk governance compliance framework',
      description=('A framework for building security governance, risk and compliance tools.'),
      long_description="G.Tool is a framework for building governance, risk and compliance security tools. It's a barebones framework, that is highly extensible but comes with a a lot of common functionality included.",
      download_url = 'https://github.com/gtoolframework/gtool/tarball/0.1.4',
      url='https://gtoolframework.github.io/',
      packages=find_packages(),
      include_package_data=True,
      install_requires=[
          'boltons>=16.5.0',
          'click>=6.6',
          'configparser>=3.5.0',
          'decorator>=4.0.10',
          'patricia-trie>=10',
          'pluginbase>=0.4',
          'pyparsing>=2.1.9',
          'PyYAML>=3.12',
          'simpleeval>=0.8.7',
          'six>=1.10.0',
          'validators>=0.11.0',
          'XlsxWriter>=0.9.3'
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