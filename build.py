import os, datetime, json, yaml, sys, string
import gzip
import zlib
import hashlib
import dbtools


db = {}
version = int(datetime.date.today().strftime('%Y%m%d'))
db['games'] = {}
db['locations'] = {}
db['version'] = version

dirs = list(string.ascii_lowercase)
dirs.append('#')

latestdb = {}

print('Building database...')

games = dbtools.load('games')

for game, data in games.items():
    gid = game
    dbgame = {}
    dbgame['name'] = data['name']
    if 'contributors' in data:
        dbgame['contributors'] = data['contributors']
    db['games'][gid] = dbgame

    for num, loc in enumerate(data['locations']):
        locid = '{}:{}'.format(gid, num) 
        db['locations'][locid] = loc
                    
if not os.path.isdir('output'): os.mkdir('output')

with gzip.open('output/gamedata', 'wt') as dbfile:
    json.dump(db, dbfile)


with open('output/gamedata', 'rb') as dbfile:
    data = dbfile.read()
    latestdb['hash'] = hashlib.sha1(data).hexdigest()

latestdb['url'] = 'http://strata.me/gamedata'
latestdb['version'] = version

print('Build complete.')
print('Version:', version)
print('Games:', len(games))
print('Hash:', latestdb['hash'])

with open('output/latestdb.json', 'w') as dbfile:
    json.dump(latestdb, dbfile)





