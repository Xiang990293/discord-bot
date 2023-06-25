import json
import os

def get_jdata(mode = 1):
	jsource = ['setting.json','secrect.json']

	mode = {"run": 1, "debug": 0}

	with open(jsource[mode], 'r', encoding='utf8') as jfile:
		jdata = json.load(jfile)

	return jdata