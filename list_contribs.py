import dbtools

games = dbtools.load('games')
contribs = {}

for game, data in games.items():
    if 'contributors' in data:
        contributors = data['contributors']

        for c in contributors:
            if not c in contribs:
                contribs[c] = 1
            else: contribs[c] += 1

for c in reversed(sorted(contribs, key=lambda p: contribs[p])):
    print(c)
  
