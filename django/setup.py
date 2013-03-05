#!/usr/bin/env python
#
# This is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this software. If not, see <http://gnu.org/licenses/>.

from distutils.core import setup

setup(
    name='django-timesink',
    version=__import__('timesink').__version__,
    license = 'GNU Lesser General Public License (LGPL), Version 3',

    requires = ['python (>= 2.5)', 'django (>= 1.2)', 'eav (>= 0.9)'],
    provides = ['timesink'],

    description='Timesink protocol implementation as a reusable Django app.',
    # long_description=open('README.rst').read(),

    url='http://github.com/Noupghmad/timesink',

    packages=['timesink'],

    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
        'Programming Language :: Python',
        'Topic :: Database',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)