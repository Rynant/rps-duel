from app.rpsgame import Game

class RpsRunner:
    '''Handles timing and messaging between rpsgame.Game and socket clients.'''
    
    def __init__(self):
        self.game = None
        self.players = []

    def add_player(self, player):
        if len(self.players) == 2:
            return False
        self.players.append(player)
        if len(self.players) == 2:
            self.game = Game(*self.players)
            pass #TODO Start runner
        return True


