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


class RpsRunner:
    '''Handles timing and messaging between rpsgame.Game and socket clients.'''
    
    def __init__(self, msgr, players=[]):
        self.game = None
        self.msgr = msgr
        self.players = []
        for player in players:
            self.add_player(player)


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
        self.msgr('Ready')
        sleep(2)
        for count in ['Rock','Paper','Scissors']:
            self.msgr(count)
            sleep(1)
        self.msgr('Shoot!')

