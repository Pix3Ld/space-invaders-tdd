

class Player():
    '''player basic logic'''

    def __init__(self,
                 x, y, 
                 hp,speed,
                 points,screen_width=800) -> None:
        
        self.x = x
        self.y = y
        self.hp=hp
        self.speed=speed
        self.screen_width = screen_width
        self.points = points

        self.starting_x = x
        self.starting_y = y
        self.starting_hp = hp
        self.starting_points = points


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
            self.hp = max(0,self.hp - dmg) 
    
    def shoot(self) -> "Bullet | None":
        return Bullet(x=self.x,
                      y=self.y,
                      speed=10,
                      damage=1,
                      direction='up',
                      owner=self) if self.is_alive() else None
    
    def player_reset(self):
        if not self.is_alive():
            self.x = self.starting_x
            self.y = self.starting_y
            self.hp = self.starting_hp
            self.points= self.starting_points
    
    def player_score(self):
        if self.is_alive() and Enemy.enemy_down:
            self.points+=100

class Bullet():

    '''bullet basic logic'''
    def __init__(self,
                 x,y,
                 speed,damage,
                 direction,owner) -> None:
        self.x = x
        self.y = y
        self.speed = speed
        self.damage = damage
        self.direction = direction
        self.owner = owner

class Enemy():
    '''enemy basic logic'''
    def __init__(self,x,y,hp,speed,diraction,damage=1,screen_width=800,screen_hight=800) -> None:
        self.x = x
        self.y = y
        self.hp = hp
        self.speed = speed
        self.damage = damage
        self.screen_width = screen_width
        self.screen_hight = screen_hight
        self.diraction=diraction
        
    def enemy_down(self) -> bool:
        return self.hp <= 0
    
    def move_right(self):
        if self.x + self.speed <= self.screen_width:
            self.x += self.speed
    
    def move_left(self):
        if self.x - self.speed >=0:
            self.x -= self.speed
    
    def move_down(self):
        if self.y + self.speed <= self.screen_hight:
            self.y += self.speed 
    
    def shoot(self) -> "Bullet | None":
        return Bullet(x=self.x,y=self.y,
                      speed=10,damage=1,
                      direction='down',owner=self) if not self.enemy_down() else None

    def diraction_change(self):
        if not self.enemy_down():
            if self.diraction==1:
                self.move_right()
            elif self.diraction==-1:
                self.move_left()

class Barrier():
    
    def __init__(self,x,y,hp,width,height) -> None:
        self.x = x
        self.y = y
        self.hp = hp
        self.width = width
        self.height = height
    
    def is_destroyed(self) -> bool:
        return self.hp <= 0
    def take_damage(self,dmg):
        if not self.is_destroyed():
            self.hp = max(0,self.hp - dmg)