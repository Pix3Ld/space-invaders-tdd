import pygame
class Player():
    '''player basic logic'''

    def __init__(self,x,y,hp,speed) -> None:
        self.x = x
        self.y = y
        self.hp=hp
        self.speed=speed
        
    def is_alive(self) -> bool:
        return self.hp > 0
    
    def move_left(self):
        self.x -= self.speed

    def move_right(self):
        self.x += self.speed
