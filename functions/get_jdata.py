import json
import os

def get_jdata(mode):
	jsource = ['setting.json','secret.json']

	# mode = {"debug": 0, "run": 1}

	with open(jsource[mode], 'r', encoding='utf8') as jfile:
		if mode == 0:
			return json.load(jfile)
		else:
			jdatat = json.load(jfile)
			key = [i for i in jdatat]
			value = [jdatat[j] for j in key]
			return {key[i]:os.environ.get(value[i]) for i in range(len(key))}
		
def get_jdata_with_key(key, mode):
	jsource = ['setting.json','secret.json']

	# mode = {"debug": 0, "run": 1}

	with open(jsource[mode], 'r', encoding='utf8') as jfile:
		if mode == 0:
			return json.load(jfile)
		else:
			jdatat = json.load(jfile)
			return jdatat[key]