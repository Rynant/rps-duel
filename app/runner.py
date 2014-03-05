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
    
    def __init__(self, msgr, players=[]):
        self.game = None
        self.msgr = msgr
        self._prompt = None
        self.players = []
        for player in players:
            self.add_player(player)


    @property
    def prompt(self):
        return self._prompt


    @prompt.setter
    def prompt(self, msg):
        logger.debug('Setting prompt: ' + msg)
        self._prompt = msg
        self.send_update()


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

    def run(self):
        logger.debug('In run')
        self.prompt = 'Ready'
        sleep(2)
        for count in ['Rock','Paper','Scissors']:
            logger.debug('Count: ' + count)
            self.prompt = count
            sleep(1)
        self.prompt = 'Shoot!'

    def send_update(self):
        p1 = self.game.player[self.players[0]]
        p2 = self.game.player[self.players[1]]
        status = {
                'players': self.players,
                self.players[0]:  {
                    'hand': p1.throw,
                    'match': p1.match_wins,
                    'bout': p1.bout_wins },
                self.players[1]: {
                    'hand': p2.throw,
                    'match': p2.match_wins,
                    'bout': p2.bout_wins },
                'msg': self.prompt }
        logger.debug('STATUS: ' + str(status))
        self.msgr(status)



