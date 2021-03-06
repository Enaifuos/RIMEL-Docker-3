# Counts the number of environment variables in a directory
# Suggesting that all EV are stored in .env files

import os

def get_EV_declaration_files(current_path):
    files = []
    for r, d, f in os.walk(current_path):
        for file in f:
            if is_env_file(file):
                files.append(os.path.join(r, file))
            if is_docker_compose_file(file):
                files.append(os.path.join(r, file))
    return files

def is_env_file(file):
    if '.env' in file or '_env' in file:
        if 'envoy' in file:
            return False
        return True
    else:
        return False

def is_docker_compose_file(file):
    if 'docker-compose' in file:
        if 'docker-compose.template' not in file and 'docker-compose.test' not in file:
            return True
    return False



def get_EV_in_docker_compose(f):
    env_list = []
    lines = [line for line in f]
    is_in_environment = True
    for line_index in range(0, len(lines)):
        line = lines[line_index]
        if 'environment' in line:
            is_in_environment = True
        else:
            if is_in_environment:
                new_ev = count_nb_of_EV_docker_compose(line_index, lines)
                if new_ev is None:
                    is_in_environment = False
                else:
                    env_list.append(new_ev)
    return env_list

def count_nb_of_EV_docker_compose(line_index, lines):
    line = lines[line_index]

    bool, delimiter, line = get_delimiter(line)
    if bool:
        var = line.split(delimiter)[0].strip()
        if check(var):
            return var
    return None

def get_delimiter(line):
    if ': ' in line:
        return True, ': ', line
    if '=' in line:
        return True, '=', line.split('-')[1]
    else:
        return False, '', line

def check(line):
    if 'env_file' in line:
        return False
    if 'restart' in line:
        return False
    if 'entry_point' in line:
        return False
    if 'command' in line:
        return False
    if '#' in line:
        return False
    if not line.strip():
        return False
    return True

def count_EV(files_paths):
    os.system('pwd')
    EV = []
    for file_path in files_paths:
        file = open(file_path, 'r')
        if '.env' in file.name or '_env' in file.name:
            for line in file:
                ve = line.split("=")[0]
                if check(ve):
                    EV.append(line.split("=")[0])
        if 'docker-compose' in file.name:
            nb_EV_in_DC = get_EV_in_docker_compose(file)
            EV.extend(nb_EV_in_DC)
        file.close()
    EV = list(dict.fromkeys(EV))
    return EV

def get_nb_of_EV():
    return len(list_of_EV())

def list_of_EV():
    files = get_EV_declaration_files('.')
    EV = count_EV(files)
    return EV

def do(project):
    print(project)
    os.system('git checkout master')
    #os.system('git pull')
    ev_list = list(dict.fromkeys(list_of_EV()))
    print(ev_list)
    print(len(ev_list))

if __name__ == "__main__":
    os.system("pwd")
    os.chdir('../..')

    os.chdir('../magma')
    do('MAGMA')
    #104

    os.chdir('../thingsboard')
    do('THINGSBOARD')
    #64

    os.chdir('../openmrs-sdk')
    do('OPENMRS-SDK')
    #16

    os.chdir('../skywalking')
    do('SKYWALKING')
    #8

    os.chdir('../elasticsearch')
    do('ELASTIC')
    #42