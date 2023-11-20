import pygame
import Finding
from Finding import matrix1
pathfinder=Finding.Pathfinder(matrix1)
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
        self.current_image=self.tileset[0][0]
        self.collision_rects = []

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
        self.current_image=pygame.transform.scale(self.tileset[self.frames[self.frame]][self.direction],(self.width,self.height))
        self.image_rect=self.current_image.get_rect(center=(self.x,self.y))
        self.change_direction()
        window.blit(self.current_image,self.image_rect)
        # pygame.draw.rect(window,("Blue"),self.image_rect,2)

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
        self.image_rect=self.current_image.get_rect(center=(self.x,self.y))

        # self.tileset[self.frames[self.frame][self.direction]][1]=(self.x,self.y,self.width,self.height)
        self.draw()


def load_tileset(filename,width,height):
    image=pygame.image.load(filename).convert_alpha()
    image_width, image_height=image.get_size()
    tileset=[]
    for tile_x in range(0,image_width//width):
        line=[]
        tileset.append(line)
        for tile_y in range (0,image_height//height):
            rect=(tile_x*width,tile_y*height,width,height)
            line.append(image.subsurface(rect))
    
    return tileset


class Enemy(Entity):
    def __init__(self,x,y,width,height,tileset,speed,health):
        super().__init__(x,y,width,height,tileset,speed,health)

        self.collider=[width,height]

        enemies.append(self)

   

    
    def set_path(self,path):
        self.path=path
        self.create_collision_rects()
        self.get_velocity()

    def update(self, player):
        # enemy_center=self.get_center()
        # player_center=player.get_center()

        # self.velocity=pygame.math.Vector2(player_center[0]-enemy_center[0], player_center[1]-enemy_center[1])
        # self.velocity.normalize_ip()
        # super().update()
        pathfinder.create_path(self,player)
        self.set_path(pathfinder.get_path())
        self.get_velocity()
        self.x +=self.velocity[0]*self.speed
        self.y +=self.velocity[1]*self.speed
        # self.check_collisions()
        self.image_rect=self.current_image.get_rect(center=(self.x,self.y))

        super().draw()

    def create_collision_rects(self):
        if self.path:
            self.collision_rects = []
            for point in self.path:
                x=(point.x*48)+24
                y=(point.y*49)+24.5
                rect=pygame.Rect((x-3.5,y-3.5),(7,7))
                pygame.draw.rect(window,"Blue",rect)
                self.collision_rects.append(rect)

    # def check_collisions(self):
    #     if self.collision_rects:
    #         for rect in self.collision_rects:
    #             if rect.colliderect(self.image_rect):
    #                 del self.collision_rects[0]
    #                 self.get_velocity()

    def get_velocity(self):
        if self.collision_rects:
            start=pygame.math.Vector2(self.x,self.y)
            end=pygame.math.Vector2(self.collision_rects[0].center)
            # print(start)
            # print(end)
            self.velocity = (end-start).normalize()
            del self.collision_rects[0]
        else:
            self.velocity = pygame.math.Vector2(0,0)
            self.path=[]

    def change_direction(self):
        super().change_direction()

        if self.velocity[1]>self.velocity[0]>0:
            self.direction=DOWN
        elif self.velocity[1]<self.velocity[0]<0:
            self.direction=UP
    def take_damage(self,damage):
        self.health-=damage
        if self.health<=0:
            self.destroy()    


    def destroy(self):
        spawn_particles(self.x-self.width/2,self.y-self.height/2)
        objects.remove(self)
        enemies.remove(self)    

    def get_center(self):
        return self.x+self.width/2,self.y+self.height/2
        

def spawn_particles(x,y):
    particle=Object(x,y,50,50,pygame.image.load("Zombies/Slime.png"))
    particles.append(particle)

# class Player:
#     def __init__(self,x,y,width,height,tileset,speed,health):
#         self.x=x
#         self.y=y
#         self.width=width
#         self.height=height
#         self.tileset=pygame.image.load(tileset)
#         self.tileset_rect=self.tileset.get_rect(center=(x,y))
#         self.speed=speed
#         self.health=health
#         self.velocity=[0,0]
#         self.collider=[width,height]

#     def update(self):
#         self.x+=self.velocity[0]*self.speed
#         self.y+=self.velocity[1]*self.speed
#         self.tileset_rect=self.tileset.get_rect(center=(self.x,self.y))
#         window.blit(self.tileset,self.tileset_rect)
   
#     def get_center(self):
#         return self.x+self.width/2,self.y+self.height/2

# def check_input(key,value):
#     if key==pygame.K_LEFT:
#         player_input["left"]=value
#     elif key==pygame.K_RIGHT:
#         player_input["right"]=value
#     elif key==pygame.K_UP:
#         player_input["up"]=value
#     elif key==pygame.K_DOWN:
#         player_input["down"]=value

# player_input={"left": False, "right": False, "up":False, "down":False}


# player=Player(1280/2,780/2,75,75,"Zombies/Wizard Zombie.png",3,3)
# enemy=Enemy(100,100,50,50,"Zombies/Baby Zombie.png",2,3)

# Run=True

# while Run:
#     window.fill("White")
#     for event in pygame.event.get():
#         if event.type==pygame.QUIT:
#             Run=False
#         elif event.type==pygame.KEYDOWN:
#             check_input(event.key,True)
#         elif event.type==pygame.KEYUP:
#             check_input(event.key,False)

#     for p in particles:
#         p.image.set_alpha(p.image.get_alpha()-1)
#         if p.image.get_alpha()==0:
#             objects.remove(p)
#             particles.insert(0,p)

#     for i in range (0,len(objects)):
#         objects[i].update()
   
#     for e in enemies:
#         if pygame.Rect.colliderect(e.image_rect,player.tileset_rect)==True:
#             player.health-=1
#             e.take_damage(1)
#             continue

#     player.velocity[0]= player_input["right"] - player_input["left"]
#     player.velocity[1]= player_input["down"] - player_input["up"]
#     player.update()
#     clock.tick(60)
#     pygame.display.update()
# pygame.quit()