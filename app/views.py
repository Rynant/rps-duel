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
        gid, open_game = next([gid, game] for gid, game in 
                games.iteritems() if len(game.players) < 2)
        if open_game:
            open_game.add_player(session['id'])
            players[session['id']]['game'] = gid
            logger.debug('Joined Game, GAMES: \n\t' + 
                    '\n\t'.join(str(x) for x in games))
            return
    except StopIteration:
        pass
    new_game = RpsRunner(update_client, [session['id']])
    game_id = str(uuid4())
    games[game_id] = new_game
    players[session['id']]['game'] = game_id
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
    global players, games
    sid = session['id']
    players.pop(sid)
    logger.debug('play_disconnect PLAYERS: \n\t' + 
            '\n\t'.join(str(p) for p in players))
    for gid, game in games.iteritems():
        if sid in game.players:
            player = [x for x in game.players if x != sid][0]
            logger.debug('Sending disconnect message to {0}'.format(player))
            players[player]['socket'].base_emit('prompt',
                    'Player disconnected. You Win!')
            games.pop(gid)



@socketio.on('throw', namespace='/play')
def receive_throw(message):
    sid = session['id']
    sock = players[sid]['socket']
    game = games[players[sid]['game']]
    logger.debug('Setting throw: {0}'.format(message))
    is_set = game.throw(sid, message)
    if is_set:
        logger.debug('Throw of {0} was set.'.format(message))
        sock.base_emit('throw_ack', message)


def update_client(player_ids, message):
    '''Callback for RpsRunner; forwards messages to the client.'''
    global players
    logger.debug('In update_client()')
    for player in player_ids:
        try:
            sock = players[player]['socket']
        except KeyError as e:
            logger.debug('Player {0} does not exist.'.format(e))
            continue
        for event, data in message.iteritems():
            logger.debug('Player: {0} Event: {1} Message: {2}'.format(
                player, event, data))
            sock.base_emit(event, data)

