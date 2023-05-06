import pygame
import sys
import os
import neat
from glob import glob
import random

score = 0
generation = 0

pygame.init()
screen = pygame.display.set_mode((800, 420))
clock = pygame.time.Clock()

cactus_spawnpos_x = [820, 900, 980, 1060, 2040, 3020, 4000]

class Dino(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super(Dino, self).__init__()
        self.list = [self.convert(f) for f in glob("sprites/dino.png")]
        self.image = self.list[0]
        self.rect = self.image.get_rect()

        self.x = x
        self.y = y

        self.isJump = False
        self.jumpCount = 15

        self.mask = pygame.mask.from_surface(self.image)

    def convert(self, f):
        return pygame.image.load(f).convert_alpha()

    def update(self):
        self.rect = pygame.Rect(self.x, self.y, 64, 64)
        screen.blit(self.image, (self.x, self.y))

    def jump(self):
        if self.isJump:
            if self.jumpCount >= -15:
                neg = 1
                if self.jumpCount < 0:
                    neg = -1
                self.y -= self.jumpCount**2 * 0.12 * neg
                self.jumpCount -= 1
            else:
                self.isJump = False
                self.jumpCount = 15

    def deathCheck(self, sprite1, sprite2):
        col = pygame.sprite.collide_rect(sprite1, sprite2)
        if col == True:
            sys.exit()

class Cactus(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super(Cactus, self).__init__()
        
        self.list = [self.convert(f) for f in glob("sprites/cactus.png")]
        self.image = self.list[0]
        self.rect = self.image.get_rect()

        self.x = x
        self.y = y

        self.mask = pygame.mask.from_surface(self.image)

    def convert(self, f):
        return pygame.image.load(f).convert_alpha()

    def update(self):
        self.rect = pygame.Rect(self.x, self.y, 64, 128)
        screen.blit(self.image, (self.x, self.y))

    def cactus_move(self):
        self.x -= 7

        if self.x <= -10:
            self.x = cactus_spawnpos_x[random.randint(0, 6)]

cactus = Cactus(cactus_spawnpos_x[random.randint(0, 6)], 320)
cactus1 = Cactus(cactus_spawnpos_x[random.randint(0, 6)], 320)
cactus2 = Cactus(cactus_spawnpos_x[random.randint(0, 6)], 320)
cactus3 = Cactus(cactus_spawnpos_x[random.randint(0, 6)], 320)

dino = Dino(50, 320)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            break
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Start to jump by setting isJump to True.
                dino.isJump = True

    screen.fill('white')

    cactus.update()
    cactus1.update()
    cactus2.update()
    cactus3.update()

    cactus.cactus_move()
    cactus1.cactus_move()
    cactus2.cactus_move()
    cactus3.cactus_move()

    dino.update()
    dino.jump()

    if pygame.sprite.collide_mask(cactus, dino):
        sys.exit()
    if pygame.sprite.collide_mask(cactus1, dino):
        sys.exit()
    if pygame.sprite.collide_mask(cactus2, dino):
        sys.exit()
    if pygame.sprite.collide_mask(cactus3, dino):
        sys.exit()

    pygame.display.flip()

    clock.tick(60)

# if __name__ == "__main__":
#     # setup config
#     config_path = "./config-feedforward.txt"
#     config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

#     # init NEAT
#     p = neat.Population(config)

#     # run NEAT
#     p.run(run_generation, 1000)
