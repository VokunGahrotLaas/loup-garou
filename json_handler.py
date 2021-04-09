import json as _json

def load(filename):
	with open(filename, mode= "r", encoding= "utf-8") as file:
		return _json.load(file)

def dump(filename, obj):
	with open(filename, mode= "w", encoding= "utf-8") as file:
		_json.dump(file, obj)
