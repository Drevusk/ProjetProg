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
gameOverSound = pygame.mixer.Sound('gameover.wav')
pygame.mixer.music.load('background.mid')

# Set up images.

playerImage = pygame.image.load('perenoel.jpeg')
playerRect = playerImage.get_rect()
baddieImage = pygame.image.load('pinguin.jpeg')
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
        #self.image = pygame.transform.scale(playerImage,(50,40)) #to scale down the our image
        self.image = playerImage
        #self.image.set_colorkey(WHITE) #to remove the white on the boarder of the image
        self.rect = self.image.get_rect()
        self.rect.centerx = WINDOWWIDTH -700
        self.rect.bottom = WINDOWHEIGHT / 2
        self.speedx = 0
        self.speedy = 0
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


#class of the ennemies
class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(baddieImage,(50,40))
        #self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.y = random.randrange(500) #random spawn on axe Y
        self.rect.x = (WINDOWWIDTH+100) #to get smooth animations, not that they spawn into existence at the right of the screen, instead they appear naturally from the extremity of the screen
        self.speedx = random.randrange(-8, -3) #random speed on X
        self.speedy = random.randrange(-3, 3)#random speed on Y
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
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)
#bullets = []

while True:
    # Set up the start of the game.
    score = 0
    playerRect.topleft = (WINDOWWIDTH -900, WINDOWHEIGHT / 2)
    moveLeft = moveRight = moveUp = moveDown = False
    pygame.mixer.music.play(-1, 0.0)
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
            m = Mob()
            all_sprites.add(m)
            mobs.add(m)



        #check to see if a mob hit the player
        hits = pygame.sprite.spritecollide(player, mobs, False) #if a mobs collide, it is stocked it the list "hits"
        if hits:
            terminate()

        #Draw everything
        windowSurface.blit(background,background_rect)
        all_sprites.draw(windowSurface)
        #after drawing everything, flip the display
        pygame.display.flip()

        # Draw the score and top score.
        drawText('Score: %s' % (score), font, windowSurface, 10, 0)
        drawText('Top Score: %s' % (topScore), font, windowSurface, 10, 40)


        mainClock.tick(FPS)

    # Stop the game and show the "Game Over" screen.
    pygame.mixer.music.stop()
    gameOverSound.play()

    drawText('GAME OVER', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
    drawText('Press a key to play again.', font, windowSurface, (WINDOWWIDTH / 3) - 80, (WINDOWHEIGHT / 3) + 50)
    pygame.display.update()
    waitForPlayerToPressKey()

    gameOverSound.stop()
