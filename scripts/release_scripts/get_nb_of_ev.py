# Counts the number of environment variables in a directory
# Suggesting that all EV are stored in .env files

import os

def is_EV(line):
    if line[0] == '#' or not line.strip():
        return False
    else:
        return True

def get_EV_declaration_files(current_path):
    files = []
    for r, d, f in os.walk(current_path):
        for file in f:
            if '.env' in file:
                files.append(os.path.join(r, file))
            if 'docker-compose' in file:
                files.append(os.path.join(r, file))
    return files

def get_EV_in_docker_compose(file):
    env_list = []
    f = open(file, 'r')
    lines = [line for line in f]
    for line_index in range(0, len(lines)):
        line = lines[line_index]
        if 'environment' in line:
            env_list.extend(count_nb_of_EV_docker_compose(line_index, lines, []))
    return env_list

def count_nb_of_EV_docker_compose(line_index, lines, ev_list):
    next_line_index = line_index + 1
    line = lines[next_line_index]
    if ': ' in line and is_line_a_DC_keyword(line):
        ev_list.append(line.split(': ')[0].strip())
        if next_line_index < len(lines)-1:
            next_line_index += 1
            ev_list.extend(count_nb_of_EV_docker_compose(next_line_index, lines, ev_list))
    return ev_list

def is_line_a_DC_keyword(line):
    if 'env_file' in line:
        return True
    if 'restart' in line:
        return True
    if 'entry_point' in line:
        return True
    return False

def count_EV(files_paths):
    EV = []
    for file_path in files_paths:
        file = open(file_path, 'r')
        if '.env' in file_path:
            for line in file:
                if is_EV(line):
                    EV.append(line.split("=")[0])
        if 'docker-compose' in file_path:
            nb_EV_in_DC = get_EV_in_docker_compose(file_path)
            EV.extend(nb_EV_in_DC)
    EV = list(dict.fromkeys(EV))
    return EV

def get_nb_of_EV():
    return len(list_of_EV())

def list_of_EV():
    files = get_EV_declaration_files('.')
    EV = count_EV(files)
    return EV

if __name__ == "__main__":
    os.system("pwd")
    os.chdir('../../../magma')
    print(list_of_EV())
    print(get_nb_of_EV())