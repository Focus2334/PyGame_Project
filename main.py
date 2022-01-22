import os
import sys
import pygame
import math
import random

pygame.init()
size = width, height = 1000, 1000
screen = pygame.display.set_mode(size)
fps = 60
cl = pygame.time.Clock()
cl.tick(fps)
mousepos = (0, 0)
chpos = (0, 0)
xr = False
xl = False
yd = False
yu = False


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Bullet(pygame.sprite.Sprite):
    image = load_image("bl.png")

    def __init__(self, gr, x, y):
        super().__init__(gr)
        self.image = Bullet.image
        self.image1 = Bullet.image
        self.rect = self.image.get_rect()
        self.pos = pygame.math.Vector2(x, y)
        self.rect.center = round(self.pos.x), round(self.pos.y)
        g = math.degrees(math.atan2(self.rect.centerx - mousepos[0], self.rect.centery - mousepos[1]))
        py = abs(g) / 90 - 1
        if g < 0:
            px = 1 - abs(py)
        else:
            px = (1 - abs(py)) * -1
        self.dir = pygame.math.Vector2((px, py))

    def update(self):
        self.pos += self.dir * 20
        self.rect.center = round(self.pos.x), round(self.pos.y)


class Enemy(pygame.sprite.Sprite):
    image = load_image("enemy.png")

    def __init__(self, gr, x, y):
        super().__init__(gr)
        self.image = Enemy.image
        self.image1 = Enemy.image
        self.rect = self.image.get_rect()
        self.pos = pygame.math.Vector2(x, y)
        self.rect.center = round(self.pos.x), round(self.pos.y)
        self.vec = True
        self.rot = 0
        self.dir = pygame.math.Vector2((0, 0))

    def update(self):
        if pygame.sprite.spritecollideany(self, blts):
            self.kill()
        self.rot = math.atan2(self.rect.centerx - char.rect.centerx, self.rect.centery - char.rect.centery)
        g = int(math.degrees(self.rot))
        py = abs(g) / 90 - 1
        if g < 0:
            px = 1 - abs(py)
        else:
            px = (1 - abs(py)) * -1
        self.dir = pygame.math.Vector2((px, py))
        self.pos += self.dir * 1
        self.rect.center = round(self.pos.x), round(self.pos.y)
        self.image = pygame.transform.rotate(self.image1, int(math.degrees(self.rot)))


class MainCh(pygame.sprite.Sprite):
    image = load_image("mar.png")

    def __init__(self):
        super().__init__()
        self.image = MainCh.image
        self.image1 = MainCh.image
        self.rect = self.image.get_rect()
        self.rect.x = 10
        self.rect.y = 30
        self.vec = True
        self.rot = 0

    def move(self):
        if xr:
            self.rect = self.rect.move(10, 0)
        if xl:
            self.rect = self.rect.move(-10, 0)
        if yd:
            self.rect = self.rect.move(0, 10)
        if yu:
            self.rect = self.rect.move(0, -10)

    def update(self):
        self.rot = math.atan2(self.rect.centerx - mousepos[0], self.rect.centery - mousepos[1])
        self.move()
        self.image = pygame.transform.rotate(self.image1, int(math.degrees(self.rot)) + 90)


running = True
chr = pygame.sprite.Group()
enms = pygame.sprite.Group()
blts = pygame.sprite.Group()
char = MainCh()
chr.add(char)
enm_spawn = 60 * 5
while running:
    print(cl.get_fps())
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEMOTION:
            mousepos = event.pos
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                yd = True
            if event.key == pygame.K_UP:
                yu = True
            if event.key == pygame.K_RIGHT:
                xr = True
            if event.key == pygame.K_LEFT:
                xl = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                yd = False
            if event.key == pygame.K_UP:
                yu = False
            if event.key == pygame.K_RIGHT:
                xr = False
            if event.key == pygame.K_LEFT:
                xl = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            Bullet(blts, char.rect.centerx, char.rect.centery)
    if enm_spawn < 0:
        Enemy(enms, random.randint(10, 510), 500)
        enm_spawn = fps * 5
    else:
        enm_spawn -= 1
    blts.draw(screen)
    chr.draw(screen)
    enms.draw(screen)
    enms.update()
    chr.update()
    blts.update()
    pygame.display.flip()
    cl.tick(60)
pygame.quit()
