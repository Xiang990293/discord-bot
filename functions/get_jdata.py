import json
import os

def get_jdata(mode = 1):
	jsource = ['setting.json','secret.json']

	# mode = {"run": 1, "debug": 0}

	with open(jsource[mode], 'r', encoding='utf8') as jfile:
		if mode == 0:
			return json.load(jfile)
		else:
			key = [i for i in jfile]
			value = [jfile for j in key]
			return {key[i]:str(os.environ.get(value[i])) for i in range(len(key))}