import time

import numpy as np
import contextlib
with contextlib.redirect_stdout(None):
    import pygame

class Game:
    def __init__(self, size1, size2):
        self.size = (size1,size2)
        self.curWorld = np.zeros((size1, size2))
        self.futWorld = np.zeros((size1, size2))
        self.all_sprites = pygame.sprite.Group()
        self.count = 0

    def countCell(self, posX,posY):
        for i in range(posX-1 if posX-1>=0 else 0,posX+2 if posX+2 < self.futWorld.shape[0] else self.futWorld.shape[0]):
            for j in range(posY - 1 if posY - 1 >= 0 else 0,
                           posY + 2 if posY + 2 < self.futWorld.shape[1] else self.futWorld.shape[1] ):
                self.futWorld[posX,posY] += self.curWorld[i,j]
        self.futWorld[posX,posY] -= self.curWorld[posX,posY]
        if self.curWorld[posX,posY] == 0:
            if self.futWorld[posX,posY] == 3:
                self.futWorld[posX,posY] = 1
            else:
                self.futWorld[posX, posY] = 0
        else:
            if self.futWorld[posX,posY] == 3 or self.futWorld[posX,posY] == 2:
                self.futWorld[posX, posY] = 1
            else:
                self.futWorld[posX, posY] = 0

    def OneStep(self):
        for i in range (self.curWorld.shape[0]):
            for j in range (self.curWorld.shape[1]):
                self.countCell(i,j)
        self.curWorld = self.futWorld.copy()
        self.futWorld = np.zeros(self.size)
        self.count += 1

    def GiveLife(self,x,y):
        if self.curWorld[x,y] == 1:
            self.curWorld[x,y] = 0
        else:
            self.curWorld[x, y] = 1

    def CreateScene(self):
        self.all_sprites.empty()
        for i in range (self.curWorld.shape[0]):
            for j in range (self.curWorld.shape[1]):
                if self.curWorld[i,j] == 1:
                    self.all_sprites.add(Cell(i, j))

    def Clear(self):
        self.curWorld = np.zeros(self.size)
        self.count = 0

class Cell(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((9, 9))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (x*10, y*10)




size1 = 200
size2 = 100
g = Game(size1, size2)

BLACK = (0, 0, 0)
WIDTH = 2000  # ширина игрового окна
HEIGHT = 1000 # высота игрового окна
FPS = 60 # частота кадров в секунду
pygame.init()
pygame.mixer.init()  # для звука
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()
font = pygame.font.SysFont(name='arial', size=20)

pause = 0
stening = False
running = True
isPlus = False
isMinus = False
while running:
    g.CreateScene()
    g.all_sprites.update()
    clock.tick(FPS)
    screen.fill(BLACK)
    pygame.font.init()
    surf = font.render(f"{g.count}", True, (255, 255, 255))
    if g.count == 0:
        surf = font.render(f"{g.count} нажми в лбую точку поля, для добавления клетки. пробел - чтобы начать, r - что бы перезапустить, \"+\" - замедлить, \"-\" - ускорить", True, (255, 255, 255))
    g.all_sprites.draw(screen)
    screen.blit(surf, (20, 20))
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                stening = True
            if pygame.key.get_pressed()[pygame.K_r]:
                g.Clear()
            if pygame.key.get_pressed()[pygame.K_KP_PLUS]:
                isPlus = True
            if pygame.key.get_pressed()[pygame.K_KP_MINUS]:
                isMinus = True
        elif event.type == pygame.KEYUP:
            if event.key in [pygame.K_SPACE]:
                stening = False
            if event.key in [pygame.K_KP_PLUS]:
                isPlus = False
            if event.key in [pygame.K_KP_MINUS]:
                isMinus = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                g.GiveLife(event.pos[0]//10,event.pos[1]//10)

    if isPlus:
        pause+=0.01
    if isMinus:
        if(pause>0):
            pause-=0.01
        if pause < 0:
            pause = 0.0
    if stening:
        g.OneStep()
        time.sleep(pause)
