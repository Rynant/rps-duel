import pytest
from app.rpsgame.game import Game, MATCHES_TO_WIN, BOUTS_TO_WIN

class TestThrows:
    @pytest.fixture(autouse=True)
    def game_instance(self):
        self.game = Game('a', 'b')
        self.player_a = self.game.player['a']
        self.player_b = self.game.player['b']
    
    def is_draw(self):
        g = self.game
        g.judge()
        bout = g.player['a'].bout_wins == g.player['b'].bout_wins == 0
        match = g.player['a'].match_wins == g.player['b'].match_wins == 0
        return bout and match
    
    def player_scores(self, p1, p2):
        g = self.game
        g.judge()
        p1_bout = g.player[p1].bout_wins == 1
        p2_bout = g.player[p2].bout_wins == 0
        match = g.player[p1].match_wins == g.player[p2].match_wins == 0
        return p1_bout and p2_bout and match
    
    def test_none_ties_none(self):
        #self.game = Game('a', 'b')
        self.game.judge()
        assert self.is_draw()
    
    def test_paper_ties_paper(self):
        self.player_a.throw = 'Paper'
        self.player_b.throw = 'Paper'
        assert self.is_draw()
    
    def test_invalid_ties_invalid(self):
        self.player_a.throw = 'bad'
        self.player_b.throw = 'nope'
        assert self.is_draw()
        
    throws = [
        ('Rock', 'Scissors'),
        ('Paper', 'Rock'),
        ('Scissors', 'Paper'),
        ('Scissors', 'bad'),
        ('Scissors', ''),
        pytest.mark.xfail(('Rock', 'Paper')),
        pytest.mark.xfail(('Scissors', 'Rock')),
        pytest.mark.xfail(('Paper', 'Scissors')),
        pytest.mark.xfail(('bad', 'Scissors')),
        pytest.mark.xfail(('', 'Rock')),
    ]
    
    @pytest.mark.parametrize("a_throw,b_throw", throws )
    def test_a_scores(self, a_throw, b_throw):
        self.player_a.throw = a_throw
        self.player_b.throw = b_throw
        assert self.player_scores('a', 'b')
    
    @pytest.mark.parametrize("b_throw,a_throw", throws )
    def test_b_scores(self, b_throw, a_throw):
        self.player_a.throw = a_throw
        self.player_b.throw = b_throw
        assert self.player_scores('b', 'a')

        

class TestScore:
    @pytest.fixture(autouse=True)
    def game_instance(self):
        self.game = Game('a', 'b')
        self.player_a = self.game.player['a']
        self.player_b = self.game.player['b']
        self.player_a.bout_wins = BOUTS_TO_WIN - 1
        
    def test_match_win_increases(self):
        a = self.player_a
        a.throw = 'Rock'
        self.game.judge()
        assert a.match_wins == 1
        assert a.bout_wins == 0
        
    def test_winner_is_set(self):
        a, b = self.player_a, self.player_b
        a.throw = 'Rock'
        b.throw = 'Scissors'
        a.match_wins =  MATCHES_TO_WIN - 1
        self.game.judge()
        assert a.match_wins == 2
        assert a.bout_wins == 0
        assert self.game.winner == 'a'