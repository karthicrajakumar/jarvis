
import socketio
import eventlet
import eventlet.wsgi
from gevent import pywsgi

from alarm_nlp_tagger import process_alarm_input
from reminder_nlp_tagger import process_remainder

sio = socketio.Server(async_mode='gevent')



@sio.on('connect')
def connect(sid, environ):
    print("connected ", sid)

@sio.on('chat')
def message(sid, data):
	output = process_remainder(data)
	sio.emit('reply',data=output)

@sio.on('disconnect')
def disconnect(sid):
	print('disconnect ', sid)

if __name__ == '__main__':
    # wrap Flask application with engineio's middleware
    app = socketio.Middleware(sio)

    # deploy as an eventlet WSGI server
    pywsgi.WSGIServer(('0.0.0.0', 9000), app).serve_forever()