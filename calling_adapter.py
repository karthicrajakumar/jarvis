'''
CAlling PARSER

1. jarvis can you call keshav
2. call venky
3. jarvis can you call my mom
4. jarvis call dad
5. jarvis I want to talk with my dad


'''

import nltk
import os
import json
import sys
import argparse
from sutime import SUTime
import re
import datetime

os.environ['TZ'] = 'Asia/Kolkata'



def calling_parser(input_sentence):
	data = {}

	name = ""
	#pos tagging
	input_sentence = input_sentence.replace('jarvis','')
	input_sentence = input_sentence.replace('hey','')
	tokens = nltk.word_tokenize(input_sentence)

	pos_tags = nltk.pos_tag(tokens)
	print(pos_tags)

	for tags in pos_tags:
		if tags[1] == "NN" and tags[0] != "call":
			name  = tags[0]
	if name == "":
		index = 0
		for tags in pos_tags:
			if tags[0] == "call":
				name = tokens[index+1]
			index = index + 1

	
	data['intent_code'] = 5
	data['error_code']= 0
	data['name'] = name
	data['message'] = "Calling "+name

	json_final ={"result": data} 
	json_data = json.dumps(json_final,sort_keys=True, indent=4)
	print(json_data)
	return json_data
	#print(pos_tags)



