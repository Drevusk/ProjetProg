#set up all the sounds
#text press a key to retry

import pygame, random, sys
from pygame.locals import *

WINDOWWIDTH=800
WINDOWHEIGHT=450
TEXTCOLOR = (0, 0, 0)
BACKGROUNDCOLOR=(255,255,255)
FPS = 60
BADDIEMINSIZE = 10
BADDIEMAXSIZE = 40
BADDIEMINSPEED = 1
BADDIEMAXSPEED = 8
ADDNEWBADDIERATE = 6
PLAYERMOVERATE = 5
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255, 0, 0)
GREEN = (0, 100, 0)
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

def terminate():
    pygame.quit()
    sys.exit()

def waitForPlayerToPressKey():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: # Pressing ESC quits.
                    terminate()
                return



def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def newmob():
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

def draw_life(surface, x, y, pct):
    if pct < 0:
        pct = 0 #so we don't have negativ value for life
    BAR_LENGTH = 100
    BAR_HEIGHT = 10 #size of the bar
    fill = (pct / 100) * BAR_LENGTH
    outline_rectangle = pygame.Rect (x, y, BAR_LENGTH, BAR_HEIGHT) #the rectangle that doesn't change
    fill_rectangle2 = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)#so we can see the ammount of life we lost
    fill_rectangle = pygame.Rect (x, y, fill, BAR_HEIGHT) #the rectangle that display the life, it goes smaller when we get hit
    pygame.draw.rect(surface, RED, fill_rectangle2)  # draw the life lost
    pygame.draw.rect(surface, GREEN, fill_rectangle) #draw the life rectangle
    pygame.draw.rect(surface, WHITE, outline_rectangle, 2) #draw outline_rectangle

# Set up pygame, the window, and the mouse cursor.
pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Dodger')
pygame.mouse.set_visible(False)

# Set up the fonts.
font = pygame.font.SysFont(None, 48)
font2= pygame.font.SysFont("Courier",75)

# Set up sounds.
pygame.mixer.music.load('background.mid')
#pygame.mixer.music.set_volume(0.4) #change the volume of the music

#shoot_sound = pygame.mixer.Sound('shoot.wave')
#explosion_sound = pygame.mixer.Sound('Explosion.wav')
#death_sound = pygame.mixer.Sound('Death.wav')


# Set up images.

playerImage = pygame.image.load('perenoel.png')
playerRect = playerImage.get_rect()
baddieImage = []
baddie_list = ['pinguin.png', 'pinguin2.jpg', 'pinguin3.png'] #all the images we want to chose from
for img in baddie_list:
    baddieImage.append(pygame.image.load(img))
background = pygame.image.load("background.png")
background_rect = background.get_rect() #to have a way to locate it
bulletImage = pygame.image.load("gift.png")


# Show the "Start" screen.
windowSurface.fill(BACKGROUNDCOLOR)
drawText('Santawars', font2, windowSurface, (WINDOWWIDTH / 3.5), (WINDOWHEIGHT / 3))
drawText('Press a key to start.', font, windowSurface, (WINDOWWIDTH / 2.68) - 50, (WINDOWHEIGHT / 3) + 200)
pygame.display.update()
waitForPlayerToPressKey()

topScore = 0
#player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(playerImage,(150 ,80)) #to scale down our image
        #self.image = playerImage
        self.image.set_colorkey(BLACK) #to remove the white on the border of the image
        self.rect = self.image.get_rect()
        #self.radius = 60 #we can chose this way the size of the circle of the player's hitboxe
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius) #this line serve to display how big the circle is, but we don't need it in the final game, only to test
        self.rect.centerx = WINDOWWIDTH -700
        self.rect.bottom = WINDOWHEIGHT / 2
        self.speedx = 0
        self.speedy = 0
        self.life = 100 #setup life so we don't get oneshoted everytime we get hit

    #update the player sprite
    def update(self):
        self.speedx = 0
        self.speedy = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.speedy = 0
            self.speedx = -8
        if keys[pygame.K_RIGHT]:
            self.speedy = 0
            self.speedx = 8
        if keys[pygame.K_UP]:
            self.speedx = 0
            self.speedy = -8
        if keys[pygame.K_DOWN]:
            self.speedx = 0
            self.speedy = 8
        if self.rect.right > WINDOWWIDTH:
            self.rect.right = WINDOWWIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > WINDOWHEIGHT:
            self.rect.bottom = WINDOWHEIGHT
        self.rect.x += self.speedx
        self.rect.y += self.speedy




    #allow the player to shoot
    def shoot(self):
        bullet = Bullet(self.rect.right, self.rect.centery) #do the bullet spawn at the center extremity of the player
        all_sprites.add(bullet)
        bullets.add(bullet)
        #shoot_sound.play()


#class of the ennemies
class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = random.choice(baddieImage)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 20 #same as player
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius) #same as player
        self.rect.y = random.randrange(500) #random spawn on axe Y
        self.rect.x = (WINDOWWIDTH+100) #to get smooth animations, not that they spawn into existence at the right of the screen, instead they appear naturally from the extremity of the screen
        self.speedx = random.randrange(-8, -3) #random speed on X
        self.speedy = random.randrange(-3, 3)#random speed on Y
        self.rotation = 0 #to choose how much the sprite rotates, initially it doesnt

    #update the ennemies sprite
    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top < 0: #if an ennemi hits a extermity of the screen it bounces and continue his trajectory instead of being stuck to the extremity
            self.rect.top = 0
            self.speedy = -self.speedy
        if self.rect.bottom > WINDOWHEIGHT:
            self.rect.bottom = WINDOWHEIGHT
            self.speedy = -self.speedy
        if self.rect.left < -25:
            self.rect.y = random.randrange(500)
            self.rect.x = (WINDOWWIDTH+100)
            self.speedx = random.randrange(-8, -3)
            self.speedy = random.randrange(-3, 3)

#class of the bullet
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(bulletImage,(40,40))
        #self.image.set.colorkey(255,255,255)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedx= 10
    #update bullet sprite
    def update(self):
        self.rect.x += self.speedx
        #kill it if it moves off the screen
        if self.rect.right > WINDOWWIDTH:
            self.kill() #remove completly the sprite if it goes of the screen

all_sprites = pygame.sprite.Group() #all the sprites are there so they can be drawn and updated
mobs = pygame.sprite.Group() #we make them all the ennemies in the same group so it's easier to work with the them (hitboxes...)
bullets = pygame.sprite.Group() #same but for the bullets
player = Player()
all_sprites.add(player)

for i in range(8): #spawn a specific number of mobs on the screen
    newmob()

pygame.mixer.music.play(-1, 0.0) #start the music before the start of the game
while True:
    # Set up the start of the game.
    score = 0
    playerRect.topleft = (WINDOWWIDTH -900, WINDOWHEIGHT / 2)
    moveLeft = moveRight = moveUp = moveDown = False
    #so the game keeps running at the right speed
    clock.tick(FPS)
    while True: # The game loop runs while the game part is playing.
        score += 1 # Increase score.

        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            if event.type == pygame.KEYDOWN: #when you press the key it does something, not when you release the key
                if event.key == pygame.K_ESCAPE:
                    terminate()
                if event.key == pygame.K_SPACE:
                    player.shoot()



        #Update the sprites
        all_sprites.update()

        #check to see if a bullethit a mob
        hits = pygame.sprite.groupcollide(mobs, bullets, True, True) #if a bullet hit a mobs, both get deleted
        for hit in hits: #we have to add new mobs for each mobs that got deleted from the game
            score += 20
            #explosion_sound.play()
            newmob()


        #check to see if a mob hit the player
        hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle) #if a mobs collide, it is stocked it the list "hits", the last element allow us to use the circle of the hitboxes we made in classes
        for hit in hits:
            player.life -= 40 #we lose life when we get hit
            newmob()
            if player.life <= 0:
                #death_sound.play()
                terminate()

        #Draw everything
        windowSurface.blit(background,background_rect)
        all_sprites.draw(windowSurface)
        drawText('Score: %s' % (score), font, windowSurface, 10, 0)
        drawText('Top Score: %s' % (topScore), font, windowSurface, 10, 40)
        draw_life(screen, 5,5,player.life) #draw the life bar
        #after drawing everything, flip the display
        pygame.display.flip()
        mainClock.tick(FPS)

    # Stop the game and show the "Game Over" screen.
    pygame.mixer.music.stop()
    gameOverSound.play()

    drawText('GAME OVER', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
    drawText('Press a key to play again.', font, windowSurface, (WINDOWWIDTH / 3) - 80, (WINDOWHEIGHT / 3) + 50)
    pygame.display.update()
    waitForPlayerToPressKey()

    gameOverSound.stop()
