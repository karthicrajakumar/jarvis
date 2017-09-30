'''
Scenarios

1. wake me up at 6 Jarvis
2. wake me up at 4 AM Jarvis
3. wake me up in half an hour
4. wake me up at 5 PM
5. wake me up at 5 
6. wake me up in 4 hours from now


Need to convert Half an Hour = 30 mins n feed

#ALL INPUTS CONVERTED TO FORMAT
#NEED TO CHECK THE OUTPUT

prepare tag for minutes (i.e 30 minutes from now , 5 minutes from now => Convert from PT2H(2 hours) 02:00)
wake me up at 5 => hours must be appended at the end of the number. Logic => if no PM/AM or hours from now then simply append hours at the end

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


def json_form_response():
	return null



def process_alarm_input(input_data):
	data = {}
	data_int = {}
	

	flag = 0
	input_data = input_data.lower()
	input_data = input_data.replace("p.m","pm") #String manip => remove dot
	input_data = input_data.replace("a.m","am") #String manip => remove dot
	input_data = input_data.replace(":"," ") #String manip => remove colon
	
	check_string = "half an hour"
	if check_string in input_data:
		input_data = input_data.replace('half an hour','30 minutes') #String manip => convert half an hour to 30 mins
	
	check_string = "from now"
	if check_string in input_data:
		input_data = input_data.replace(check_string,"") #String manip => remove from now in string



	
	tokens = nltk.word_tokenize(input_data)
	validity = []


	# For every token if digit perform various string operations
	for t in tokens:
		if t.isdigit():
			token_index = tokens.index(t)
			token_index = token_index+1
			if(token_index != len(tokens)):
				nows = datetime.datetime.now()
				now_hour = nows.hour


				if (now_hour>12 and (input_data.find("pm") == -1)): #if no PM in input data append pm to string getting from current time
					tokens.append("pm")
				elif(now_hour<12 and (input_data.find("am")== -1)): #if no AM in input data append pm to string getting from current time
					tokens.append("am")
				
				
				#Check if next is a minutes digit and followed by pm. Eg: "4 30 pm" or "5 30 am". append if dosent exist
				if(tokens[token_index].isdigit() and (tokens[token_index+1] == "am" or tokens[token_index+1] == "pm" or tokens[token_index+1] == "a.m" or tokens[token_index+1] == "p.m") ):
					

					if(tokens[token_index+1] == "am" or tokens[token_index+1] == "a.m"):
						input_data = input_data.replace("a.m","")
						input_data = input_data.replace("am","")
						index_temp = input_data.find(str(t))
						index_temp = index_temp + len(str(t))
						input_data = input_data[:index_temp]+ ' am' +input_data[index_temp:]
						input_temp = input_data.find(tokens[token_index+1])
						input_temp  = input_temp + len(str(tokens[token_index+1])) + len("am") + 1
						input_data = input_data[:input_temp] + ' minutes' + input_data[input_temp:]
					else:
						input_data = input_data.replace("p.m","")
						input_data = input_data.replace("pm","")
						index_temp = input_data.find(str(t))
						index_temp = index_temp + len(str(t))
						input_data = input_data[:index_temp]+ ' pm' +input_data[index_temp:]
						input_temp = input_data.find(tokens[token_index+1])
						input_temp  = input_temp + len(str(tokens[token_index+1])) + len("pm") + 1
						input_data = input_data[:input_temp] + ' minutes' + input_data[input_temp:]
					


				#continue loop if pm already exists
				elif(tokens[token_index]== 'pm' or tokens[token_index] == 'am' or tokens[token_index] == 'a.m' or tokens[token_index] == 'p.m' or tokens[token_index] == 'hours' or tokens[token_index] == 'minutes' or tokens[token_index] == 'hour'):
					continue
			t = int(t)
			#convert 5  => 5 am and 16 => 4 pm 
			if(token_index != len(tokens)):
				temp_token = tokens[token_index]
			
			if t<12:
				index_temp = input_data.find(str(t))
				index_temp = index_temp + len(str(t))
				input_data = input_data[:index_temp]+ ' am' +input_data[index_temp:]
				
			else:
				temp = t-12
				string = str(temp) + " pm"
				input_data = input_data.replace(str(t),string)
			
		

	#Process input data via SUTIME parser
	

		json_raw = sutime.parse(input_data)
	if json_raw:
		
		temp_string  = json_raw[0]['value']

		minute_string = "minutes"
		hours_string = "hours"
		hour_string = "hour"
		am_string = "am"
		pm_string = "pm"

		# HOURS AND MINUTES
		if minute_string in input_data and (hours_string in input_data or hour_string in input_data):
			temp_string_1=  json_raw[1]['value']
			index_hour = temp_string.find('PT')
			index_min = temp_string_1.find('PT')
			if index_hour != -1 and index_min != -1:
				index_hour = index_hour +1
				index_min = index_min +1 
				temp_string = temp_string[index_hour+1:]
				temp_string_1 = temp_string_1[index_min+1:]
				temp_string_1 = temp_string_1.replace('M',"")
				temp_string = temp_string.replace('H',"")
				now = datetime.datetime.now()
				now_plus_10 = datetime.timedelta(hours = int(temp_string), minutes = int(temp_string_1)) + now
				now_plus_10 = str(now_plus_10.time())

				


				data['hours'] = now_plus_10[:2]
				data['minutes'] = now_plus_10[3:5]
				data['minutes_only'] = "0"

		# AM/PM AND MINUTES
		elif (am_string in input_data or pm_string in input_data) and minute_string in input_data:
			index = temp_string.find('T')
			temp_string = temp_string[index+1:]
			index = temp_string.find(':')
			
			data['hours'] = temp_string[:index]
			temp_string_1=  json_raw[1]['value']
			index_min = temp_string_1.find('PT')
			temp_string_1 = temp_string_1[index_min+2:]
			temp_string_1 = temp_string_1.replace('M',"")
			data['minutes'] = temp_string_1
			data['minutes_only'] = "0"


		# MINUTES
		elif minute_string in input_data:
			index = temp_string.find('PT')
			
			if index != -1:
				index = index +1
				temp_string = temp_string[index+1:]
				temp_string = temp_string.replace('M',"")
				now = datetime.datetime.now()
				now_plus_10 = now + datetime.timedelta(minutes = int(temp_string))
				now_plus_10 = str(now_plus_10.time())
				data['hours'] = now_plus_10[:2]
				data['minutes'] = now_plus_10[3:5]
				data['minutes_only'] = "1"
 
		#HOURS
		elif hours_string in input_data or hour_string in input_data:


			current_time = str(datetime.datetime.now().time())
			current_time =current_time[:2]
			index = temp_string.find('PT')
			if index != -1:
				index = index +1 
				temp_string =temp_string[index+1:]
				temp_string = temp_string.replace('H',"")
				now = datetime.datetime.now()
				now_plus_10 = datetime.timedelta(hours = int(temp_string)) + now
				now_plus_10 = str(now_plus_10.time())
				data['hours'] = now_plus_10[:2]
				data['minutes'] = now_plus_10[3:5]
				data['minutes_only'] = "0"



		#AM and PM only
		else:
			index = temp_string.find('T')
			temp_string = temp_string[index+1:]
			index = temp_string.find(':')
			
			data['hours'] = temp_string[:index]
			data['minutes']= temp_string[index+1:]
			data['minutes_only'] = "0"
			
			
		data['message'] = "Setting Alarm"
		data['trigger_sentence'] = json_raw[0]['text']
		data['intent'] = "alarm.set"
		data['intent_code'] = 1
		data['error_code'] = 0 

		json_final ={"result": data} 
		json_data = json.dumps(json_final,sort_keys=True, indent=4)
		
		print(json_data)
		return json_data
	else:
		data_int['desc'] = "What time do you want the Alarm?"
		data_int['error_code'] = 1
		data_int['intent_code'] = 1
		data_int['original_input'] = input_data
		json_final ={"result" : data_int}
		json_data = json.dumps(json_final,sort_keys=True,indent=4)
		print(json_data)
		return json_data


'''
if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument(
		'input',
		help='Input for the parser',
		)
unparsed = parser.parse_args()

while(1):
	s = input()
	process_alarm_input(s)
'''
'''
OUTPUT Notes:
	wake me up at 5 pm => correct after variable 'T'
	30 minutes - PT30M
	2 hours - PT3H



'''