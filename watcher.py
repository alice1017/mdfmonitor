#!/usr/bin/env python
#coding: utf-8

import os
import sys
import time
import difflib

class DuplicationError(BaseException):
    """Raise this Error if you add duplication file."""

    pass

class Watcher(object):

    def __init__(self):

        self.f_repository = []

    def add_file(self, file, **kwargs):

        if os.access(file, os.F_OK):

            if file in self.f_repository:
                raise DuplicationError("file already added.")

            self.f_repository.append(file)

        else:
            raise IOError("file not found.")


    def add_files(self, filelist, **kwargs):

        # check filelist is list type
        if not isinstance(filelist, list):
            raise TypeError("request the list type.")
        
        for file in filelist:
            self.add_file(file)    

    def watch(self, sleep=5):
        
       monitor = FileModificationMonitor(self.f_repository, sleep) 
       return monitor.monitoring()


class FileModificationMonitor(object):

    def __init__(self, f_repository, sleep=5):

        self.f_repository = f_repository
        self.sleep = sleep

    def monitoring(self):

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
                
            time.sleep(self.sleep)
            
            
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
        self.manager = None

        self.new_mtime, self.old_mtime = t_mtime
        self.new_fbody, self.old_fbody = t_fbody


    def _set_manager(self, manager):

        self.manager = manager

    def show_diff(self):

        for line  in difflib.unified_diff(
                        self.old_fbody.splitlines(),
                        self.new_fbody.splitlines(),
                        "old/"+self.file, "new/"+self.file,
                        self._strftime(self.old_mtime),
                        self._strftime(self.new_mtime)):
            print line

    def _strftime(self, etime):
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(etime)),
