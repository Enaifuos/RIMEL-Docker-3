import os

from scripts.AnalysisScript import runAnalysis
from scripts.AnalysisStatistics import getStatisticsFromAllFiles
from scripts.release_scripts.get_nb_of_ev import get_nb_of_EV

import matplotlib.pyplot as plt
import json

project_path = '../../../thingsboard'
current_path_from_project_path = '../RIMEL-Docker-3/scripts/release_scripts'
project_env_files_path = './docker'
script_tag_path = '../scriptTag.sh'
tags_path = './tags.json'

def retrieve_stats(nbEV, complexities, nloc):
    nbEV.append(get_nb_of_EV())

    data = getStatisticsFromAllFiles(runAnalysis('.'))

    complexity = json.loads(data['ccn'])
    print(complexity)
    complexities.append((complexity['avg'], complexity['median']))

    nloc_data = json.loads(data['nloc'])
    print(nloc_data)
    nloc.append((nloc_data['avg'], nloc_data['median']))

    return nbEV, complexities, nloc

def git_checkout(commit):
    os.system('git checkout ' + commit)

def change_directory(path):
    os.chdir(path)

def plot_stats(x, y, title, x_axis, y_axis):
    avg_data = [el[0] for el in y]
    md_data = [el[1] for el in y]

    plt.style.use('ggplot')
    plt.plot(x, avg_data, color='red')
    plt.plot(x, md_data, color='green')
    plt.title(title)
    plt.xlabel(x_axis)
    plt.ylabel(y_axis)
    plt.show()

def plot(x, y, title, x_axis, y_axis):
    plt.style.use('ggplot')
    plt.plot(x, y, color='blue')
    plt.title(title)
    plt.xlabel(x_axis)
    plt.ylabel(y_axis)
    plt.show()

def count(directory):
    releases = []
    nbEV = []
    complexities = []
    nloc = []

    f = open(tags_path, 'r')
    logs_json = json.load(f)


    change_directory(project_path)
    print(os.getcwd())

    i = 0
    for release in logs_json:
        commit = logs_json[release]
        git_checkout(commit)

        releases.append(release)
        nbEV, complexities, nloc = retrieve_stats(nbEV, complexities, nloc)
        i+=1
        if i>1:
            break;

    git_checkout('master')
    change_directory(current_path_from_project_path)

    return releases, nbEV, complexities, nloc

if __name__ == "__main__":

    # Generating tags.json
    os.system(script_tag_path + ' ' + project_path)

    releases, nbEV, complexities, nloc = count(project_env_files_path)
    print(releases, nbEV, complexities, nloc)

    plot(releases, nbEV, 'Evolution of the NB of EV', 'releases', 'nb of EV')
    plot_stats(releases, complexities, 'Evolution of the complexity', 'releases', 'complexity')
    plot_stats(releases, nloc, 'Evolution of the NLOC per method', 'releases', 'NLOC per method')