'''
Manages the timing of the game.

Once two players have been added to the RpsRunner, the runner thread
starts. The runner thread sends prompts and score updates to the client.

TODO List messages and format.

'''
from app.rpsgame import Game
from time import sleep
from threading import Thread
import thread
import logging
from logging import StreamHandler

logger = logging.getLogger("Views")
logger.setLevel(logging.DEBUG)
handler = StreamHandler()
handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
handler.setFormatter(formatter)
logger.addHandler(handler)


logger.debug('RpsRunner BEGIN')


class RpsRunner(object):
    '''Handles timing and messaging between rpsgame.Game and socket clients.'''
    
    def __init__(self, msg_callback, players=[]):
        '''msg_callback is called by RpsRunner to send a dictionary of the
        game status back to the client. The runner can be initialized with
        0-2 players. The game will not start until there are 2 players.'''
        self.game = None
        self.accept_throw = False
        self.msg_callback = msg_callback
        self.players = []
        self._stop = False
        for player in players:
            self.add_player(player)


    def send_prompt(self, msg):
        '''Sends prompts to the client'''
        self.send_update({'prompt': msg})


    def send_update(self, data={}):
        '''Sends state updates to the callback provieded at init.'''
        if self._stop:
            thread.exit()
        self.msg_callback(self.players, data)


    def send_score(self, msg):
        p1 = self.game.player[self.players[0]]
        p2 = self.game.player[self.players[1]]
        status = {'scores': {
                self.players[0]:  {
                    'hand': p1.last_throw,
                    'match': p1.match_wins,
                    'bout': p1.bout_wins },
                self.players[1]: {
                    'hand': p2.last_throw,
                    'match': p2.match_wins,
                    'bout': p2.bout_wins }},
                'prompt': msg }
        logger.debug('STATUS: ' + str(status))
        self.send_update(status)


    def add_player(self, player):
        '''Game will start once two players have been added.'''
        logger.debug('In add_player(); player: {0}'.format(str(player)))
        if len(self.players) == 2:
            return None
        self.players.append(player)
        logger.debug('Appending player {0}'.format(len(self.players)))
        logger.debug('len(players): {0}'.format(len(self.players)))
        if len(self.players) == 2:
            logger.debug('Creating game')
            self.game = Game(*self.players)
            runner = Thread(target=self.run)
            logger.debug('Starting run()')
            runner.start()


    def throw(self, player_id, throw):
        '''If currently accepting throws, set the players throw.'''
        logger.debug('Player {0} throw of {1}'.format(player_id, throw))
        if self.accept_throw and not self.game.player[player_id].throw:
            self.game.player[player_id].throw = throw
            return True
        logger.debug('Not setting throw. accept_throw={0} throw={1}'.format(
                self.accept_throw, self.game.player[player_id].throw))
        return False


    def stop(self):
        '''Sets a flag for the runner thread to exit.'''
        self._stop = True


    def run(self):
        '''Run the game until there is a winner.'''
        logger.debug('In run()')
        for i in range(10, 0, -1):
            self.send_prompt('Starting Game in {0} second(s)'.format(i))
            sleep(1)
        while not self.game.winner:
            self.send_update({'bout': None})
            self.count_off()
            sleep(1)
            outcome = self.game.judge()
            self.send_score(outcome)
            sleep(3)
        self.send_update({'end_game': {'winner': self.game.winner}})


    def count_off(self):
        '''Count off 'Rock', 'Paper', 'Scissors' and accept throws.'''
        logger.debug('In count_off()')
        self.accept_throw = True
        self.send_prompt('Ready')
        sleep(1)
        for count in ['Rock','Paper','Scissors']:
            sleep(1)
            logger.debug('Count: ' + count)
            self.send_prompt(count)
        sleep(1)
        self.accept_throw = False
        self.send_prompt('Shoot!')

