class Player():
    '''player basic logic'''

    def __init__(self,x,y,hp,speed,screen_width=800) -> None:
        
        self.x = x
        self.y = y
        self.hp=hp
        self.speed=speed
        self.screen_width = screen_width

        self.starting_x = x
        self.starting_y = y
        self.starting_hp = hp


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
    
    def shoot(self) -> "Bullet | None":
        return Bullet(x=self.x,y=self.y,speed=10,damage=1,direction='up',owner=self) if self.is_alive() else None
    
    def position_reset(self):
        self.x = self.starting_x
        self.y = self.starting_y
        self.hp = self.starting_hp
    

class Bullet():
    '''bullet basic logic'''
    def __init__(self,x,y,speed,damage,direction,owner) -> None:
        self.x = x
        self.y = y
        self.speed = speed
        self.damage = damage
        self.diraction = direction
        self.owner = owner