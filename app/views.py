# -*- coding: utf-8 -*-
from flask import render_template
from app import app
from app import socketio, emit

clients = []
msg_count = 0

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")

print('#####SCRIPT')

@app.route('/play')
def play():
	return render_template("game.html")

#TODO HTTP_SEC_WEBSOCKET_KEY
@socketio.on('connect', namespace='/echo')
def echo_socket():
    print('******CONNECT')
    emit('connected', {'data': 'Connected'})


@socketio.on('throw', namespace='/echo')
def receive_throw(message):
    print('******THROW')
    print(message)
    emit('throw ack', {'data': 'ACK: ' + message['data']})
