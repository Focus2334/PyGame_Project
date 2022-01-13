import os
import sys
import pygame
import math

pygame.init()
size = width, height = 1000, 1000
screen = pygame.display.set_mode(size)
cl = pygame.time.Clock()
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


class Car(pygame.sprite.Sprite):
    image = load_image("mar.png")

    def __init__(self, *gr):
        super().__init__(*gr)
        self.image = Car.image
        self.image1 = Car.image
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
        ad = event
        self.move()
        self.image = pygame.transform.rotate(self.image1, int(math.degrees(self.rot)) + 90)


running = True
cars = pygame.sprite.Group()
Car(cars)
while running:
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
    cars.draw(screen)
    cars.update()
    pygame.display.flip()
    cl.tick(60)
pygame.quit()
