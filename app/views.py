# -*- coding: utf-8 -*-
from flask import render_template, session, request
from app import app, socketio, emit
from uuid import uuid4
import logging
from logging import StreamHandler

logger = logging.getLogger("Views")
logger.setLevel(logging.DEBUG)
handler = StreamHandler()
handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
handler.setFormatter(formatter)
logger.addHandler(handler)


logger.debug('START')

players = []
msg_count = 0


def get_this_socket():
    for sessid, socket in request.namespace.socket.server.sockets.items():
        if socket['/play'].session.get('id', None) == session['id']:
            return socket

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


@app.route('/rules')
def rules():
    return render_template('rules.html')


@socketio.on('connect', namespace='/play')
def play_connect():
    global players
    session['id'] = str(uuid4())
    print('ID: ' + session['id'])
    emit('connected', {'data': 'Connected'})

@socketio.on('connect_ack', namespace='/play')
def play_connect_ack(message):
    players.append(get_this_socket())
    logger.debug('play_connect_ack PLAYERS: \n\t' + 
            '\n\t'.join(str(p) for p in players))

   

@socketio.on('disconnect', namespace='/play')
def play_disconnect():
    global players
    players.remove(get_this_socket())
    logger.debug('play_disconnect PLAYERS: \n\t' + 
            '\n\t'.join(str(p) for p in players))

   


@socketio.on('throw', namespace='/play')
def receive_throw(message):
    emit('throw ack', {'data': 'ACK: ' + message['data']})
