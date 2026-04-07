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
    
class WaveMenager():
    def __init__(self,enemies) -> None:
        self.enemies = enemies
        self.direction = 1 # 1 - right, -1 - left

    def move(self): # zmienia ruch wroga samodzielnie w zależności od kierunku 
        for enemy in self.enemies:
            enemy.direction = self.direction
            enemy.direction_change()
     