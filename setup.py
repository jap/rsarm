#!/usr/bin/env python

from distutils.core import setup

from sys import version
if version < '2.2.3':
    from distutils.dist import DistributionMetadata
    DistributionMetadata.classifiers = None
    DistributionMetadata.download_url = None
setup(name = 'rsarm',
        version = '0.9',
        description = 'Reed Solomon Armor',
        author = 'Jasper Spaans',
        author_email = 'j@jasper.es',
        classifiers = [
              'Development Status :: 4 - Beta',
              'License :: OSI Approved :: GNU General Public License (GPL)',
              'Programming Language :: Python :: 2',
           ],
        packages = ['rsarm'],
        requires = ['reedsolomon'],
        entry_points={ 'console_scripts': ['rsarm = rsarm.rsarm:main' ] },
        )
