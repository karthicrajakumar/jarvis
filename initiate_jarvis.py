import MySQLdb
import socketio
import eventlet
import eventlet.wsgi
from gevent import pywsgi
from alarm_nlp_tagger import process_alarm_input
from reminder_nlp_tagger import process_remainder
from rnn_text_classifier import main
from youtube_adapter import youtube_tagger
from calling_adapter import calling_parser
import json



''' 
DB Connection and Object Cursor  
'''
db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                     user="root",         # your username
                     passwd="delta2345",  # your password
                     db="jarvis")        # name of the data bases


cur = db.cursor()



sio = socketio.Server(async_mode='gevent')


@sio.on('connect')
def connect(sid, environ):
    print("connected ", sid)


@sio.on('chat')
def message(sid, data):
	int_data = {}
	intent_code = main("test",data)
	if intent_code == 1:
		int_data['message'] = "Hey There! How can I help you ?"
		int_data['trigger_sentence'] = data
		int_data['intent'] = "greeting_command"
		int_data['intent_code'] = 3
		json_final ={"result" : int_data}
		json_data = json.dumps(json_final,sort_keys=True,indent=4)
		sio.emit('reply',data=json_data)
	elif intent_code == 2:
		output = youtube_tagger(data)
		sio.emit('reply',data=output)
	elif intent_code == 4:
		output = process_remainder(data)
		sio.emit('reply',data=output)
	elif intent_code == 3:
		output = process_alarm_input(data)
		sio.emit('reply',data=output)
	elif intent_code == 5:
		output = calling_parser(data)
		sio.emit('reply',data=output)


@sio.on('disconnect')
def disconnect(sid):
	print('disconnect ', sid)

if __name__ == '__main__':
    # wrap Flask application with engineio's middleware
    app = socketio.Middleware(sio)

    # deploy as an eventlet WSGI server
    pywsgi.WSGIServer(('0.0.0.0', 9000), app).serve_forever()