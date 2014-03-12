'''
Example

game = Game('Player A', 'Player B')

while not game.winner:
    game.player['Player A'].throw = 'rock'
    game.player['Player B'].throw = 'scissors'
    game.judge()

print('{0} wins!'.format(game.winner))

'''
import logging

logger = logging.getLogger("Views")
logger.setLevel(logging.DEBUG)


THROWS = { 'Rock': 'Scissors', 'Paper': 'Rock', 'Scissors': 'Paper' }

MATCHES_TO_WIN = 3
BOUTS_TO_WIN = 2

class _Player(object):
    
    def __init__(self):
        self.match_wins = 0
        self.bout_wins = 0
        self._throw = ''
        self.last_throw = ''


    @property
    def throw(self):
        '''Gets the player's current throw.'''
        return self._throw
    
    
    @throw.setter
    def throw(self, move):
        '''If the throw is not a valid throw (is a key of THROWS), the player's
        throw is set to an empty string.
        '''
        logger.debug('Setting throw of {0}'.format(move))
        move = move.title()
        if THROWS.has_key(move) or move == '':
            self._throw = move
    
    def __repr__(self):
        text = "{{match_wins: {0}, bout_wins: {1}, throw: '{2}'}}"
        return text.format(self.match_wins, self.bout_wins, self.throw)



class Game(object):
    
    def __init__(self, player1, player2):
        '''Initialize game.'''
        self.player = {}
        self.player[player1] = _Player()
        self.player[player2] = _Player()
        self._winner = None
        self._loser = None
    
    
    @property
    def winner(self):
        return self._winner
    
    
    @property
    def loser(self):
        return self._loser
    
    
    def _add_point(self, player_key):
        '''Add a point to the player's score. Return False if the player does
        not have enough points to win. Return True if the player wins.
        '''
        if self.winner:
            msg = '{0} has already won.'.format(self.winner)
            raise RuntimeError(msg)
        
        self.player[player_key].bout_wins += 1
        if self.player[player_key].bout_wins == BOUTS_TO_WIN:
            for each in self.player:
                self.player[each].bout_wins = 0
            self.player[player_key].match_wins += 1
            if self.player[player_key].match_wins == MATCHES_TO_WIN:
                return True
        return False
        
    
    
    def judge(self):
        '''Compare the players' throws and determine the winner of the throw.
        If a player wins the game, return the player's key, else, return None.
        '''
        if self._winner:
            return self.winner
        
        (pid1, p1), (pid2, p2) = self.player.items()

        scorer = ''
        result = ''
        
        if p1.throw != p2.throw:
            if not p1.throw:
                scorer = pid2
            elif not p2.throw:
                scorer = pid1
            elif THROWS.get(p1.throw) == p2.throw:
                scorer = pid1
            else:
                scorer = pid2
                
        p1.last_throw = p1.throw if p1.throw else 'No-Throw'
        p2.last_throw = p2.throw if p2.throw else 'No-Throw'
        p1.throw = p2.throw = ''
        
        if scorer:
            loser = pid1 if scorer == pid2 else pid2
            msg = "{0} beats {1}".format(self.player[scorer].last_throw,
                                         self.player[loser].last_throw)
            win = self._add_point(scorer)
            if win:
                self._winner = scorer
                self._loser = loser
            return msg
        else:
            return 'Draw'
                
        
        
