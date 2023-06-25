import json
import os

def get_jdata(mode = 1):
	jsource = ['setting.json','secret.json']

	# mode = {"run": 1, "debug": 0}

	with open(jsource[mode], 'r', encoding='utf8') as jfile:
		if mode == 0:
			return json.load(jfile)
		else:
			jdatat = json.load(jfile)
			key = [i for i in jdatat]
			value = [jdatat[j] for j in key]
			return {key[i]:os.environ.get(value[i]) for i in range(len(key))}