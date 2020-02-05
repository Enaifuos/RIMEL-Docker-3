# Counts the number of environment variables in a directory
# Suggesting that all EV are stored in .env files

import os

def is_EV(line):
    if line[0] == '#' or not line.strip():
        return False
    else:
        return True

def get_EV_declaration_files():
    files = []
    for r, d, f in os.walk('.'):
        for file in f:
            if '.env' in file:
                files.append(os.path.join(r, file))
    return files

def count_EV(files_paths):
    nb_EV = 0
    for file_path in files_paths:
        file = open(file_path, 'r')
        for line in file:
            if is_EV(line):
                nb_EV += 1
    return nb_EV

def get_nb_of_EV():
    files = get_EV_declaration_files();
    return count_EV(files)

