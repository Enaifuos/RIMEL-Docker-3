import os

from scripts.AnalysisScript import runAnalysis
from scripts.AnalysisStatistics import getStatisticsFromAllFiles
from scripts.release_scripts.get_nb_of_ev import get_nb_of_EV

import matplotlib.pyplot as plt
import json

project_path = '/home/passport/Repos/tmp/thingsboard'
current_path_from_project_path = '../RIMEL-Docker-3/scripts/release_scripts'
project_env_files_path = './docker'
script_tag_path = '../scriptTag.sh'
tags_path = './tags.json'

def retrieve_stats(nbEV, complexities, nloc):
    nbEV.append(get_nb_of_EV())

    data = getStatisticsFromAllFiles(runAnalysis('.'))

    complexities.append(json.loads(data['ccn'])['avg'])
    nloc.append(json.loads(data['nloc'])['avg'])

    return nbEV, complexities, nloc

def git_checkout(commit):
    os.system('git checkout ' + commit)

def change_directory(path):
    os.chdir(path)

def plot(x, y, color, title, x_axis, y_axis):
    plt.style.use('ggplot')
    plt.plot(x, y, color=color)
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

    for release in logs_json:
        commit = logs_json[release]
        git_checkout(commit)

        releases.append(release)
        nbEV, complexities, nloc = retrieve_stats(nbEV, complexities, nloc)

    git_checkout('master')
    change_directory(current_path_from_project_path)

    return releases, nbEV, complexities, nloc

if __name__ == "__main__":

    # Generating tags.json
    os.system(script_tag_path + ' ' + project_path)

    releases, nbEV, complexities, nloc = count(project_env_files_path)
    print(releases, nbEV, complexities, nloc)


