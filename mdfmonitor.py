#!/usr/bin/env python
#coding: utf-8

"""
mdfmonitor - Monitor the file moification
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The **mdfmonitor** is Python module about monitoring files modification using timestamp and body.

How to use:

It's simple. 
1. Import this module.
2. Create `ModificationMonitor` class's instance.
3. Append file or files to instance using add_file method.
4. using Python for sentence, You can write anything under for sentence.

    >>> from mdfmonitor import ModificationMonitor
    >>> monitor = ModificationMonitor()
    >>> monitor.add_file("README.md")
    >>> for mdf in monitor.monitor():
    ...     print "Old timestamp: %s" % mdf.old_mtime
    ...     print "New timestamp: %s" % mdf.new_mtime
    ...     print "manager: %s" % str(mdf.manager.o_repository)
    ...     print "Diff".center(30,"=")
    ...     print mdf.diff

"""

import os
import sys
import time
import difflib

__version__ = "0.1.1b"

class DuplicationError(BaseException):
    """Raise this Error if you add duplication file."""

    pass

class ModificationMonitor(object):
    """The ModificationMonitor can monitoring file modification.
    usage:

    it's simple.
    1. Create instance (call this instance `monitor` from now).
    2. Append file to instance using `add_file` or `add_files` method.
       Monitor has a file repository, monitor append file to repository using 
       `add_file` method. Please put a file name to argument. If you use 
       `add_files` method and put list of file to argument, Monitor append 
       files to repository.
    3. Run monitor uring `monitor` method.
       The `monitor` method is generator, return FileModificationObject.

    """

    def __init__(self):

        self.f_repository = []

    def add_file(self, file, **kwargs):
        """Append a file to file repository.

        For file monitoring, monitor instance needs file.
        Please put the name of file to `file` argument.

        :param file: the name of file you want monitor.

        """

        if os.access(file, os.F_OK):

            if file in self.f_repository:
                raise DuplicationError("file already added.")

            self.f_repository.append(file)

        else:
            raise IOError("file not found.")


    def add_files(self, filelist, **kwargs):
        """Append files to file repository.
        
        ModificationMonitor can append files to repository using this.
        Please put the list of file names to `filelist` argument.

        :param filelist: the list of file nmaes
        """

        # check filelist is list type
        if not isinstance(filelist, list):
            raise TypeError("request the list type.")

        for file in filelist:
            self.add_file(file)    

    def monitor(self, sleep=5):
        """Run file modification monitor.

        The monitor can catch file modification using timestamp and file body.
        Monitor has timestamp data and file body data. And insert timestamp 
        data and file body data before into while roop. In while roop, monitor 
        get new timestamp and file body, and then monitor compare new timestamp
        to originaltimestamp. If new timestamp and file body differ original,
        monitor regard thease changes as `modification`. Then monitor create
        FileModificationObject, yield this object.

        :param sleep: How times do you sleep in while roop.
        """


        manager = FileModificationObjectManager()

        timestamps = {}
        filebodies = {}

        # register original timestamp and filebody to dict
        for file in self.f_repository:
            timestamps[file] = self._get_mtime(file)
            filebodies[file] = open(file).read()


        while True:

            # file modification to object
            for file in self.f_repository:

                mtime = timestamps[file]
                fbody = filebodies[file]

                checker = self._check_modify(file, mtime, fbody)

                # file not modify -> continue
                if not checker:
                    continue

                # file modifies -> create the modification object

                new_mtime = self._get_mtime(file)
                new_fbody = open(file).read()

                obj = FileModificationObject(
                        file,
                        (mtime, new_mtime),
                        (fbody, new_fbody) )

                # overwrite new timestamp and filebody
                timestamps[file] = new_mtime
                filebodies[file] = new_fbody


                # append file modification object to manager
                manager.add_object(obj)

             # return new modification object
                yield obj

            time.sleep(sleep)


    def _get_mtime(self, file):

        return os.stat(file).st_mtime


    def _check_modify(self, file, o_mtime, o_fbody):

        n_mtime = self._get_mtime(file)
        n_fbody = open(file).read()

        if n_mtime == o_mtime:
            return False

        else:

            if n_fbody == o_fbody:
                return False

            else:

                return True


class FileModificationObjectManager(object):
    """

    """

    def __init__(self):

        self.o_repository = []

        self.__is_iterable = False
        self.__r_pointer = 0


    def add_object(self, obj):

        self.o_repository.append(obj)

        obj._set_manager(self)

        if not self.__is_iterable:
            self.__is_iterable = True

        return self

    def __iter__(self):

        if not self.__is_iterable:
            raise TypeError(
                    "'%s' object is not iterable" % self.__class__.__name__)
            return self

    def next(self):

        if not self.__is_iterable:
            raise TypeError(
                    "'%s' object is not iterable" % self.__class__.__name__)

            if self.__r_pointer == len(self.o_repository):
                raise StopIteration

        result = self.o_repository[self.__r_pointer]
        self.__r_pointer += 1
        return result

    def __next__(self):

        return self.next()

    def seek(self, offset):

        self.__r_pointer = offset

class FileModificationObject(object):

    def __init__(self, file, t_mtime, t_fbody):

        self.file = file

        self.new_mtime, self.old_mtime = t_mtime
        self.new_fbody, self.old_fbody = t_fbody

        self.manager = None
        self.diff = self._diffgen()

    def _set_manager(self, manager):

        self.manager = manager

    def _diffgen(self):

        contents = []

        for line  in difflib.unified_diff(
                self.old_fbody.splitlines(),
                self.new_fbody.splitlines(),
                "old/"+self.file, "new/"+self.file,
                self._strftime(self.old_mtime),
                self._strftime(self.new_mtime)):

            contents.append(line)

        return "\n".join(contents)

    def _strftime(self, etime):
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(etime))


