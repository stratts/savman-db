import os
import sys
import json
import zlib
import hashlib
import gzip
import random

##tdirs = []
##tfiles = []
##
##for root, dirs, files in os.walk('C:/'):
##    for file in files:
##        if len(file) > 24: tfiles.append(file[:24])
##        else: tfiles.append(file)
##    for d in dirs:
##        if len(d) > 24: tfiles.append(file[:24])
##        else: tdirs.append(d)
##
##with gzip.open('files', 'wt') as f:
##    pack = json.dump(tfiles, f)
##
##with gzip.open('dirs', 'wt') as f:
##    pack = json.dump(tdirs, f)
##
##sys.exit()
dirs = []
files = []

db = {}
version = 20180305
db['games'] = {}
db['locations'] = {}
db['version'] = version

def randchoices(seq, num):
    return [ random.choice(seq) for _ in range(num) ]

with gzip.open('files', 'rt') as file:
    files = json.load(file)

with gzip.open('dirs', 'rt') as file:
    dirs = json.load(file)

for _ in range(3000):
    words = randchoices(dirs, 2)
    name = ' '.join(words)
    gid = ''.join(words)
    contribs = randchoices(dirs, 2)

    db['games'][gid] = {'name': name, 'contributors': contribs}

    locid = '{}:0'.format(gid)
    ltype = 'variable'
    lvar = random.choice(['userdoc','appdata','userprofile'])
    subdir = os.path.join(*randchoices(dirs, 3))
    linclude = randchoices(files, 2)
    db['locations'][locid] = {'type': ltype, 'variable':lvar, 'subdir': subdir,
                              'include': linclude}

    locid = '{}:1'.format(gid)
    ltype = 'profile'
    lname = name
    subdir = random.choice(dirs)
    litems = randchoices(files, 3)
    lexclude = randchoices(files, 2)
    db['locations'][locid] = {'type': ltype, 'profile_dir': lname, 'subdir': subdir,
                              'profile_items': litems, 'exclude': lexclude}

with gzip.open('dummydata', 'wt') as dbfile:
    json.dump(db, dbfile)







