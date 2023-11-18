import pygame

pygame.init()
SCREEN_SIZE=(1400,787)
window=pygame.display.set_mode((SCREEN_SIZE))
enemies=[]
particles=[]
UP=2
LEFT=3
DOWN=0
RIGHT=1
ANIMATION_FRAME_RATE=10
class Player:
    def __init__(self,x,y,width,height,filename):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.collider=[width,height]
        self.filename=filename


    def get_center(self):
        return self.x+self.width/2, self.y+self.height/2


    def update(self):

        window.blit(pygame.image.load(self.filename).convert_alpha(),(self.x,self.y))

class Enemy:
    def __init__ (self,x,y,width,height,speed,health):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        
        self.collider=[width,height]

        self.speed=speed
        self.health=health
        self.velocity=pygame.math.Vector2(0,0)
       
        enemies.append(self)
       
        self.frame=0
        
        self.frames=[1,0,1,2]
        
        self.direction=0

        self.frame_timer=0

        self.tileset=load_tileset("Zombie/Zombies/Baby Zombie.png",41,36)
        
    
    def change_direction(self):
        if self.velocity[0]<0:
            self.direction=LEFT
        elif self.velocity[0]>0:
            self.direction=RIGHT
        elif self.velocity[1]>0:
            self.direction=DOWN
        elif self.velocity[1]<0:
            self.direction=UP

        if self.velocity[1]>self.velocity[0]>0:
            self.direction=DOWN
        elif self.velocity[1]<self.velocity[0]<0:
            self.direction=UP
    
    #Get center coordinate of object 
    def get_center(self):
        return self.x+self.width/2, self.y+self.height/2
    
    def draw(self):
        image=pygame.transform.scale(self.tileset[self.frames[self.frame]][self.direction],(self.width,self.height))
        self.change_direction()
        window.blit(image,(self.x,self.y))
        pygame.draw.rect(window,("Blue"),(self.x,self.y,self.width,self.height),2)
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


    def update(self,player):
        enemy_center=self.get_center()
        player_center=player.get_center()

        # Chase player
        self.velocity=pygame.math.Vector2(player_center[0]-enemy_center[0],player_center[1]-enemy_center[1])
        self.velocity.normalize_ip()
        # The next coordinate
        self.x+=self.velocity[0]*self.speed
        self.y+=self.velocity[1]*self.speed
        self.draw()

    def take_damage(self,damage):
        self.health-=damage
        if self.health<=0:
            self.destroy()

    def destroy(self):
        spawn_particles(self.x,self.y)
        enemies.remove(self)


def spawn_particles(x,y):
    particle=pygame.transform.scale(pygame.image.load("Zombie/Zombies/Slime.png").convert_alpha(),(50,50))
    particles.append(particle)

# Split the frame into frames from tileset
def load_tileset(filename,width,height):
    image=pygame.image.load(filename).convert_alpha()
    image_width, image_height = image.get_size()
    tileset=[]
    for tile_x in range(0,image_width//width):
        line=[]
        tileset.append(line)
        for tile_y in range(0,image_height//height):
            rect=(tile_x*width,tile_y*height,width,height)
            line.append(image.subsurface(rect))
    return tileset


# def check_collision(obj1, obj2):
#     x1,y1=obj1.get_center()
#     x2,y2=obj2.get_center()
#     w1,h1=obj1.collider[0]/2-10, obj1.collider[1]/2-10
#     w2,h2=obj2.collider[0]/2-10, obj2.collider[1]/2-10
#     if x1+w1>x2-w2 and x1-w1<x2+w2:
#         return y1+h1>y2-h2 and y1-h1<y2+h2
#     return False