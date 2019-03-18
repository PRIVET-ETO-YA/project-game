import pygame
import os
import random
import sys
pygame.init()
size = width, height = 590, 590
screen = pygame.display.set_mode(size)
w = pygame.Surface((800, 640))
fps = 50
gravity = 0.25
b = False
running = True
final = False
c = [-590, 0]
font = pygame.font.Font (None, 50)
poss = []

def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    image = image.convert_alpha()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image 

zomb = pygame.sprite.Group()

class Menu():
    def __init__(self, punkts = [150, 150, "start", (71, 74, 81), (255, 0, 0)]):
        self.punkts = punkts
        
    def render(self, screeen, font, number):
        for i in self.punkts:
            if number == i[5]:
                screeen.blit(font.render(i[2], 1, i[4]), (i[0], i[1]))
            else:
                screeen.blit(font.render(i[2], 1, i[3]), (i[0], i[1]))
    def menu(self):
        fon2 = load_image("intro2.png")
        done = True
        fontm = pygame.font.Font (None, 100)
        p = 0
        while done:
            screen.fill((255, 255, 255))
            screen.blit(fon2, (0, 0))
            mp = pygame.mouse.get_pos()
            for i in self.punkts:
                if mp[0] > i[0] and mp[0] < i[0] + 310 and mp[1] > i[1] and mp[1] < i[1] + 100:
                    p = i[5]
                self.render(screen, fontm, p)
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    sys.exit() 
                if e.type == pygame.KEYDOWN: 
                    keys = pygame.key.get_pressed()
                    if e.key == pygame.K_UP and p > 0:
                        p -= 1
                    if e.key == pygame.K_DOWN and p < len(self.punkts) - 1:       
                        p += 1   
                if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    if p == 0:
                        done = False
                    elif p == 1:
                        sys.exit()
            pygame.display.flip()
            
class Zombie(pygame.sprite.Sprite):
    
    image = load_image("zombie.png")
    
    def __init__(self, group):
        super().__init__(zomb)
        global poss
        self.image = Zombie.image
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, 540, 60)
        self.rect.y = random.randrange(0, 540, 60)
        while [self.rect.x, self.rect.y] in poss:
            self.rect.x = random.randrange(0, 540, 60)
            self.rect.y = random.randrange(0, 540, 60)            
 
    def get_eventt(self, a):
        if self.rect.collidepoint((a[0] + 30, a[1] + 30)):
            return True
        return False
    
joys = pygame.sprite.Group()

class Joystik(pygame.sprite.Sprite):
    
    image = load_image("joystick.png")
    
    def __init__(self, group, a):
        super().__init__(joys)
        self.image = Joystik.image
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, 540, 60)
        self.rect.y = random.randrange(0, 540, 60)
        global poss
        poss.append(a)
        poss.append([self.rect.x, self.rect.y])  
 
    def get_event(self, a, kolvo):
        if self.rect.collidepoint((a[0] + 30, a[1] + 30)):
            global poss
            poss = []
            for zombie in zomb:
                zomb.remove(zombie)
            joys.remove(joystik)
            Joystik(joys, a)
            for i in range(kolvo):
                Zombie(zomb)          
            return 1
        return 0
a = [0, 0] 
kolvo = 10
for i in range(1):
    Joystik(joys, a)
for i in range(kolvo):
    Zombie(zomb)
punkts = [[75, 480, "START", (153, 64, 154), (255, 0, 0), 0], 
          [325, 480, "QUIT", (153, 64, 154), (255, 0, 0), 1]]
game = Menu(punkts)
game.menu()
pygame.mouse.set_visible(False)
g = load_image("gamer.png")
fon = load_image("field.png")
go = load_image("over.png")
screen_rect = (0, 0, width, height)
clock = pygame.time.Clock()
a = [0, 0]
score = 0
score2 = 0
step = 60
pygame.display.flip()

running = True
while running:
    if final == False:
        if score - score2 == 10:
            kolvo += 2
            score2 += 2
        for joystik in joys:
            score += joystik.get_event(a, kolvo)
        for zombie in zomb:
            final = zombie.get_eventt(a)
            if final == True:
                break        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False 
          
            if event.type == pygame.KEYDOWN: 
                                          
                keys = pygame.key.get_pressed()
                if (event.key == pygame.K_LEFT or event.key == pygame.K_a) and a[0] != 0:
                    a[0] -= step 
                elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and a[0] != 540:
                    a[0] += step
                elif (event.key == pygame.K_UP or event.key == pygame.K_w) and a[1] != 0:
                    a[1] -= step
                elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and a[1] != 540:       
                    a[1] += step
        text = font.render ( "Score:" + str (score), True, (255, 0, 0))
        screen.fill((255, 255, 255))       
        screen.blit(fon, (0, 0))
        zomb.draw(screen)
        joys.draw(screen) 
        screen.blit(g, a)
        screen.blit (text, [4,4])
        pygame.display.flip()
        clock.tick(50)  
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False             
        if c[0] < 0: 
            c[0] += 200 * clock.tick() / 1000
        screen.blit(go, c)
        pygame.display.flip()        
pygame.quit()
pygame.init()