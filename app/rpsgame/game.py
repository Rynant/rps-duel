'''
Example

game = Game('Player A', 'Player B')

while not game.winner:
    game.player['Player A'].throw = 'rock'
    game.player['Player B'].throw = 'scissors'
    game.judge()

print('{0} wins!'.format(game.winner))

'''

THROWS = { 'Rock': 'Scissors', 'Paper': 'Rock', 'Scissors': 'Paper' }

MATCHES_TO_WIN = 2
BOUTS_TO_WIN = 2

class _Player(object):
    
    def __init__(self):
        self.match_wins = 0
        self.bout_wins = 0
        self._throw = ''


    @property
    def throw(self):
        '''Gets the player's current throw.'''
        return self._throw
    
    
    @throw.setter
    def throw(self, move):
        '''If the throw is not a valid throw (is a key of THROWS), the player's
        throw is set to an empty string.
        '''
        self._throw =  THROWS.get(move.title(), '')
    
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
            self.player[player_key].bout_wins = 0
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
        
        p1, p2 = self.player.keys()
        scorer = ''
        
        if self.player[p1].throw != self.player[p2].throw:
            if not self.player[p1].throw:
                scorer = p2
            elif not self.player[p2].throw:
                scorer = p1
            elif THROWS.get(self.player[p1].throw) == self.player[p2].throw:
                scorer = p1
            else:
                scorer = p2
                
        self.player[p1].throw = self.player[p2].throw = ''
        
        if scorer:
            win = self._add_point(scorer)
            if win:
                self._winner = scorer
                self._loser = p1 if scorer == p2 else p2
        
        return self.winner
                
        
        
