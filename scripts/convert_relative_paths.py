from os.path import abspath, join, dirname
__dirname = abspath(dirname(__file__))

DATA  = abspath(join(__dirname, '..', 'data'))
INDEX = abspath(join(DATA, 'index.json'))
REL_INDEX = abspath(join(DATA, 'relative_index.json'))

with open(INDEX, 'r') as in_file, open(REL_INDEX, 'w') as out_file:
    for line in in_file:
        out_file.write(line.replace(DATA, '.'))
