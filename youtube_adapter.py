'''   
YOUTUBE ADAPTER


1. Open Youtube and play a song for me
2. I want to listen to some music
3. play the song wake me up when september ends


Find each words determinatans and feed it into the search query api
'''
import requests
import json
import nltk
from nltk.corpus import stopwords


#Youtube API adapter
def youtube_api_caller(query):

	q = query
	API_KEY = "AIzaSyDLHeLXwRghj8AoWZEXMOyRtH-C3wkU5cw"



	url = 'https://www.googleapis.com/youtube/v3/search?maxResults=1&key='+API_KEY+'&q='+q+'&part=id%2Csnippet&alt=json'
	r = requests.get(url=url)
	data = r.json()
	
	if data['items'][0]['id']['kind'] == 'youtube#video':
		return data['items'],0,0
	else:
		url = "https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId="+data['items'][0]['id']['playlistId']+"&key="+API_KEY
		playlist  = requests.get(url=url)
		playlist_items = playlist.json()


		return data['items'],1,playlist_items['items'][0]['snippet']['resourceId']


def youtube_tagger(input_sentence):
	data = {}

	#remove extra words
	input_sentence = input_sentence.replace("open","")
	input_sentence = input_sentence.replace("youtube","")
	

	#generate tokens
	tokens = nltk.word_tokenize(input_sentence)
	pos_tags = nltk.pos_tag(tokens)
	index_det = 0

	
	
	for item in pos_tags:
		if item[1] == 'DT':
			det_item = item 
			break

	index_det = pos_tags.index(det_item)
	max_len = len(tokens)
	predicted_message = ""
	predicted_output = tokens[index_det:max_len]
	for item in predicted_output:
		predicted_message += item + " "
	

	#call youtube function

	output_json,type_of_video,firstVideo_id = youtube_api_caller(predicted_message)

	if type_of_video == 0:
		message = "Opening YouTube to play "+output_json[0]['snippet']['title']
		data['video_id'] = output_json[0]['id']['videoId']
		data['message'] = message
		data['type'] = "video"
		data['intent_code'] = 4
		data['error_code']= 0
		json_final ={"result": data} 
		json_data = json.dumps(json_final,sort_keys=True, indent=4)
		print(json_data)
		return json_data
	else:
		message = "Opening YouTube to play the list "+output_json[0]['snippet']['title']
		data['video_id'] = output_json[0]['id']['playlistId']
		data['message'] = message
		data['firstVideo_id'] = firstVideo_id['videoId']
		data['type'] = "playlist"
		data['intent_code'] = 4
		data['error_code']= 0
		json_final ={"result": data} 
		json_data = json.dumps(json_final,sort_keys=True, indent=4)
		print(json_data)
		return json_data




	


'''
while(1):
	i = input("command:")
	main(i)
#youtube_api_caller("adele songs")
'''