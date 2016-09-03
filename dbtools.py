import os
import yaml
import sys
import string
from collections import OrderedDict

_mapping_tag = yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG
dirs = list(string.ascii_lowercase)
dirs.append('#')

def dict_representer(dumper, data):
    return dumper.represent_dict(data.items())

def dict_constructor(loader, node):
    return OrderedDict(loader.construct_pairs(node))

yaml.SafeDumper.add_representer(OrderedDict, dict_representer)
yaml.SafeLoader.add_constructor(_mapping_tag, dict_constructor)

def load(directory):
    games = {}
    for d in os.listdir(directory):
        subd = os.path.join(directory, d)
        if d in dirs and os.path.isdir(subd):
            for f in os.listdir(subd):
                fpath =  os.path.join(subd, f)
                if os.path.isfile(fpath) and f.endswith('.yaml'):
                    with open(fpath) as y:
                        game = yaml.safe_load(y)
                        if {'id', 'name', 'locations'} <= game.keys():
                            gid = game['id']
                            del game['id']
                            games[gid] = game
                            
    return games
    
def save(games, directory):
    try:
        if not os.path.isdir(directory): os.mkdir(directory)
        for d in dirs:
            dpath = os.path.join(directory, d)
            if not os.path.isdir(dpath): os.mkdir(dpath)
        for game, data in games.items():
            if not {'name', 'locations'} <= data.keys(): continue
            
            let = game[0].lower()
            if let in dirs: letpath = os.path.join(directory, let)
            else: letpath =  os.path.join(directory, '#')
            
            data['id'] = game
            data.move_to_end('id', last=False)
            
            ypath = os.path.join(letpath, '{}.yaml'.format(game))
            with open(ypath, 'w') as yfile:
                yaml.safe_dump(data, yfile, default_flow_style=False, indent=4)
                
    except AttributeError: 
        raise TypeError(
            "'games' argument must be 'dict', not '{}'".format(
                type(games).__name__)
            )
