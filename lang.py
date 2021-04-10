from os import listdir
from os.path import isdir
from json_handler import load as json_load

__PATH = "lang/"

def __load_dir(dirname):
	return { item: __load_dir(dirname + item + "/") if isdir(dirname + item) else __load_file(dirname, item) for item in listdir(dirname) }

def __load_file(dirname, filename):
	return json_load(dirname + filename)

langs = { subdir: __load_dir(__PATH + subdir + "/") for subdir in listdir(__PATH) }
