import os
import sys
import pygame
import math
import random
from PIL import Image
import numpy as np

pygame.init()
size = width, height = 1000, 800
screen = pygame.display.set_mode(size)
fps = 60
cl = pygame.time.Clock()
cl.tick(60)
mousepos = (0, 0)
chpos = (0, 0)
xr = False
xl = False
yd = False
yu = False
gun = {'name': 'Gun',  # имя
       'bult': 5,  # заряд
       'blmax': 5,  # макс. заряд
       'rof': 20,  # скорость стрельбы
       'nxt': 0,  # время до след. выстрела
       'fire': False,  # состояние стрельбы
       'acc': 2,  # разброс
       'rld': 100,  # время перезарядки
       'nxtrld': 0,  # время до конца перезарядки
       'img': 'gun.png'}  # изображение
avt = {'name': 'Avt',  # имя
       'bult': 30,  # заряд
       'blmax': 30,  # макс. заряд
       'rof': 10,  # скорость стрельбы
       'nxt': 0,  # время до след. выстрела
       'fire': False,  # состояние стрельбы
       'acc': 5,  # разброс
       'rld': 150,  # время перезарядки
       'nxtrld': 0,  # время до конца перезарядки
       'img': 'avt.png'}  # изображение


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["Bullet Time", "",
                  "Правила игры",
                  "Собирайте снаряжение, пока не закончилось время.",
                  "Оно вам пригодится, когда таймер покажет 00:00",
                  "И враги начнут нападать отовсюду"]

    fon = pygame.transform.scale(load_image('grass.png'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.SysFont('Impact', 35)
    text_coord = 50

    def dr(text_coord):
        for line in intro_text:
            string_rendered = font.render(line, True, pygame.Color('white'))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)

    prs = 'Нажмите любую кнопку'
    colr = [255, 255, 255]
    colb = False

    while True:
        screen.blit(fon, (0, 0))
        dr(text_coord)
        if not colb:
            colr = list(map(lambda x: x - 4, colr))
            if colr <= [150, 150, 150]:
                colb = True
        if colb:
            colr = list(map(lambda x: x + 4, colr))
            if colr >= [250, 250, 250]:
                colb = False
        strr = font.render(prs, True, colr)
        screen.blit(strr, (500 - strr.get_rect()[2] // 2, 700))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                main_menu()
                return
        pygame.display.flip()


def main_menu():
    fon = pygame.transform.scale(load_image('grass.png'), (width, height))
    screen.blit(fon, (0, 0))
    lvl1icon = pygame.transform.scale(load_image('lvl1icon.png'), (120, 180))
    lvl1_rect = (100, 300)
    screen.blit(lvl1icon, lvl1_rect)
    lvl_1 = False

    while True:
        screen.blit(fon, (0, 0))
        screen.blit(lvl1icon, lvl1_rect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEMOTION:
                if (lvl1_rect[0] < event.pos[0] < lvl1icon.get_rect()[2] + lvl1_rect[0]) and (
                        lvl1_rect[1] < event.pos[1] < lvl1icon.get_rect()[3] + lvl1_rect[1]):
                    lvl1icon = pygame.transform.scale(load_image('lvl1hovered.png'), (120, 180))
                    lvl_1 = True
                else:
                    lvl1icon = pygame.transform.scale(load_image('lvl1icon.png'), (120, 180))
                    lvl_1 = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if lvl_1:
                    return
        pygame.display.flip()


start_screen()


class Trap(pygame.sprite.Sprite):
    image = load_image("trap.png")

    def __init__(self, gr, x, y):
        super().__init__(gr)
        self.image = Trap.image
        self.image1 = Trap.image
        self.rect = self.image.get_rect()
        self.pos = pygame.math.Vector2(x, y)
        self.rect.center = round(self.pos.x), round(self.pos.y)


class Bullet(pygame.sprite.Sprite):
    image = load_image("bl.png")

    def __init__(self, gr, x, y):
        super().__init__(gr)
        self.image = Bullet.image
        self.image1 = Bullet.image
        self.rect = self.image.get_rect()
        self.pos = pygame.math.Vector2(x, y)
        self.rect.center = round(self.pos.x), round(self.pos.y)
        self.xp = mousepos[0]
        self.yp = mousepos[1]
        g = math.degrees(math.atan2(self.rect.centerx - self.xp, self.rect.centery - self.yp))
        py = abs(g) / 90 - 1 + (random.randint(-char.weapon['acc'], char.weapon['acc']) / 100)
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
        self.hp = 3
        self.rot = 0
        self.prlsd = False
        self.prlstm = 0
        self.dir = pygame.math.Vector2((0, 0))

    def update(self):
        if pygame.sprite.spritecollideany(self, blts):
            self.hp -= 1
            pygame.sprite.groupcollide(enms, blts, False, True)
        if self.hp <= 0:
            self.kill()
        if pygame.sprite.spritecollideany(self, trp):
            self.prlsd = True
            self.prlstm = fps * 3
            pygame.sprite.groupcollide(enms, trp, False, True)
        if self.prlstm > 0:
            self.prlstm -= 1
        else:
            self.prlsd = False
        if self.prlsd:
            return None
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
        self.weapon = gun
        self.wpns = [gun, avt]
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
trp = pygame.sprite.Group()
char = MainCh()
chr.add(char)
enm_spawn = fps * 5
curwp = char.wpns.index(char.weapon)
while running:
    if char.weapon['bult'] == 0:
        char.weapon['nxtrld'] = char.weapon['rld']
        char.weapon['bult'] = -1
    if char.weapon['nxtrld'] > 0:
        char.weapon['nxtrld'] -= 1
    if char.weapon['nxtrld'] == 0 and char.weapon['bult'] == -1:
        char.weapon['bult'] = char.weapon['blmax']
    if char.weapon['nxt'] > 0:
        char.weapon['nxt'] -= 1
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEMOTION:
            mousepos = event.pos
        if event.type == pygame.MOUSEWHEEL:
            curwp = char.wpns.index(char.weapon)
            if event.y == 1:
                curwp += 1
                if curwp == len(char.wpns):
                    curwp = 0
            char.weapon = char.wpns[curwp]
            print(char.weapon)
        if event.type == pygame.KEYDOWN:
            print(event.key)
            if event.key == 115:
                char.weapon = gun
            if event.key == 114:
                char.weapon['bult'] = 0
            if event.key == (pygame.K_DOWN or 115):
                yd = True
            if event.key == (pygame.K_UP or 119):
                yu = True
            if event.key == (pygame.K_RIGHT or 100):
                xr = True
            if event.key == (pygame.K_LEFT or 97):
                xl = True
        if event.type == pygame.KEYUP:
            if event.key == (pygame.K_DOWN or 115):
                yd = False
            if event.key == (pygame.K_UP or 119):
                yu = False
            if event.key == (pygame.K_RIGHT or 100):
                xr = False
            if event.key == (pygame.K_LEFT or 97):
                xl = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:
                Trap(trp, char.rect.centerx, char.rect.centery)
            elif event.button == 1:
                char.weapon['fire'] = True
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                char.weapon['fire'] = False
    if char.weapon['fire'] and not char.weapon['nxt'] and char.weapon['bult'] > 0:
        Bullet(blts, char.rect.centerx, char.rect.centery)
        if char.weapon['name'] == 'Gun':
            char.weapon['fire'] = False
        char.weapon['nxt'] = char.weapon['rof']
        char.weapon['bult'] -= 1

    if enm_spawn < 0:
        Enemy(enms, random.randint(10, 510), 500)
        enm_spawn = fps * 5
    else:
        enm_spawn -= 1
    trp.draw(screen)
    enms.draw(screen)
    blts.draw(screen)
    chr.draw(screen)
    trp.update()
    enms.update()
    chr.update()
    blts.update()
    blic = pygame.transform.scale(load_image('bulleticon.png'), (40, 76))
    blic.set_alpha((255 // char.weapon['blmax']) * char.weapon['bult'])
    font = pygame.font.SysFont('Impact', 35)
    if char.weapon['nxtrld']:
        rldtm = font.render(str(int(char.weapon['nxtrld'] / 60 * 10) / 10), True, pygame.Color('white'))
        screen.blit(rldtm, (905, 660))
    screen.blit(blic, (900, 650))
    pygame.display.flip()
    cl.tick(60)
pygame.quit()
