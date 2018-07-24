# ATTENTION
This project has deprecated, and inherited to the **[JustWatch](https://github.com/alice1017/justwatch) project.**

# mdfmonitor - Monitor the file moification

The **mdfmonitor** is Python module about monitoring files modification using timestamp and body.

The **mdfmonitor** contains:

 - **FileModificationMonitor**
 - **URLModificationMonitor**

## FileModificationMonitor

This FileModificationMonitor (call this *monitor* from now) can monitor to a **file** or files modification.

Monitor has the repository of file's **timestamp** data and **body** data.
And monitor appends each data, then monitor **compare** new data to old data.
If new data **differ** to old data, monitor **regard** this difference to **modification**.
Then monitor create instance of FileModificationObject, yield this.


### How to Use

It's simple. 

1. Import this module.
2. Create `FileModificationMonitor` class's instance.
3. Append file or files to instance using add_file method.
4. using Python for sentence, You can write anything under for sentence.

```python
#!/usr/bin/python

import os
from mdfmonitor import FileModificationMonitor

files = os.listdir(".") # >>> ['sample.txt', 'sample.py']

# create Watcher instnce
monitor = FileModificationMonitor()

# append file to mdfmonitor instance
monitor.add_file("sample.txt")

# or 
# append files to mdfmonitor instance
monitor.add_files(os.listdir("."))

for mdf in monitor.monitor():
    
    print mdf.file.center(30, "=")
    print "Catch the Modification!!"
    print "Old timestamp: %s" % mdf.old_mtime
    print "New timestamp: %s" % mdf.new_mtime
    print "manager: %s" % str(mdf.manager.o_repository)
    print "Diff".center(30,"=")
    print mdf.diff

```

## URLModificationMonitor

This URLModificationMonitor (call this *monitor* from now) can monitor to **body of url** or urls modification.

This monitor's structure **almost same** to FileModificationMonitor.
Both monitor just difference is to time data what compare.
FileModificationMonitor gets a file **timestamp**, URLModificationMonitor gets the `Date` header's **date** of server.


### How to Use

It's simple too. 

1. Import this module.
2. Create `URLModificationMonitor` class's instance.
3. Append url string or url string's list to instance using add_url method.
4. using Python for sentence, You can write anything under for sentence.

```python
#!/usr/bin/python

import os
from mdfmonitor import URLModificationMonitor

files = os.listdir(".") # >>> ['sample.txt', 'sample.py']

# create Watcher instnce
monitor = URLModificationMonitor()

# append file to mdfmonitor instance
monitor.add_url("http://sampe.com/path/")

for mdf in monitor.monitor():
    
    print mdf.url.center(30, "=")
    print "Catch the Modification!!"
    print "Old timestamp: %s" % mdf.old_dtime
    print "New timestamp: %s" % mdf.new_dtime
    print "manager: %s" % str(mdf.manager.o_repository)
    print "Diff".center(30,"=")
    print mdf.diff

```


## How to install

You can use pip or easy_install.

```shell
$ sudo easy_install mdfmonitor
```

Or, use git.

```shell
$ git clone https://github.com/alice1017/mdfmonitor.git
$ cd mdfmonitor
$ sudo pyton setup.py build install
```

## LICENSE

Copyright (c) 2014 Hayato, Tominaga

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

