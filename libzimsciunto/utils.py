#!/usr/bin/env python

#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>


"""
A couple of useful functions...
"""

import re
import os

def protect(s):
    """
    Protect Metacaracters in a string
    (add a \\ before)

    :param s: string
    :returns: protected string
    """
    s = re.sub('\&', '\\\&', s)
    s = re.sub('\[', '\\\[', s)
    s = re.sub('\]', '\\\]', s)
    s = re.sub('\|', '\\\|', s)
    s = re.sub('\?', '\\\?', s)
    return s

def get_unexpanded_path(path):
    """
    if start by /home/foo,
    convert /home/foo by ~ in a path

    >>> get_unexpanded_path('/home/gnu/dir')
    '~/dir'
    >>> get_unexpanded_path('/tmp/foo')
    '/tmp/foo'
    >>> get_unexpanded_path('/home/fr/foo/home/bar')
    '~/foo/home/bar'
    """
    path = re.sub('^/home/[a-zA-Z0-9]*/', '~/', str(path))
    return path

def create_pidfile(filename):
    """
    Create a pidfile

    :param filename: name of the pid file
    """
    filename = os.path.expanduser(filename)
    if os.access(filename, os.F_OK):
        #Oh oh, there is a lock file
        with open(filename, "r") as pidfile:
            pidfile.seek(0)
            old_pd = pidfile.readline()
        #PID is running?
        if os.path.exists("/proc/%s" % old_pd):
            #Yes
            print('An instance is already running, exiting')
            sys.exit(1)
        else:
            #No
            os.remove(filename)

    with open(filename, "w") as pidfile:
        pidfile.write("%s" % os.getpid())

def release_pidfile(filename):
    """
    Release the pidfile

    :param filename: name of the pid file
    """
    os.remove(os.path.expanduser(filename))


def _test():
    import doctest
    doctest.testmod()

if __name__ == '__main__':
    _test()
