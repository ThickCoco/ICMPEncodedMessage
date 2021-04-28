#!/usr/bin/python

import json

with open('tout.json') as f:
	data = json.load(f)

outData = ""

for x in range(0,len(data)):
	msg = json.dumps(data[x]['_source']['layers']['data'])	
	msg = msg[18:-2]
	outData += msg

print(outData)

