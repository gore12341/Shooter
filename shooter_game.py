
from random import randint
from pygame import *
import pygame
pygame.init()
patrons = 5
life = 3
lost = 0
score = 0
finish = False
speed = 2
win_height = 500
win_width = 700
font.init()
window = display.set_mode((win_width, win_height))
display.set_caption('Шутер')
background = transform.scale(image.load('galaxy2.jpg'),(700,500))
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y  
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -=self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx-7, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

class Bullet(GameSprite):
    def update(self):
        self.rect.y +=self.speed
        if self.rect.y < 0:
            self.kill()
class Enemy(GameSprite):
    def update(self):
        self.rect.y +=self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost+=1
player = Player('rocket.png', 5, win_height - 100, 80, 100, 6)
monsters = sprite.Group()
bullets = sprite.Group()
asteroids = sprite.Group()
for i in range(1,5):
    monster = Enemy('ufo.png', randint(80, win_width - 80), 0, 70, 50, randint(1,3))
    monsters.add(monster)
for i in range(1,3):
    asteroid = Enemy('asteroid.png', randint(30, win_width-30), -40, 80, 50, randint(1,3))
    asteroids.add(asteroid)
FPS = 60
font = font.SysFont(None, 40)
text3 = font.render(f'Ты победил!', True, (255,255,255))
text7 = font.render(f'Перезарядись!', True, (255,0,0))
text8 = font.render(f'XP:{life}', True, (255,0,0))
text4 = font.render(f'Ты проиграл!', True, (255,255,255))
clock = time.Clock()
game = True
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if patrons != 0:
                    player.fire()
                    patrons-=1
            if e.key == K_r:
                if patrons ==0:
                    for i in range(5):
                        pygame.time.wait(100)
                        patrons+=1
    if not finish:
        window.blit(background, (0, 0))
        asteroids.update()
        asteroids.draw(window)
        monsters.update()
        monsters.draw(window)
        bullets.update()
        bullets.draw(window)
        player.reset()
        player.update()
        text6 = font.render(f'Патроны: {patrons}', True, (255,255,255))
        text = font.render(f'Пропущено: {lost}', True, (255,255,255))
        window.blit(text,(0,0))
        window.blit(text6,(0,58))
        window.blit(text8,(630,0))
        text2 = font.render(f'Счёт: {score}', True, (255,255,255))
        window.blit(text2,(0,30))
        collides = sprite.groupcollide(bullets, monsters, True, True)
        if life == 3:
            text8 = font.render(f'XP:{life}', True, (0,255,0))
        if life == 2:
            text8 = font.render(f'XP:{life}', True, (255,255,0))
        if life == 1:
            text8 = font.render(f'XP:{life}', True, (255,0,0))
        if life == 0:
            text8 = font.render(f'XP:{life}', True, (255,0,0))
        if patrons == 0:
            window.blit(text7,(0,88))
        for c in collides:
            monster = Enemy('ufo.png', randint(80, win_width - 80), 0, 70, 50, randint(1,3))
            monsters.add(monster)
            score+=1
        for monster in monsters:
            if player.rect.colliderect(monster):
                monster.rect.y=0
                life-=1
        for bullet in bullets:
            if sprite.groupcollide(asteroids, bullets, False, True):
                print('')
        if score >= 10:
            window.blit(text3,(250, 250))
            finish = True
        if lost >= 10:
            window.blit(text4,(250, 250))
            finish = True
        if life <= 0:
            window.blit(text4,(250, 250))
            finish = True
    else:
        life = 3
        patrons = 5
        lost = 0
        score = 0
        for m in monsters:
            m.kill()
        for b in bullets:
            b.kill()
        for a in asteroids:
            a.kill()
        for i in range(1,5):
            monster = Enemy('ufo.png', randint(80, win_width - 80), 0, 70, 50, randint(1,3))
            monsters.add(monster)
        for i in range(1,3):
            asteroid = Enemy('asteroid.png', randint(30, win_width-30), -40, 80, 50, randint(1,3))
            asteroids.add(asteroid)
        player.rect.x = win_height-100
        pygame.time.wait(3000)
        finish=False
    display.update()
    clock.tick(FPS)