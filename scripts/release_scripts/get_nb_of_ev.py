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
    if ': ' in lines[next_line_index]:
        ev_list.append(lines[next_line_index].split(': ')[0])
        next_line_index += 1
        ev_list.extend(count_nb_of_EV_docker_compose(next_line_index, lines, ev_list))
    return ev_list


def count_EV(files_paths):
    nb_EV = 0
    EV = []
    for file_path in files_paths:
        file = open(file_path, 'r')
        if '.env' in file_path:
            for line in file:
                if is_EV(line):
                    nb_EV += 1
                    EV.append(line.split("=")[0])
        if 'docker-compose' in file_path:
            nb_EV_in_DC = get_EV_in_docker_compose(file_path)
            nb_EV += len(nb_EV_in_DC)
            EV.extend(nb_EV_in_DC)
    return nb_EV, EV

def get_nb_of_EV():
    files = get_EV_declaration_files('.')
    nb_EV, EV = count_EV(files)
    return nb_EV

def list_of_EV():
    files = get_EV_declaration_files('.')
    nb_EV, EV = count_EV(files)
    return EV

if __name__ == "__main__":
    os.system("pwd")
    os.chdir('../../../thingsboard')
    print(list_of_EV())
    print(get_nb_of_EV())