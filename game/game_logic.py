from game.entities import Player
# state: 0 - game_over, 1 - menu, 2 - started
class GameState():
    def __init__(self,state,player) -> None:
        self.state = state
        self.player = player
    def game_start(self):
        self.state = 2

    def game_over(self):
        if not self.player.is_alive():
            self.state = 0 

    def game_restart(self):
        if self.state == 0:
            self.state = 2
    