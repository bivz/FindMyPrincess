import pygame
import random

screenWidth = 800
screenHeight = 480
pygame.init()
win = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption('Find My Princess')
bg = pygame.image.load('bg.jpg')
char = pygame.image.load('standing.png')
p_image = pygame.image.load('Princess.png')
clock = pygame.time.Clock()
score = 0

bulletSound = pygame.mixer.Sound('bullet.wav')
hitSound = pygame.mixer.Sound('hit.wav')
win_clap = pygame.mixer.Sound('win_clap.wav')
yay = pygame.mixer.Sound('yay.wav')
loose = pygame.mixer.Sound('gameOver.wav')
music = pygame.mixer.music.load('happy.wav')
pygame.mixer.music.play((-1))



class Player(object):
    # Load Images
    walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'),
                 pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'),
                 pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]
    walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'),
                pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'),
                pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.left = False
        self.right = False
        self.standing = True
        self.walkCount = 0
        self.hitbox = (self.x + 18, self.y + 11, 29, 52)
        self.isJump = False
        self.jumpCount = 10
        self.health = 10
        self.visible = True

    def draw(self, win):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0
        if not self.standing:
            if self.left:
                win.blit(self.walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1

            elif self.right:
                win.blit(self.walkRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
        else:
            if self.right:
                win.blit(self.walkRight[0], (self.x, self.y))
            else:
                win.blit(self.walkLeft[0], (self.x, self.y))

        pygame.draw.rect(win, (255, 0, 0), (self.hitbox[0]-10, self.hitbox[1] - 10, 50, 5))
        pygame.draw.rect(win, (0, 255, 255),
                         (self.hitbox[0]-10, self.hitbox[1] - 10, 50 - ((50 / 10) * (10 - abs(score+10))), 5))

        self.hitbox = (self.x + 18, self.y + 11, 29, 52)
        # pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

    def hit(self):
        if self.health > 0:
            self.health -= 1
        else:
            self.visible = False


class Princess:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.hitbox = (self.x + 12, self.y + 11, 29, 72)
        self.isFalling = False
        self.onGround = False

    def draw(self, win):
        win.blit(p_image, (self.x, self.y))
        self.hitbox = (self.x+12, self.y+11, 25, 40)
        #pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

    def fall(self):
        if self.isFalling and self.y < 400:
            self.y += 5
        else:
            self.isFalling = False

    def hit(self):
        self.x = random.randint(5, screenWidth - 65)
        self.y = random.randint(65, screenHeight - 400)


class Projectile(object):
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 5 * facing

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)


class Enemy(object):
    walkRight = [pygame.image.load('R1E.png'), pygame.image.load('R2E.png'), pygame.image.load('R3E.png'),
                 pygame.image.load('R4E.png'), pygame.image.load('R5E.png'), pygame.image.load('R6E.png'),
                 pygame.image.load('R7E.png'), pygame.image.load('R8E.png'), pygame.image.load('R9E.png'),
                 pygame.image.load('R10E.png'), pygame.image.load('R11E.png')]
    walkLeft = [pygame.image.load('L1E.png'), pygame.image.load('L2E.png'), pygame.image.load('L3E.png'),
                pygame.image.load('L4E.png'), pygame.image.load('L5E.png'), pygame.image.load('L6E.png'),
                pygame.image.load('L7E.png'), pygame.image.load('L8E.png'), pygame.image.load('L9E.png'),
                pygame.image.load('L10E.png'), pygame.image.load('L11E.png')]

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x, self.end]
        self.walkCount = 0
        self.vel = 3
        self.hitbox = (self.x + 17, self.y+2, 31, 57)
        self.health = 10
        self.visible = True
        self.left = False
        self.right = False


    def draw(self, win):
        if self.visible:
            self.move()
            if self.walkCount + 1 >= 33:
                self.walkCount = 0

            if self.vel > 0:
                win.blit(self.walkRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
                self.right = True
                self.left = False
            else:
                win.blit(self.walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
                self.right = False
                self.left = True

            self.hitbox = (self.x + 17, self.y + 2, 31, 57)

    def move(self):
        if self.visible:
            if self.vel > 0:
                if self.x + self.vel < self.path[1]:
                    self.x += self.vel
                else:
                    self.vel = self.vel * -1
                    self.walkCount = 0
            else:
                if self.x - self.vel > self.path[0]:
                    self.x += self.vel
                else:
                    self.vel = self.vel * -1
                    self.walkCount = 0

    def hit(self):
        if self.health > 0:
            self.health -= 1
        else:
            self.visible = False


def drawgamewindow():
    pygame.display.update()
    win.blit(bg, (0, 0))
    text = font.render("Score: " + str(score), 1, (0,0,0))
    win.blit(text, (375, 10))
    man.draw(win)
    goblin.draw(win)
    princess.draw(win)
    for bullet in bullets:
        bullet.draw(win)


# Main Loop
font = pygame.font.SysFont('Sans', 30, True, True)
font_message = pygame.font.SysFont('Sans', 50, True)
man = Player(300, 410, 64, 64)
goblin = Enemy(100, 410, 64, 64, 450)
p_x = random.randint(5, screenWidth - 65)
p_y = random.randint(65, screenHeight - 360)
princess = Princess(p_x, p_y, 64, 64)
bullets = []
shootLoop = 0
pauseLogic = True


run = True

while run:
    rangen = random.randint(0, 10)
    keys = pygame.key.get_pressed()
    # Gaming Control Stuffs
    clock.tick(40)
    drawgamewindow()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Bullet Logic
    if shootLoop > 0:
        shootLoop += 1
        if shootLoop > 3:
            shootLoop = 0

    if shootLoop == 0 and rangen % 2 == 0:
        if goblin.left:
            facing = -1
        else:
            facing = 1
        if len(bullets) < 1:
            bullets.append(Projectile(round(goblin.x + goblin.width//2), round(goblin.y + goblin.height//2), 6, (0, 0, 0), facing))
            bulletSound.play()

        shootLoop = 1

    for bullet in bullets:
        if bullet.y - bullet.radius < man.hitbox[1] + man.hitbox[3] and bullet.y + bullet.radius > man.hitbox[1]:  # Bullet hit man condition
            if bullet.x + bullet.radius > man.hitbox[0] and bullet.x - bullet.radius < man.hitbox[0] + man.hitbox[2]:
                man.hit()
                hitSound.play()
                score -= 1
                bullets.pop(bullets.index(bullet))

        if bullet.x < 500 and bullet.x > 0:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))

    # Game Logic
    # Princess randomly Falling
    if rangen % 3 == 0:
        princess.isFalling = True
        princess.fall()

    # Check if Princess on ground
    if princess.y > screenHeight - 100:
        score -= 3
        loose.play()
        font_message = pygame.font.SysFont('Sans', 20)
        fall_text = font_message.render('I Fell on Ground !!', 1, (255, 0, 0))
        win.blit(fall_text, (princess.x-10, princess.y-20))
        pygame.display.update()
        pygame.time.delay(1500)
        princess.hit()

    # Princess being hit by man
    if man.hitbox[1]< princess.hitbox[1]+princess.hitbox[3] and man.hitbox[1]+man.hitbox[3] > princess.hitbox[1]:
        if man.hitbox[0] + man.hitbox[2] > princess.hitbox[0] and man.hitbox[0] < princess.hitbox[0] + princess.hitbox[2]:
            yay.play()
            font_message = pygame.font.SysFont('Sans', 20)
            fall_text = font_message.render('Thanks For Saving Me !!', 1, (0, 255, 0))
            win.blit(fall_text, (princess.x - 10, princess.y - 20))
            pygame.display.update()
            pygame.time.delay(1000)
            princess.hit()
            score += 1
    # Man being hit by goblin
    if man.hitbox[1] < goblin.hitbox[1] + goblin.hitbox[3] and man.hitbox[1] + man.hitbox[3] > goblin.hitbox[1]:
        if man.hitbox[0] + man.hitbox[2] > goblin.hitbox[0] and man.hitbox[0] < goblin.hitbox[0] + goblin.hitbox[2]:
            man.hit()
            # score -= 1

    # Keys Pressed Action
    if keys[pygame.K_LEFT] and man.x > man.vel:
        man.x -= man.vel
        man.left = True
        man.right = False
        man.standing = False

    elif keys[pygame.K_RIGHT] and man.x < screenWidth - man.width - man.vel:
        man.x += man.vel
        man.left = False
        man.right = True
        man.standing = False

#    elif keys[pygame.K_UP] and man.y > man.vel:
#        man.y -= man.vel
#
#    elif keys[pygame.K_DOWN] and man.y < screenHeight - man.height - man.vel:
#        man.y += man.vel
    else:
        man.standing = True
        man.walkCount = 0

    if not man.isJump:
        if keys[pygame.K_UP] or keys[pygame.K_SPACE]:
            man.isJump = True
            man.right = False
            man.left = False
            man.walkCount = 0

    else:
        if man.jumpCount >= -10:
            neg = 1
            if man.jumpCount < 0:
                neg = -1
            man.y -= (man.jumpCount ** 2) * 0.3 * neg
            man.jumpCount -= 1
        else:
            man.isJump = False
            man.jumpCount = 10

    # Game Win Loose Condition
    if score >= 10:
        font_message = pygame.font.SysFont('Sans', 100)
        fall_text = font_message.render('You Win  !!', 1, (0, 255, 0))
        win.blit(fall_text, ((screenWidth/2 - fall_text.get_width()/2), screenHeight/2))
        win_clap.play()
        pygame.display.update()
        paused = True
        while paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    paused = False
                    run = False

    elif score <= -10:
        font_message = pygame.font.SysFont('Sans', 100)
        fall_text = font_message.render('You Lose  !!', 1, (0, 0, 0))
        win.blit(fall_text, ((screenWidth / 2 - fall_text.get_width() / 2), screenHeight / 2))
        loose.play()
        pygame.display.update()
        paused = True
        while paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    paused = False
                    run = False

    pygame.display.update()

    while(pauseLogic):
        pygame.time.delay(2000)
        pauseLogic = False

pygame.quit()
quit()
