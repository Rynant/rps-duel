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


@app.route('/play')
def play():
	return render_template("game.html",
            scripts=[
                'http:////cdnjs.cloudflare.com/ajax/libs/socket.io/0.9.16/socket.io.min.js',
                '/static/js/rps.js'])

#TODO HTTP_SEC_WEBSOCKET_KEY
@socketio.on('connect', namespace='/echo')
def echo_socket():
    emit('connected', {'data': 'Connected'})


@socketio.on('throw', namespace='/echo')
def receive_throw(message):
    emit('throw ack', {'data': 'ACK: ' + message['data']})
