# -*- coding: utf-8 -*-
from flask import render_template, session, request
from app import app, socketio, emit
from uuid import uuid4
from collections import OrderedDict
import logging
from logging import StreamHandler
from runner import RpsRunner

logger = logging.getLogger("Views")
logger.setLevel(logging.DEBUG)



logger.debug('START')

players = {}
games = OrderedDict()
msg_count = 0


def get_this_socket():
    for sessid, socket in request.namespace.socket.server.sockets.items():
        if socket['/play'].session.get('id', None) == session['id']:
            return socket['/play']


def add_player(player_id):
    try:
        open_game = next(game for gid, game in games.iteritems() if len(game.players) < 2)
        if open_game:
            open_game.add_player(session['id'])
            logger.debug('Joined Game, GAMES: \n\t' + 
                    '\n\t'.join(str(x) for x in games))
            return
    except StopIteration:
        pass
    new_game = RpsRunner(update_client, [session['id']])
    games[str(uuid4())] = new_game
    logger.debug('Added Game, GAMES: \n\t' + 
            '\n\t'.join(str(x) for x in games))
    

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
    logger.debug('Connected ID: ' + session['id'])
    emit('connected', {'id': session['id']})


@socketio.on('connect_ack', namespace='/play')
def play_connect_ack(message):
    players[session['id']] = {'socket': get_this_socket()}
    logger.debug('play_connect_ack PLAYERS: \n\t' + 
            '\n\t'.join(str(p) for p in players))
    add_player(session['id'])


@socketio.on('disconnect', namespace='/play')
def play_disconnect():
    global players
    players.pop(session['id'])
    logger.debug('play_disconnect PLAYERS: \n\t' + 
            '\n\t'.join(str(p) for p in players))


@socketio.on('throw', namespace='/play')
def receive_throw(message):
    #emit('throw ack', {'data': 'ACK: ' + message['data']})
    sock = players[session['id']]['socket']
    sock.base_emit('throw ack', {'data': 'ACK: ' + message['data']})


def update_client(message):
    '''Callback for RpsRunner; forwards messages to the client.'''
    global players
    logger.debug('In update_client()')
    logger.debug('Message: {0}'.format(message))
    for player in message['players']:
        sock = players[player]['socket']
        status = {'msg': message['msg']}
        sock.base_emit('status', status)

