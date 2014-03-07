from app.rpsgame import Game
from time import sleep
from threading import Thread
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
        for player in players:
            self.add_player(player)

    def send_prompt(self, msg):
        '''Sends prompts to the client'''
        logger.debug('Setting prompt: ' + msg)
        self.send_update({'prompt': {'msg': msg}})


    def send_update(self, data={}):
        '''Send state updates to the callback provieded at init.'''
        msg = {'players': self.players}
        msg.update({'update': data})
        self.msg_callback(msg)


    def send_score(self):
        p1 = self.game.player[self.players[0]]
        p2 = self.game.player[self.players[1]]
        status = {'scores': {
                self.players[0]:  {
                    'hand': p1.throw,
                    'match': p1.match_wins,
                    'bout': p1.bout_wins },
                self.players[1]: {
                    'hand': p2.throw,
                    'match': p2.match_wins,
                    'bout': p2.bout_wins }}}
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
        if self.accept_throw:
            self.game.player[player_id].throw = throw
            return True
        return False


    def run(self):
        '''Run the game until there is a winner.'''
        logger.debug('In run()')
        while not self.game.winner:
            self.count_off()
            self.game.judge()
            self.send_score()
            sleep(3)
        self.send_prompt('Winner is {0}'.format(self.game.winner))


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
        self.accept_throw = False
        sleep(1)
        self.send_prompt('Shoot!')

