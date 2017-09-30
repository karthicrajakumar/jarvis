'''
REMINDER PARSER

1. remind me to take the trash out in 2 hours
2. remind me to do something in 2 days
3. remind me about my meeting on thursday



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



jar_files = os.path.join(os.path.dirname(__file__), 'jars')
sutime = SUTime(jars=jar_files, mark_time_ranges=True)


def time_data_addition():
	print("Require Time data")

def date_data_addition():
	print("date data required")



def process_remainder(input_data):
	data = {}
	data_int={}
	index_message = 0
	
	
	input_data = input_data.replace("I want you to set","")
	tokens = nltk.word_tokenize(input_data)
	pos_tags  = nltk.pos_tag(tokens)
	if "to" in tokens:
		index_message = pos_tags.index(('to','TO'))
	elif "about" in tokens:
		index_message = pos_tags.index(('about','IN'))

	if index_message!= 0:
		json_raw =sutime.parse(input_data)
		
		if json_raw:
			time_data = json_raw[0]['value']
			data_json = json_raw[0]['text']
			message_data = data_json.split()
			#print(time_data[0])
			time_data_index = tokens.index(message_data[0])
			#print(nltk.pos_tag([tokens[time_data_index-1]])[0])
			#MESSAGE FETCHING ! 
			if (nltk.pos_tag([tokens[time_data_index-1]])[0][1] == "IN"):
				message = tokens[index_message+1:time_data_index-1]
			else:
				message = tokens[index_message+1:time_data_index] 
		
			reminder_message = ' '.join(message)

			# time data  => 2017-01-19 (only date) => 2017-01-19T15:30 (with time and pm/am)
			
			
			#only hours and minutes in input
			if "PT" in time_data:
				
				data_int['desc'] = "Which day ?"
				data_int['error_code'] = 1
				data_int['intent_code'] = 2
				data_int['original_input'] = input_data
				json_final ={"result" : data_int}
				json_data = json.dumps(json_final,sort_keys=True,indent=4)
				print(json_data)
				return json_data
				

			elif "T" in time_data:
				time_split = time_data.index("T")
				date = time_data[:time_split]
				time = time_data[time_split+1:]
				date = date.replace("-","/")
				data['date'] = date
				data['time'] = time
				data['desc'] = reminder_message
				data['intent_code'] = 2
				data['error_code'] = 0

				json_final ={"result": data} 
				json_data = json.dumps(json_final,sort_keys=True, indent=4)

				print(json_data)
				
				return json_data
			else:
				data_int['desc'] = "What time?"
				data_int['error_code'] = 1
				data_int['intent_code'] = 2
				data_int['original_input'] = input_data
				json_final ={"result" : data_int}
				json_data = json.dumps(json_final,sort_keys=True,indent=4)
				print(json_data)
				return json_data

		else:
			data_int['desc'] = "The date ?"
			data_int['error_code'] = 1
			data_int['intent_code'] = 2
			data_int['original_input'] = input_data
			json_final ={"result" : data_int}
			json_data = json.dumps(json_final,sort_keys=True,indent=4)
			print(json_data)
			return json_data
	else:
		data_int['desc'] = "What do you want me to remind you about?"
		data_int['error_code'] = 1
		data_int['intent_code'] = 2
		data_int['original_input'] = input_data
		json_final ={"result" : data_int}
		json_data = json.dumps(json_final,sort_keys=True,indent=4)
		print(json_data)
		return json_data

			

			


			#print(date, time)

	



'''
while(1):
	text= input()
	process_remainder(text)
'''
'''
if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument(
		'input',
		help='Input for the parser',
		)
unparsed = parser.parse_args()
process_remainder(unparsed)
'''


'''
remind me about my massage on thursday at 3:30 pm 


'''