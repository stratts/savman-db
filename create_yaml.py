import yaml, string, os, sys
from collections import OrderedDict


def represent_ordereddict(dumper, data):
    value = []

    for item_key, item_value in data.items():
        node_key = dumper.represent_data(item_key)
        node_value = dumper.represent_data(item_value)

        value.append((node_key, node_value))

    return yaml.nodes.MappingNode(u'tag:yaml.org,2002:map', value)

yaml.SafeDumper.add_representer(OrderedDict, represent_ordereddict)

def autoid(name):
    wlist = []
    name = name.replace('-',' ')
    subabbr = ''
    replace = {'II':'2', 'III':'3', 'IV':'4', 'V':'5', 'VI':'6', 'VII':'7', 'VIII':'8',
            'IX':'9', 'X':'10', 'XI':'11', 'XII':'12', 'XIII':'13', '&':'And','HD':'HD'}
    valid = list(string.ascii_letters+string.digits)+list(replace)
    split = name.split(':', maxsplit=1)
    if len(split) > 1 and len(name) > 32:
        subs = split[1].strip().split(' ')
        if len(subs) > 1:
            for sub in subs:
                sub = ''.join([ x for x in list(sub) if x in valid ])
                if sub: subabbr += replace[sub] if sub in replace else sub[0].upper()
            name = split[0]
        
    for word in name.split(' '):
        if word.lower() == 'the': continue
        chars = [ x.lower() for x in list(word) if x in valid ]
        if chars: chars[0] = chars[0].upper()
        new = ''.join(chars)
        if new.upper() in replace: wlist.append(replace[new.upper()])
        else: wlist.append(new)

    wlist.append(subabbr)
    newname = ''.join(wlist)
    return newname

varpaths = {'appdata': os.path.normpath(os.path.join(os.environ['APPDATA'], '..')),
           'userdoc': os.path.join(os.environ['USERPROFILE'], 'Documents'),
           'userprofile': os.environ['USERPROFILE']}


while True:
    while True:
        name = input('Enter the game name: ')
        if len(name) > 2: break
        else: print('Error: Name must be 3 characters or longer')

    while True:
        valid = True
        gid = autoid(name)
        if not len(gid) > 3:
            print('Error: ID must be 3 characters or longer')
            continue
        for char in gid:
            if not char in string.ascii_letters and not char in string.digits:
                print('Error: ID must only contain letters and numbers. Please try again')
                valid = False
                break      
        if valid: break
    print('Generated id: {}'.format(gid))


    types = {'1': 'variable', '2': 'profile'}
    variables = { '1': 'appdata', '2': 'userdoc', '3': 'userprofile'}
    for key, value in types.copy().items(): types[value] = value
    for key, value in variables.copy().items(): variables[value] = value

    print(
    '''
Choose the method to use when finding the directory:
    1. Environment Variable [variable]
           Find the directory by associating it with an environment
           variable that points to a location (eg, AppData, Documents)
    2. Directory Profile [profile]
           Input a list of items that you would find in the directory.
           This profile will then be used to match it when scanning
           for games on a computer.
    '''
            )


    while True:
        c = input('Enter your choice - you may use the number or the id: ')
        valid = True
        if not c in types:
            print("Error: '{}' is not a valid option.".format(c))
            valid = False
        if valid:
            ltype = types[c]
            break

    if ltype == 'variable':
        print(
        '''
Choose a variable to associate the save directory with:
    1. AppData [appdata] ({}) 
    2. User Documents [userdoc] ({})
    3. User Profile [userprofile] ({})
        '''.format(varpaths['appdata'], varpaths['userdoc'], varpaths['userprofile'])
            )
        while True:
            c = input('Enter your choice - you may use the number or the id: ')
            valid = True
            if not c in variables:
                print("Error: '{}' is not a valid option.".format(c))
                valid = False
            if valid:
                lvar = variables[c]
                break

        print("The current path is '{}'".format(varpaths[lvar]))

    if ltype == 'profile':
        pname = input('Choose the name of the directory to match (optional): ')
        while True:
            pitemstr = input('Enter a list of items in the directory to match, separated by commas:\n')
            if not len(pitemstr) > 2:
                print('Error: You must enter at least one item with a length of 3 characters.')
                continue
            else: break
        
        pitems = [ i.strip() for i in pitemstr.split(',') ]
        print(pitems)

        pbase = '[directory that contains {}]'.format(', '.join(pitems))
        print("The current path is '{}'".format(os.path.normpath(pbase)))
        
    subdir = input('Enter the sub directory (optional): ')
    if subdir:
        if ltype == 'profile': print("The current path is '{}'".format(os.path.normpath(os.path.join(pbase, subdir))))
        if ltype == 'variable': print("The current path is '{}'".format(os.path.normpath(os.path.join(varpaths[lvar], subdir))))
    if not subdir: subdir = None

    includes = input('Enter paths/files to include, separated by commas (optional):\n')
    includes = [ i.strip() for i in includes.split(',') ] if includes else None

    excludes = input('Enter paths/files to exclude, separated by commas (optional):\n')
    excludes = [ e.strip() for e in excludes.split(',') ] if excludes else None

    #location = OrderedDict( [('type',ltype), ('root',root),('folders',folders),
                          #  ('gamedir',gamedir), ('file',file)] )
    location = OrderedDict()
    l = location
    l['type'] = ltype
    if ltype == 'variable': l['variable'] = lvar
    if subdir: l['subdir'] = subdir    
    if ltype == 'profile':
        if pname: l['profile_dir'] = pname
        l['profile_items'] = pitems
    if includes: l['include'] = includes
    if excludes: l['exclude'] = excludes
        
    game = OrderedDict([('name',name),('id',gid), ('locations',[location])])

    with open('{}.yaml'.format(gid),'w') as yfile:
        yaml.safe_dump(game, yfile, default_flow_style=False,indent=4)

    print("Saved to '{}.yaml'\n".format(gid))

    cont = input('Would you like to add a new game? [y|n]\n')
    if cont == 'y':
        os.system('cls')
        continue
    else: break


    
