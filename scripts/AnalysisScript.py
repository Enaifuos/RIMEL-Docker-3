# Code Analysis module via Lizard code analyzer
# provides functions to analyze a list of files
# the analyze funciton returns a json string to be injected into a web-ui

import json
import lizard
from lizard_ext.lizardduplicate import LizardExtension as DuplicateDetector
from lizard_ext.lizardcpre import LizardExtension as lizardcpre
from lizard_ext.lizardnd import LizardExtension as lizardnd
from lizard_ext.lizardio import LizardExtension as lizardio
from lizard_ext.lizardns import LizardExtension as lizardns
import glob
import sys
import os
import pathlib
from distutils.dir_util import copy_tree

# GLOBALS
LIZARD_SUPPORTED_LANGUAGES = ["c", "cpp", "cc", "mm", "cxx", "h", "hpp", "cs", "gd",
                              "go", "java", "js", "lua", "m", "php", "py", "rb",
                              "scala", "swift", "tnsdl", "sdl", "ttcn", "ttcnpp"]
# How many tokens such as: "if", "(", "abc", "%", "4", ")" must be repeated to appear in duplicate detection list
MIN_DUP_TOKENS = 70


# analyzes all files, with lizard, provided in list and returns a json string of the raw data
def analyze(path, filenameList):
    lizOut = runLizard(filenameList)
    asDict = filesInfoToDict(path, lizOut)

    # for more readable json output:
    data = json.dumps(asDict, indent=4, sort_keys=False)
    # for compressed json:
    # data = json.dumps(asDict, sort_keys=False)
    return data


# Runs lizard on each individual file designated in the given filenameList.
def runLizard(filenameList):
    duplicates = DuplicateDetector()
    cpre = lizardcpre()
    nd = lizardnd()
    ns = lizardns()
    io = lizardio()
    extensions = lizard.get_extensions([duplicates, cpre, ns, nd, io])
    outList = list(lizard.analyze_files(filenameList, exts=extensions))
    dupCodeSnips = list(duplicates.get_duplicates(min_duplicate_tokens=MIN_DUP_TOKENS))
    dupInfo = {'duplicates': [dupInfoToDict(d) for d in dupCodeSnips],
               'duplicateRate': duplicates.saved_duplicate_rate,
               'uniqueRate': duplicates.saved_unique_rate}
    return {'fileList': outList,
            'dupInfo': dupInfo}


# converts a list of FileInformation objects into a list of dictionaries
def filesInfoToDict(path, info):
    filesAsDicts = [fileInfoToDict(f) for f in info['fileList']]

    return {'path': path,
            'duplicateInfo': info['dupInfo'],
            'files': filesAsDicts}


# converts FileInformation object into a dictionary
def fileInfoToDict(fileInfo):
    filename = fileInfo.filename
    funcs = []
    for func in fileInfo.function_list:
        funcs.append(funcInfoToDict(func))

    return {'filename': filename,
            'filetype': filename.split('.')[1],
            'functions': funcs}


# converts FunctionInformation object into dictionary
def funcInfoToDict(funcInfo):
    return {'name': funcInfo.name,
            'longName': funcInfo.long_name,
            'startLine': funcInfo.start_line,
            'nloc': funcInfo.nloc,
            'ccn': funcInfo.cyclomatic_complexity,
            'tokens': funcInfo.token_count,
            'params': len(funcInfo.parameters),
            'length': funcInfo.length,
            'fanIn': funcInfo.fan_in,
            'fanOut': funcInfo.fan_out,
            'generalFanOut': funcInfo.general_fan_out,
            'maxNestingDepth': funcInfo.max_nesting_depth,
            'maxNestedStructures': funcInfo.max_nested_structures}


# converts duplicate CodeSnippet objects to dicts of info
def dupInfoToDict(snippets):
    return [{'filename': c.file_name,
             'startLine': c.start_line,
             'endLine': c.end_line} for c in snippets]


# ################################################################################################################
# GLOBALS
# DATA_REPLACE_TOKEN = "<script id=\"rawData\" type=\"application/json\">"

# runs it all. This is called down below.
def runAnalysis(dir):
    path = checkPathExists(dir)
    filenameList = buildFilenameList(path)
    jsonData = analyze(path, filenameList)
    formattedJson = json.loads(jsonData)
    return(formattedJson)

# returns the input string if no errors, signals error and quits else
def checkPathExists(dir):
    dir = str(dir)
    path = os.path.abspath(dir)
    if(os.path.exists(path) is not True):
        print("error: Path \'", path, "\' does not exist.")
        sys.exit()
    if (os.path.isdir(path)):
        path += '/'
    return path

# for packaged data files in the stand alone executable
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# goes through given path and identifies all files within that are supported by lizard, then puts those files in a list
def buildFilenameList(path):
    files = []
    if(os.path.isfile(path)):
        if getExtensionFromFilename(path) in LIZARD_SUPPORTED_LANGUAGES:
            files.append(path)
            return files
    for ext in LIZARD_SUPPORTED_LANGUAGES:
        addUs = [f for f in glob.glob(path + "/**/*." + ext, recursive=True)]
        files.extend(addUs)
    return files

# returns just the extension from a file name
def getExtensionFromFilename(path):
    ext = pathlib.Path(path).suffix
    ext = ext[1:] # strip off the '.'
    return ext
