import os
import sys
import pygame
import math
import random
import sqlite3

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
con = sqlite3.connect("databaze.db")
cur = con.cursor()
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
       'bult': 12,  # заряд
       'blmax': 12,  # макс. заряд
       'rof': 12,  # скорость стрельбы
       'nxt': 0,  # время до след. выстрела
       'fire': False,  # состояние стрельбы
       'acc': 5,  # разброс
       'rld': 200,  # время перезарядки
       'nxtrld': 0,  # время до конца перезарядки
       'img': 'avt.png'}  # изображение
weapons = []


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


class Trap(pygame.sprite.Sprite):
    image = load_image("trap.png")
    image2 = pygame.transform.scale(load_image("trpd.png"), (30, 30))

    def __init__(self, gr, x, y, typ):
        super().__init__(gr)
        if typ == 0:
            self.image = Trap.image
            self.image1 = Trap.image
        if typ == 1:
            self.image = Trap.image2
            self.image1 = Trap.image2
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

    def __init__(self, gr, x, y, speed, hp, size):
        super().__init__(gr)
        self.image = pygame.transform.scale(Enemy.image, (size, size))
        self.image1 = self.image
        self.rect = self.image.get_rect()
        self.pos = pygame.math.Vector2(x, y)
        self.rect.center = round(self.pos.x), round(self.pos.y)
        self.vec = True
        self.hp = hp
        self.rot = 0
        self.prlsd = False
        self.prlstm = 0
        self.dir = pygame.math.Vector2((0, 0))
        self.ready = fps
        self.speed = speed

    def update(self):
        if self.ready > 0:
            self.ready -= 1
        if pygame.sprite.spritecollideany(self, blts):
            self.hp -= 1
            pygame.sprite.groupcollide(enms, blts, False, True)
        if self.hp <= 0:
            char.scr += 1
            self.kill()
        if pygame.sprite.spritecollideany(self, trp):
            self.prlsd = True
            self.prlstm = fps * 3
            pygame.sprite.groupcollide(enms, trp, False, True)
        if pygame.sprite.spritecollideany(self, trpd):
            char.scr += 1
            pygame.sprite.groupcollide(enms, trpd, True, True)
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
        if math.hypot(self.rect.centerx - char.rect.centerx, self.rect.centery - char.rect.centery) >= 30:
            self.pos += self.dir * self.speed
        else:
            if not self.ready:
                char.hp -= 1
                self.ready = fps

        self.rect.center = round(self.pos.x), round(self.pos.y)
        self.image = pygame.transform.rotate(self.image1, int(math.degrees(self.rot)))


class MainCh(pygame.sprite.Sprite):
    image = load_image("mar.png")

    def __init__(self):
        super().__init__()
        self.image = MainCh.image
        self.image1 = MainCh.image
        self.rect = self.image.get_rect()
        self.rect.x = width // 2
        self.rect.y = height // 2
        self.hp = 10
        self.scr = 0
        self.weapon = gun
        self.wpns = weapons
        self.vec = True
        self.rot = 0

    def move(self):
        if xr and self.rect.x < 980:
            self.rect = self.rect.move(4, 0)
        if xl and self.rect.x > 0:
            self.rect = self.rect.move(-4, 0)
        if yd and self.rect.y < 780:
            self.rect = self.rect.move(0, 4)
        if yu and self.rect.y > 0:
            self.rect = self.rect.move(0, -4)

    def update(self):
        self.rot = math.atan2(self.rect.centerx - mousepos[0], self.rect.centery - mousepos[1])
        self.move()
        self.image = pygame.transform.rotate(self.image1, int(math.degrees(self.rot)))


char = MainCh()
chr = pygame.sprite.Group()
enms = pygame.sprite.Group()
blts = pygame.sprite.Group()
trp = pygame.sprite.Group()
trpd = pygame.sprite.Group()
trpslc = 0
chr.add(char)


def set_id():  # функция создания id для ячеек
    id = []
    ids = cur.execute('SELECT id FROM score').fetchall()
    for i in range(len(ids)):
        id.append(ids[i][0])
    if not ids:
        return 0
    return max(id) + 1


def lvl1():
    global yd
    global yu
    global xr
    global xl
    global mousepos
    global trpslc
    for i in enms:
        i.kill()
    for i in blts:
        i.kill()
    char.rect.center = width // 2, height // 2
    for i in trp:
        i.kill()
    char.hp = 10
    enms.clear(screen, screen)
    running = True
    enm_spawn = fps * 10
    trp_spawn = fps * 6
    wpimg = char.weapon['img']
    wpns = ['Gun', 'Avt', 'Shotgun']
    for i in cur.execute('SELECT * FROM weapon').fetchall():
        for j in wpns:
            if i[0] == j:
                if i[1] == 'True':
                    if i[0] not in weapons:
                        if gun['name'] == i[0]:
                            weapons.append(gun)
                        if avt['name'] == i[0]:
                            weapons.append(avt)
                else:
                    if sum(list(map(lambda x: x[0], cur.execute('SELECT score FROM score').fetchall()))) >= i[2]:
                        res = 'Update weapon set able = "True" where weapon = "'
                        res += str(i[0]) + '"'
                        if i[0] not in weapons:
                            if gun['name'] == i[0]:
                                weapons.append(gun)
                            if avt['name'] == i[0]:
                                weapons.append(avt)
                        cur.execute(res)
    curwp = char.wpns.index(char.weapon)
    rate = 1
    trpim = Trap.image
    trpdcn = 3
    trpcn = 3
    char.wpns = weapons
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
        screen.fill((0, 0, 90))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                res = "insert into score values (" + str(set_id()) + ", " + str(char.scr) + ", 1)"
                cur.execute(res)
                con.commit()
                running = False
                return
            if event.type == pygame.MOUSEMOTION:
                mousepos = event.pos
            if event.type == pygame.MOUSEWHEEL:
                curwp = char.wpns.index(char.weapon)
                if event.y == 1:
                    curwp += 1
                    if curwp == len(char.wpns):
                        curwp = 0
                char.weapon = char.wpns[curwp]
                wpimg = char.weapon['img']
            if event.type == pygame.KEYDOWN:
                if event.key == 27:
                    res = "insert into score values (" + str(set_id()) + ", " + str(char.scr) + ", 1)"
                    cur.execute(res)
                    con.commit()
                    running = False
                    main_menu()
                    return
                if event.key == 115:
                    char.weapon = gun
                if event.key == 116:
                    if trpslc < 1:
                        trpslc += 1
                        trpim = Trap.image2
                    else:
                        trpslc = 0
                        trpim = Trap.image
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
                    if trpslc == 0:
                        if trpcn > 0:
                            Trap(trp, char.rect.centerx, char.rect.centery, 0)
                            trpcn -= 1
                    else:
                        if trpdcn > 0:
                            Trap(trpd, char.rect.centerx, char.rect.centery, 1)
                            trpdcn -= 1
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
            Enemy(enms, random.randint(200, 800), 800, 2, 5, 50)
            Enemy(enms, random.randint(200, 800), 0, 3, 3, 40)
            Enemy(enms, 0, random.randint(100, 700), 5, 2, 30)
            if rate > fps * 2:
                Enemy(enms, 1000, random.randint(200, 800), 2, 4, 45)

            if rate < fps * 4:
                rate += 5
            else:
                Enemy(enms, 0, random.randint(200, 800), 2, 4, 45)

            enm_spawn = fps * 8 - rate
        else:
            enm_spawn -= 1
        trpd.draw(screen)
        trp.draw(screen)
        enms.draw(screen)
        blts.draw(screen)
        chr.draw(screen)
        trpd.update()
        trp.update()
        enms.update()
        chr.update()
        blts.update()
        screen.blit(load_image(wpimg), (830, 50))
        screen.blit(trpim, (900, 50))
        blic = pygame.transform.scale(load_image('bulleticon.png'), (40, 76))
        blic.set_alpha((255 // char.weapon['blmax']) * char.weapon['bult'])
        hpic = pygame.transform.scale(load_image('hp.png'), (60, 60))
        hpic.set_alpha((255 // 10) * char.hp)
        font = pygame.font.SysFont('Impact', 35)
        if char.weapon['nxtrld']:
            rldtm = font.render(str(int(char.weapon['nxtrld'] / 60 * 10) / 10), True, pygame.Color('white'))
            screen.blit(rldtm, (905, 660))
        if trpslc == 1:
            trcn = font.render(str(trpdcn), True, pygame.Color('white'))
        else:
            trcn = font.render(str(trpcn), True, pygame.Color('white'))
        if trp_spawn > 0:
            trp_spawn -= 1
        else:
            if trpdcn < 10:
                trpdcn += 1
            if trpcn < 10:
                trpcn += 1
            trp_spawn = fps * 4
        screen.blit(trcn, (930, 50))
        screen.blit(blic, (900, 650))
        screen.blit(hpic, (830, 650))
        if char.hp < 1:
            res = "insert into score values (" + str(set_id()) + ", " + str(char.scr) + ", 1)"
            cur.execute(res)
            con.commit()
            start_screen()
            running = False
            return
        pygame.display.flip()
        cl.tick(60)


def lvl2():
    global yd
    global yu
    global xr
    global xl
    global mousepos
    global trpslc
    for i in enms:
        i.kill()
    for i in blts:
        i.kill()
    char.rect.center = width // 2, height // 2
    for i in trp:
        i.kill()
    char.hp = 10
    enms.clear(screen, screen)
    running = True
    enm_spawn = fps * 8
    trp_spawn = fps * 7
    wpimg = char.weapon['img']
    wpns = ['Gun', 'Avt', 'Shotgun']
    for i in cur.execute('SELECT * FROM weapon').fetchall():
        for j in wpns:
            if i[0] == j:
                if i[1] == 'True':
                    if i[0] not in weapons:
                        if gun['name'] == i[0]:
                            weapons.append(gun)
                        if avt['name'] == i[0]:
                            weapons.append(avt)
                else:
                    if sum(list(map(lambda x: x[0], cur.execute('SELECT score FROM score').fetchall()))) >= i[2]:
                        res = 'Update weapon set able = "True" where weapon = "'
                        res += str(i[0]) + '"'
                        if i[0] not in weapons:
                            if gun['name'] == i[0]:
                                weapons.append(gun)
                            if avt['name'] == i[0]:
                                weapons.append(avt)
                        cur.execute(res)
    curwp = char.wpns.index(char.weapon)
    rate = 1
    trpim = Trap.image
    trpdcn = 3
    trpcn = 3
    char.wpns = weapons
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
        screen.fill((30, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                res = "insert into score values (" + str(set_id()) + ", " + str(char.scr) + ", 2)"
                cur.execute(res)
                con.commit()
                running = False
                return
            if event.type == pygame.MOUSEMOTION:
                mousepos = event.pos
            if event.type == pygame.MOUSEWHEEL:
                curwp = char.wpns.index(char.weapon)
                if event.y == 1:
                    curwp += 1
                    if curwp == len(char.wpns):
                        curwp = 0
                char.weapon = char.wpns[curwp]
                wpimg = char.weapon['img']
            if event.type == pygame.KEYDOWN:
                if event.key == 27:
                    res = "insert into score values (" + str(set_id()) + ", " + str(char.scr) + ", 2)"
                    cur.execute(res)
                    con.commit()
                    running = False
                    main_menu()
                    return
                if event.key == 115:
                    char.weapon = gun
                if event.key == 116:
                    if trpslc < 1:
                        trpslc += 1
                        trpim = Trap.image2
                    else:
                        trpslc = 0
                        trpim = Trap.image
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
                    if trpslc == 0:
                        if trpcn > 0:
                            Trap(trp, char.rect.centerx, char.rect.centery, 0)
                            trpcn -= 1
                    else:
                        if trpdcn > 0:
                            Trap(trpd, char.rect.centerx, char.rect.centery, 1)
                            trpdcn -= 1
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
            Enemy(enms, random.randint(200, 800), 800, 2, 5, 50)
            Enemy(enms, random.randint(200, 800), 0, 5, 2, 30)
            Enemy(enms, 0, random.randint(100, 700), 5, 2, 30)
            Enemy(enms, 1000, random.randint(200, 800), 5, 2, 30)
            if rate > fps * 2:
                Enemy(enms, 1000, random.randint(200, 800), 5, 2, 30)

            if rate < fps * 4:
                rate += 5
            else:
                Enemy(enms, 0, random.randint(200, 800), 5, 2, 30)

            enm_spawn = fps * 8 - rate
        else:
            enm_spawn -= 1
        trpd.draw(screen)
        trp.draw(screen)
        enms.draw(screen)
        blts.draw(screen)
        chr.draw(screen)
        trpd.update()
        trp.update()
        enms.update()
        chr.update()
        blts.update()
        screen.blit(load_image(wpimg), (830, 50))
        screen.blit(trpim, (900, 50))
        blic = pygame.transform.scale(load_image('bulleticon.png'), (40, 76))
        blic.set_alpha((255 // char.weapon['blmax']) * char.weapon['bult'])
        hpic = pygame.transform.scale(load_image('hp.png'), (60, 60))
        hpic.set_alpha((255 // 10) * char.hp)
        font = pygame.font.SysFont('Impact', 35)
        if char.weapon['nxtrld']:
            rldtm = font.render(str(int(char.weapon['nxtrld'] / 60 * 10) / 10), True, pygame.Color('white'))
            screen.blit(rldtm, (905, 660))
        if trpslc == 1:
            trcn = font.render(str(trpdcn), True, pygame.Color('white'))
        else:
            trcn = font.render(str(trpcn), True, pygame.Color('white'))
        if trp_spawn > 0:
            trp_spawn -= 1
        else:
            if trpdcn < 10:
                trpdcn += 1
            if trpcn < 10:
                trpcn += 1
            trp_spawn = fps * 4
        screen.blit(trcn, (930, 50))
        screen.blit(blic, (900, 650))
        screen.blit(hpic, (830, 650))
        if char.hp < 1:
            res = "insert into score values (" + str(set_id()) + ", " + str(char.scr) + ", 2)"
            cur.execute(res)
            con.commit()
            start_screen()
            running = False
            return
        pygame.display.flip()
        cl.tick(60)


def weaponry():
    fon = pygame.transform.scale(load_image('grass.png'), (width, height))
    while True:
        wpns = ['Gun', 'Avt']
        screen.blit(fon, (0, 0))
        if len(cur.execute('SELECT score FROM score').fetchall()):
            lvl1scr = "Всего баллов: " + str(
                sum(list(map(lambda x: x[0], cur.execute('SELECT score FROM score').fetchall()))))
        else:
            lvl1scr = 'Всего баллов: 0'
        font = pygame.font.SysFont('Impact', 30)
        string_rendered = font.render(lvl1scr, True, pygame.Color('white'))
        screen.blit(string_rendered, (50, 50))
        string_rendered = font.render('Пистолет', True, pygame.Color('white'))
        screen.blit(string_rendered, (50, 150))
        string_rendered = font.render('Автомат', True, pygame.Color('white'))
        screen.blit(string_rendered, (50, 270))
        cord = 200
        for i in cur.execute('SELECT * FROM weapon').fetchall():
            for j in wpns:
                if i[0] == j:
                    if i[1] == 'True':
                        txt = 'Активно'
                        if i[0] not in weapons:
                            if gun['name'] == i[0]:
                                weapons.append(gun)
                            if avt['name'] == i[0]:
                                weapons.append(avt)
                    else:
                        txt = 'Необходимо ' + str(i[2]) + ' баллов'
                        if sum(list(map(lambda x: x[0], cur.execute('SELECT score FROM score').fetchall()))) >= i[2]:
                            res = 'Update weapon set able = "True" where weapon = "'
                            res += str(i[0]) + '"'
                            cur.execute(res)
                            txt = 'Активно'
                    string_rendered = font.render(txt, True, pygame.Color('white'))
                    screen.blit(string_rendered, (50, cord))
                    cord += 120
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == 27:
                    main_menu()
                    return
        pygame.display.flip()


def start_screen():
    intro_text = ["Bullet Time", "",
                  "Правила игры",
                  "Используйте ловушки или оружие для победы над врагами",
                  "Сложность увеличивается со временем",
                  "Убейте как можно больше врагов для получения баллов ",
                  "за которые откроются новые уровни и вооружение"]

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
    lvl2icon = pygame.transform.scale(load_image('lvl2.png'), (120, 180))
    lvl1_rect = (100, 300)
    lvl2_rect = (450, 300)
    screen.blit(lvl1icon, lvl1_rect)
    lvl_1 = False
    wapnry = False
    lvl_2 = False
    cr = str(sum(list(map(lambda x: x[0], cur.execute('SELECT score FROM score').fetchall()))))

    while True:
        screen.blit(fon, (0, 0))
        screen.blit(lvl1icon, lvl1_rect)
        screen.blit(lvl2icon, lvl2_rect)
        if len(cur.execute('SELECT score FROM score WHERE level = 1').fetchall()):
            lvl1scr = "Лучший рекорд: " + str(max(cur.execute('SELECT score FROM score WHERE level = 1').fetchall())[0])
        else:
            lvl1scr = 'Лучший рекорд: 0'
        if len(cur.execute('SELECT score FROM score WHERE level = 2').fetchall()):
            lvl2scr = "Лучший рекорд: " + str(max(cur.execute('SELECT score FROM score WHERE level = 2').fetchall())[0])
        else:
            lvl2scr = 'Лучший рекорд: 0'
        font = pygame.font.SysFont('Impact', 30)
        string_rendered = font.render(lvl1scr, True, pygame.Color('white'))
        screen.blit(string_rendered, (50, 250))
        string_rendered = font.render(lvl2scr, True, pygame.Color('white'))
        screen.blit(string_rendered, (400, 250))
        pygame.draw.rect(screen, (90, 150, 90), (width // 2 - 100, 600, 200, 80))
        string_rendered = font.render("Оружейная", True, pygame.Color('white'))
        screen.blit(string_rendered, (width // 2 - 75, 615))
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
                if int(cr) >= 20:
                    if (lvl2_rect[0] < event.pos[0] < lvl2icon.get_rect()[2] + lvl2_rect[0]) and (
                            lvl2_rect[1] < event.pos[1] < lvl2icon.get_rect()[3] + lvl2_rect[1]):
                        lvl2icon = pygame.transform.scale(load_image('lvl2hovered.png'), (120, 180))
                        lvl_2 = True
                    else:
                        lvl2icon = pygame.transform.scale(load_image('lvl2icon.png'), (120, 180))
                        lvl_2 = False
                if (width // 2 - 100 < event.pos[0] < 200 + width // 2 - 100) and (
                        600 < event.pos[1] < 80 + 600):
                    wapnry = True
                else:
                    wapnry = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if lvl_1:
                    lvl1()
                    return
                if lvl_2 and int(cr) > 20:
                    lvl2()
                    return
                if wapnry:
                    weaponry()
                    return
        pygame.display.flip()


start_screen()
pygame.quit()
