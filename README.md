# mdfmonitor - Monitor the file moification

The **mdfmonitor** is Python module about monitoring files modification using timestamp and body.

## How to Use

It's simple. 

1. Import this module.
2. Create `ModificationMonitor` class's instance.
3. Append file or files to instance using add_file method.
4. using Python for sentence, You can write anything under for sentence.

```python
#!/usr/bin/python

import os
from mdfmonitor import ModificationMonitor

files = os.listdir(".") # >>> ['sample.txt', 'sample.py']

# create Watcher instnce
monitor = Watcher()

# append file to mdfmonitor instance
monitor.add_file("sample.txt")

# or 

# append files to mdfmonitor instance
monitor.add_files(os.listdir("."))

# start watch using with sentence
# you can write anything under for sentence.
# If mdfmonitor catch file modification, mdfmonitor run anything you written
for mdf in monitor.monitor():
    
    print mdf.file.center(30, "=")
    print "Catch the Modification!!"
    print "Old timestamp: %s" % mdf.old_mtime
    print "New timestamp: %s" % mdf.new_mtime
    print "manager: %s" % str(mdf.manager.o_repository)
    print "Diff".center(30,"=")
    print mdf.diff

```

