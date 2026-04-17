 # state: 0 - game_over, 1 - menu, 2 - started
import os 
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
        self.down = 0 # 1 - down, 0 - nie idziemy w dół

    def move(self): # zmienia ruch wroga samodzielnie w zależności od kierunku 
        right_edge = any(enemy.x + enemy.speed > enemy.screen_width for enemy in self.enemies)
        left_edge = any(enemy.x - enemy.speed < 0 for enemy in self.enemies)

        if right_edge or left_edge:
            self.direction *= -1
            for enemy in self.enemies:
                enemy.move_down()

            for enemy in self.enemies:
                enemy.direction = self.direction
                enemy.direction_change()

        for enemy in self.enemies:
            enemy.direction = self.direction
            enemy.direction_change()

class ScoreManager():
    
    def __init__(self,filename,player,current_score=0,high_score=0) -> None:
        self.filename=filename
        self.current_score=current_score
        self.high_score=high_score
    
    def add_points(self,points):
        self.current_score += points
            
    def reset(self):
        self.current_score = 0
    def save(self):
        if self.current_score > self.high_score:
            with open(self.filename, 'w') as f:
                f.write(str(self.current_score))

    def load(self):
        with open(self.filename, 'r') as f:
            return int(f.read())