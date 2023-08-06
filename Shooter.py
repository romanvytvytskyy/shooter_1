from pygame import *
from random import randint
from time import time as timer

#!  pyistaller --onefile Shooter.py


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_speed, player_x, player_y, size_x, size_y):
        super().__init__()
        self.image = transform.scale(
            image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        mw.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()

        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        elif keys[K_RIGHT] and self.rect.x < win_width - 85:  
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet(img_bullet, 15, self.rect.centerx-7, self.rect.top, 14,20)
        bullets.add(bullet)
    
    
class Enemy(GameSprite):
    def update(self):
        self.rect.y +=self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80,win_width-80)
            self.rect.y = 0
            lost +=1
            
            
class Bullet(GameSprite):
    def update(self):
        self.rect.y-=self.speed
        if self.rect.bottom <= 0 :
            self.kill()

img_back = "galaxy.jpg"  # game background
img_hero = "rocket.png"  # player sprite
img_enemy = "ufo.png"  # enemy sprite
img_bullet = "bullet.png"  # bullet sprite
img_bullet_1 = transform.scale(image.load(img_bullet),(5, 10))  # bullet sprite
img_asteroid = "asteroid.png"  # asteroid sprite

win_width = 700
win_height = 500
display.set_caption("Shooter")
display.set_icon(image.load(img_hero))
mw = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))


# FONT 
font.init()
text_font1 = font.SysFont("Arial", 36)
text_font2 = font.SysFont("Arial", 60)


text_win = ['   YOU WIN!', 'BE READY TO', '!NEXT WAVE!'] #Зберігаємо потрібний текст в список
text_alien = ['ALIANS WIN!','  TRY AGAIN']

def show_level(text_list, text_color): #створюємо фунцію
    '''функція приймає текст у вигляді списку. 
    Кожен новий рядок це новий елемент списку. 
    Другий параметр це колір тексту для відображення (передається кортежем)
    ''' 
    for i in range(len(text_list)):
            mw.blit(text_font2.render(text_list[i], 1, text_color), (200, ((i+1)*80))) #рендеремо коженя рядок окремо

#music
volume_level = 0.5
mixer.init()
mixer.music.set_volume(volume_level)
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')
mixer.Sound.set_volume(fire_sound, volume_level)

player = Player("rocket.png", 5, 250, win_height-100, 80, 100)
monsters = sprite.Group()
asteroids = sprite.Group()
bullets = sprite.Group()

def spawner(n):
    for i in range(n):
        m = Enemy(img_enemy, randint(1,5), randint(80,win_width-80), 0, 80,50)
        monsters.add(m)
    for i in range(n//3):
        m = Enemy(img_asteroid, randint(1, 3), randint(
            80, win_width-80), 0, 80, 50)
        asteroids.add(m)
        


max_monsters = 6
spawner(max_monsters)
goal = 10
max_lost = 3
game = True
lost = 0
score = 0
finish = False
rel_time = False
num_fire = 0
life = 3

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type ==KEYDOWN:
            if e.key==K_SPACE :
                if num_fire < (3+(max_monsters//2)) and rel_time ==False:
                    num_fire +=1
                    fire_sound.play()
                    player.fire()
                    
                if num_fire >= (3+(max_monsters//2)) and rel_time == False:
                    last_time = timer()
                    rel_time = True
                
                
            if e.key == K_KP_PLUS and volume_level<1:
                volume_level  = round(volume_level + 0.1, 1)
                mixer.music.set_volume(volume_level)
                mixer.Sound.set_volume(fire_sound, volume_level)
            if e.key == K_KP_MINUS and volume_level > 0: 
                volume_level = round(volume_level - 0.1, 1)
                mixer.music.set_volume(volume_level)
                mixer.Sound.set_volume(fire_sound, volume_level)
                
            
    if not finish:
        mw.blit(background, (0,0))
        x = 20
        for i in range((3+(max_monsters//2))-num_fire):
            mw.blit(img_bullet_1, (x, win_height-50))
            x += 7
            
        text_score = text_font1.render("Рахунок: "+str(score), 1,(255,155,55))
        text_lose = text_font1.render("Пропущено: "+str(lost), 1,(255,155,55))
        v_level = text_font1.render("Гучність: "+str(int(volume_level*100)), 1, (255, 155, 55))
        mw.blit(text_score, (10,20))
        mw.blit(text_lose, (10,50))
        mw.blit(v_level, (10, 80))
        
        player.update()
        player.reset()
        monsters.update()
        monsters.draw(mw)
        asteroids.update()
        asteroids.draw(mw)
        bullets.update()
        bullets.draw(mw)
        
        if rel_time == True:
            now_time = timer()
            if now_time - last_time < 3:
                mw.blit(text_font1.render("Wait!!! reloading...", 1, (150,0,0)), (260,450))
            else:
                num_fire = 0
                rel_time = False
                
        
        
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for collide in collides:
            score +=1
            m = Enemy(img_enemy, randint(1, 5), randint(
                80, win_width-80), 0, 80, 50)
            monsters.add(m)
            
        if (sprite.spritecollide(player, monsters, False) or 
            sprite.spritecollide(player, asteroids, False)):
            sprite.spritecollide(player, monsters, True)
            sprite.spritecollide(player, asteroids, True)
            life -=1
        
        if life == 0 or lost >= max_lost:
            finish = True
            if max_monsters >2:
                max_monsters -=1
            mw.fill((255,255,255))
            show_level(text_alien, (178, 0, 0))
        
        if life == 3:
            life_color = (0,150,0)
        if life == 2:
            life_color = (150,150,0)
        if life == 1:
            life_color = (150,0,0)
            
        mw.blit(text_font2.render(str(life),1,life_color), (650,10))
            
            
        if score >= goal:
            finish = True
            max_monsters +=1
            mw.fill((255,255,255))
            show_level(text_win, (29, 82, 11))

            
        display.update()
    else:
        finish = False
        score = 0
        lost = 0
        rel_time= False
        num_fire = 0
        life = 3
        for bullet in bullets:
            bullet.kill()
        for monster in monsters:
            monster.kill()
        for asteroid in asteroids:
            asteroid.kill()
        time.delay(3000)
        spawner(max_monsters)
        
    time.delay(50)