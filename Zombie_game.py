import pygame
import pathfinding
pygame.init()
SCREEN_SIZE=(1400,787)
window=pygame.display.set_mode(SCREEN_SIZE)
clock=pygame.time.Clock()
DOWN=0
RIGHT=1 
UP=2 
LEFT=3
ANIMATION_FRAME_RATE = 10

objects=[]
enemies=[]
particles=[]

class Object:
    def __init__(self,x,y,width,height,image):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.image=image

        self.collider=[width,height]

        self.velocity=pygame.math.Vector2(0,0)

        objects.append(self)

    def draw(self):
        
        window.blit(pygame.transform.scale(self.image,(self.width,self.height)),(self.x,self.y))

    def update(self):
        self.x +=self.velocity[0]
        self.y+=self.velocity[1]
        self.draw()

    def get_center(self):

        return self.x+self.width/2, self.y+self.height/2

class Entity(Object):
    def __init__(self,x,y,width,height,tileset,speed,health):
        super().__init__(x,y,width,height,None)

        self.speed = speed
        self.health=health

        self.tileset = load_tileset(tileset,41,36)
        self.image_rect=pygame.Rect(0,0,0,0)
        self.direction=0
        self.frame=0
        self.frames=[1,0,1,2]
        self.frame_timer=0
        
    def change_direction(self):
        if self.velocity[0]<0:
            self.direction=LEFT
        elif self.velocity[0]>0:
            self.direction=RIGHT
        elif self.velocity[1]>0:
            self.direction=DOWN
        elif self.velocity[1]<0:
            self.direction=UP


    def draw(self):
        image=pygame.transform.scale(self.tileset[self.frames[self.frame]][self.direction],(self.width,self.height))
        self.image_rect=image.get_rect()
        self.change_direction()
        window.blit(image,(self.x,self.y))
        pygame.draw.rect(window,("Blue"),(self.x,self.y,self.width,self.height),2)

        # self.tileset[self.frames[self.frame][self.direction]][1]=(self.x,self.y,self.width,self.height)
        if self.velocity[0]==0 and self.velocity[1]==0:
            self.frame=0
            return 
        
        self.frame_timer+=1
        if self.frame_timer<ANIMATION_FRAME_RATE:
            return 
        
        self.frame+=1
        if self.frame>=len(self.frames):
            self.frame=0

        self.frame_timer=0

    def update(self):
        self.x+=self.velocity[0]*self.speed
        self.y+=self.velocity[1]*self.speed
        # self.tileset[self.frames[self.frame][self.direction]][1]=(self.x,self.y,self.width,self.height)
        self.draw()


def load_tileset(path,width,height):
    image=pygame.image.load(path).convert_alpha()
    image_width, image_height=image.get_size()
    tileset=[]
    for tile_x in range(0,image_width//width):
        line=[]
        tileset.append(line)
        for tile_y in range (0,image_height//height):
            rect=(tile_x*width,tile_y*height,width,height)
            line.append(image.subsurface(rect))
    
    return tileset

def check_collisions(obj1, obj2):
    x1,y1 =obj1.get_center()
    x2,y2 =obj2.get_center()
    w1,h1 =obj1.collider[0]/2, obj1.collider[1]/2
    w2,h2 =obj2.collider[0]/2, obj2.collider[1]/2
    if x1+w1>x2-w2 and x1-w1<x2+w2:
        return y1+h1>y2-h2 and y1-h1<y2+h2
    return False

class Enemy(Entity):
    def __init__(self,x,y,width,height,tileset,speed,health):
        super().__init__(x,y,width,height,tileset,speed,health)

        # self.max_width=width
        # self.max_height=height

        # self.width=0
        # self.height=0

        self.collider=[width,height]

        
        # self.start_timer=pygame.time.get_ticks()
    
    # def cooldown(self,time):
    #     a=pygame.time.get_ticks()-self.start_timer
    #     if a<time*1000:
    #         self.x=-1
    #         self.y=-1
        
        # self.width = int(self.max_width*(a/time*1000))
        # self.height = int(self.max_height*(a/time*1000))
        enemies.append(self)
    def update(self,player):
        enemy_center=enemy.get_center()
        player_center=player.get_center()

        self.velocity=pygame.math.Vector2(player_center[0]-enemy_center[0], player_center[1]-enemy_center[1])
        self.velocity.normalize_ip()

        # self.cooldown(2)
        
        super().update()


    def take_damage(self,damage):
        self.health-=damage
        if self.health<=0:
            self.destroy()    


    def destroy(self):
        spawn_particles(self.x,self.y)
        objects.remove(self)
        enemies.remove(self)    
    def get_center(self):
        return self.x+self.width/2,self.y+self.height/2
        

def spawn_particles(x,y):
    particle=Object(x,y,75,75,pygame.image.load("Zombie/Zombies/particles.png"))
    particles.append(particle)

class Player:
    def __init__(self,x,y,width,height,tileset,speed,health):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.tileset=pygame.image.load(tileset)
        self.tileset_rect=self.tileset.get_rect()
        self.speed=speed
        self.health=health
        self.velocity=[0,0]
        self.collider=[width,height]

    def update(self):
        self.x+=self.velocity[0]*self.speed
        self.y+=self.velocity[1]*self.speed
        pygame.draw.rect(window,("Blue"),(self.x,self.y,self.width,self.height))
   
    def get_center(self):
        return self.x+self.width/2,self.y+self.height/2

def check_input(key,value):
    if key==pygame.K_LEFT:
        player_input["left"]=value
    elif key==pygame.K_RIGHT:
        player_input["right"]=value
    elif key==pygame.K_UP:
        player_input["up"]=value
    elif key==pygame.K_DOWN:
        player_input["down"]=value

player_input={"left": False, "right": False, "up":False, "down":False}


player=Player(1280/2,780/2,75,75,"D:/PythonE/Zombie/Zombies/Wizard Zombie.png",5,3)
enemy=Enemy(100,100,100,100,"Zombie/Zombies/Baby Zombie.png",2,3)
# 
Run=True
while Run:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            Run=False
        elif event.type==pygame.KEYDOWN:
            check_input(event.key,True)
        elif event.type==pygame.KEYUP:
            check_input(event.key,False)
    for p in particles:
        p.image.set_alpha(p.image.get_alpha()-1)
        if p.image.get_alpha()==0:
            objects.remove(p)
            particles.remove(p)
            continue
        objects.remove(p)
        objects.insert(0,p)
    if pygame.Rect.colliderect(enemy.image_rect,player.tileset_rect):
        player.health-=1
        enemy.destroy()
        continue
    window.fill("White")
    player.velocity[0]= player_input["right"] - player_input["left"]
    player.velocity[1]= player_input["down"] - player_input["up"]
    enemy.update(player)
    player.update()
    clock.tick(60)
    pygame.display.update()
pygame.quit()