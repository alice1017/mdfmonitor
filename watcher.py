#!/usr/bin/env python
#coding: utf-8

import os
import sys

class Watcher(object):

    def __init__(self):

        self.f_repository = []

    def add_file(self, file, **kwargs):

        if os.access(file, os.F_OK):
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
        
       monitor = FileMonitor(self.f_repository, sleep) 
       return monitor.monitoring()

class FileMonitor(object):

    def __init__(self, f_repository, sleep=5):

        self.f_repository = f_repository
        self.sleep = sleep

    def monitoring(self):

        manager = FileModificationManager()


        while True:

            # process of file modification catching

            # file modification to object
            new_obj = FileModificationObject()

            # append file modification object to manager
            manager.add_object(new_obj)

            # return new modification object
            yield new_obj

            time.sleep(sleep)


class FileModificationManager(object):

    def __init__(self):

        self.obj_repository = []

        self.__is_iterable = False
        self.__r_pointer = 0


    def add_object(self, obj):

        self.obj_repository.append(obj)

        if not __is_iterable:
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

        if self.__r_pointer == len(self.obj_repository):
            raise StopIteration

        result = self.obj_repository[self.__r_pointer]
        self.__r_pointer += 1
        return result
        
    def __next__(self):

        return self.next()

    def seek(self, offset):

        self.__r_pointer = offset

class FileModificationObject(object):

    def __init__(self):

        return


