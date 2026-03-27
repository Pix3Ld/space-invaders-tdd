class Player():
    '''player basic logic'''

    def __init__(self,x,y,hp,speed,screen_width=800) -> None:
        self.x = x
        self.y = y
        self.hp=hp
        self.speed=speed
        self.screen_width = screen_width

    def is_alive(self) -> bool:
        return self.hp > 0
    
    def move_left(self):
        if self.x - self.speed >= 0:
            self.x -= self.speed 

    def move_right(self):
        if self.x + self.speed <= self.screen_width: 
            self.x += self.speed  

    def take_damage(self,dmg):
        if self.is_alive():
            self.hp -= dmg
