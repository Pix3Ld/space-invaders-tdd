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