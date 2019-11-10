import pygame

pygame.init() # initialize py game

window = pygame.display.set_mode((500,500)) # surface, topleft is 0,0 , bottm right is 500,500

pygame.display.set_caption("Dragon Quest")
walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'), pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'), pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]
walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'), pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'), pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]
bg = pygame.image.load("background.jpg")
clock = pygame.time.Clock()

bullet_sound = pygame.mixer.Sound("pew.wav")
hit_sound = pygame.mixer.Sound("expl6.wav")

class player:
    def __init__(self,x,y,width,height):
        self.x = x # x determines horizontal positon
        self.y = y # y determines vertical position
        self.width = width
        self.height = height
        self.vel = 5
        self.isJump = False
        self.jumpCount = 10
        self.left = False
        self.right = False
        self.walkCount = 0
        self.standing = True
        self.hitbox = (self.x + 17, self.y + 11, 29, 52) # recatangle
        self.hp = 10
        self.visible = True

    def draw(self,window):
        if self.visible:
            if self.walkCount + 1 > 27:
                self.walkCount = 0

            if not self.standing:

                if self.left:
                    window.blit(walkLeft[self.walkCount//3],(self.x, self.y))
                    self.walkCount += 1

                elif self.right:
                    window.blit(walkRight[self.walkCount//3],(self.x, self.y))
                    self.walkCount += 1

            else:
                if self.right:
                    window.blit(walkRight[0], (self.x, self.y))

                else:
                    window.blit(walkLeft[0], (self.x, self.y))


                #window.blit(char,(self.x,self.y))
            self.hitbox = (self.x + 17, self.y + 11, 29, 52) # by having this line here
                                                        # it will move along with player
            pygame.draw.rect(window, (255, 0, 0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10)) # health bar
            pygame.draw.rect(window, (0, 128, 0), (self.hitbox[0], self.hitbox[1] - 20, 50 - (5 * (10 - self.hp)), 10))
            pygame.draw.rect(window,(250,0,0),self.hitbox,2) # hitbox (rectangle) shows up

        else:
            font2 = pygame.font.SysFont(None,100)
            text3 = font2.render("Game Over", 1, (250,0,0))
            window.blit(text3, (80, 200))

    def health(self):
        if self.hp > 0:
            self.hp -= 1
            hit_sound.play()
            i = 0
            while i < 300:
                pygame.time.delay(1)
                i += 1
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        i = 301
                        pygame.quit()

        else:
            self.visible = False

class projectile():
    def __init__(self,x,y,radius,color,facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing # why 8

    def draw(self,window):
        pygame.draw.circle(window, self.color, (self.x,self.y), self.radius)

class enemy():
    walkRight = [pygame.image.load('R1E.png'), pygame.image.load('R2E.png'), pygame.image.load('R3E.png'),
                 pygame.image.load('R4E.png'), pygame.image.load('R5E.png'), pygame.image.load('R6E.png'),
                 pygame.image.load('R7E.png'), pygame.image.load('R8E.png'), pygame.image.load('R9E.png'),
                 pygame.image.load('R10E.png'), pygame.image.load('R11E.png')]
    walkLeft = [pygame.image.load('L1E.png'), pygame.image.load('L2E.png'), pygame.image.load('L3E.png'),
                pygame.image.load('L4E.png'), pygame.image.load('L5E.png'), pygame.image.load('L6E.png'),
                pygame.image.load('L7E.png'), pygame.image.load('L8E.png'), pygame.image.load('L9E.png'),
                pygame.image.load('L10E.png'), pygame.image.load('L11E.png')]

    def __init__(self,x,y,width,height,end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x, self.end] # represents where it strats and where it ends
        self.walkCount = 0
        self.vel = 3 # why 3
        self.hitbox = (self.x + 17, self.y + 2, 31, 57)  # recatangle
        self.hp = 10
        self.visible = True # after defeated, should disappear
        self.jumpCount = 10


    def draw(self,window):
        self.move() # every time the ennemy moves, draw it
        if self.visible:

            if self.walkCount +1 >= 33:
                self.walkCount = 0

            if self.vel > 0: # moving to right
                window.blit(self.walkRight[self.walkCount //3], (self.x, self.y))
                self.walkCount +=1
            else:
                window.blit(self.walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1

            self.hitbox = (self.x + 17, self.y + 2, 31, 57)  # recatangle
            pygame.draw.rect(window, (255,0,0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
            pygame.draw.rect(window, (0, 128, 0), (self.hitbox[0], self.hitbox[1] - 20, 50 - (5 * (10 - self.hp)), 10)) # green

    def move(self):
        if self.vel > 0:
            if (self.x + self.vel) < self.path[1]: # as long as enemy is not off the screen,
                self.x += self.vel # move to the right

            else:
                self.vel = self.vel * -1 # by multplying it by negative -1, it will become negative and move towards to the left
                self.walkCount = 0

        else:
            if self.x - self.vel > self.path[0]: # as long as enemy is not off the screen, (left screen)
                self.x += self.vel

            else:
                self.vel = self.vel * -1 # -1 * -1 is 1 so starts moving towards to the right
                self.walkCount = 0

    def draw1(self,window):
        self.movefaster() # every time the ennemy moves, draw it
        if self.visible:

            if self.walkCount +1 >= 33:
                self.walkCount = 0

            if self.vel > 0: # moving to right
                window.blit(self.walkRight[self.walkCount //3], (self.x, self.y))
                self.walkCount +=1
            else:
                window.blit(self.walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1

            self.hitbox = (self.x + 17, self.y + 2, 31, 57)  # recatangle
            pygame.draw.rect(window, (255,0,0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
            pygame.draw.rect(window, (0, 128, 0), (self.hitbox[0], self.hitbox[1] - 20, 50 - (5 * (10 - self.hp)), 10)) # green
            # hp bar decrements by 5
            #pygame.draw.rect(window, (250, 0, 0), self.hitbox, 2)  # rectangle shows up

    def movefaster(self):

        if self.vel > 0:
            if (self.x + self.vel) < self.path[1]: # as long as enemy is not off the screen,
                self.x += self.vel * 2 # move faster

            else:
                self.vel = self.vel * -1 # by multplying it by negative -1, it will become negative and move towards to the left
                self.walkCount = 0

        else:
            # if self.x > 0: go all the way down to left edge
            if self.x - self.vel > self.path[0]: # as long as enemy is not off the screen, (left screen)
                self.x += self.vel * 2 # now self.vel is negative

            else:
                self.vel = self.vel * -1 # -1 * -1 is 1 so starts moving towards to the right
                self.walkCount = 0

    def hit(self):
        if self.hp > 1:
            self.hp -= 1
            hit_sound.play()

        else:
            self.visible = False

        print("King Kong aint got shit on me")

def redrawGamewindow():

    window.blit(bg,(0,0))# before moving rectangle, fills screen
    icon.draw(window)
    goblin.draw(window)
    goblin1.draw1(window)
    text = font.render("Score:" + str(hit_cnt), 1, (0,0,0))
    window.blit(text, (390,10))
    for bullet in bullets:
        bullet.draw(window)

    pygame.display.update() # by updating, everything will show up

def endScreen(hit_cnt):
    speed = 80 # reset speed
    run = True
    while run:
        pygame.time.delay(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False

        window.blit(bg, (0, 0))  # reset background
        largeFont = pygame.font.SysFont("comicsans", 80)
        pre_score = largeFont.render("Max Score: " + str(hit_cnt), 1, (255, 255, 255))
        window.blit(pre_score, (500 // 2 - pre_score.get_width() // 2, 200))
        pygame.display.update()

icon = player(0,410,64,64)
goblin = enemy(120,410,64,64,450)
goblin1 = enemy(120,410,64,64,450)
bullets = []
shootLoop = 0
#isHit = False
hit_cnt = 0
# how to display integer (hit_cnt) in the screen
#window.blit(str(hit_cnt),(840, 20))
font = pygame.font.Font(None,30)
font1 = pygame.font.Font(None,60)

# main loop checks for all the events such as collision and mouse events

run = True
while run:
    clock.tick(27)

    if goblin.visible:
        # collide player and goblin
        # when player collides with the top of goblin (jump and collide), it doesnt count
        if icon.hitbox[1] < goblin.hitbox[1] + goblin.hitbox[3] and icon.hitbox[1] > goblin.hitbox[1]:
            if icon.hitbox[0] + icon.hitbox[2] > goblin.hitbox[0] and icon.hitbox[0] < goblin.hitbox[0] + goblin.hitbox[2]:
                icon.health()

    if goblin1.visible:
        # player collides with goblin 1
        if icon.hitbox[1] < goblin1.hitbox[1] + goblin1.hitbox[3] and icon.hitbox[1] > goblin1.hitbox[1]:
            if icon.hitbox[0] + icon.hitbox[2] > goblin1.hitbox[0] and icon.hitbox[0] < goblin1.hitbox[0] + goblin1.hitbox[2]:
                icon.health()

    if shootLoop > 0:
        shootLoop += 1

    if shootLoop > 3:
        shootLoop = 0

    # check for the events/actions such as
    for event in pygame.event.get():
        # if the big red button at the top right hit, quits
        if event.type == pygame.QUIT:
            run = False

    for bullet in bullets:
        # goblin is hit
        if bullet.y - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3] and bullet.y + bullet.radius > goblin.hitbox[1]:
            if bullet.x + bullet.radius > goblin.hitbox[0] and bullet.x - bullet.radius < goblin.hitbox[0] + goblin.hitbox[2]:
                #isHit = True
                goblin.hit()
                hit_cnt += 1
                if bullet in bullets:
                    bullets.remove(bullet)

        # goblin 1 is hit
        if bullet.y - bullet.radius < goblin1.hitbox[1] + goblin1.hitbox[3] and bullet.y + bullet.radius > goblin1.hitbox[1]:
            if bullet.x + bullet.radius > goblin1.hitbox[0] and bullet.x - bullet.radius < goblin1.hitbox[0] + goblin1.hitbox[2]:
                goblin1.hit()
                hit_cnt += 1
                if bullet in bullets:
                    bullets.remove(bullet)
                    # ValueError: list.remove(x): x not in list


        if 0 < bullet.x < 500: # bullet not going off the screen
            bullet.x += bullet.vel

        else: # delete bullet
            bullets.remove(bullet)

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE] and shootLoop == 0:
        if icon.left:
            facing = -1
        else:
            facing = 1

        if len(bullets) < 5:
            bullets.append(projectile(round(icon.x + icon.width // 2), round(icon.y + icon.height//2),6,(0,0,0),facing))
            bullet_sound.play()
        shootLoop = 1

    if keys[pygame.K_LEFT] and icon.x > icon.vel:
        icon.x -= icon.vel # move towards left
        icon.left  = True
        icon.right = False
        icon.standing = False # as he is walking

        # 500 came from screen width and conrdinate is technically topleft so screenwidth - width of character
    elif keys[pygame.K_RIGHT] and icon.x < 500 - icon.width - icon.vel:
        icon.x += icon.vel # move towards right
        icon.left  = False
        icon.right = True
        icon.standing = False # as he is walking

    else:
        icon.standing = True
        icon.walkCount = 0

    if not icon.isJump: # when jumping, up and down are not allowed

        if keys[pygame.K_UP]: # jump
            icon.isJump = True
            icon.right = False
            icon.left = False
            icon.walkCount = 0

    else:
        if icon.jumpCount >= -10:
            neg = 1
            if icon.jumpCount < 0:
                neg = -1
            icon.y -= (icon.jumpCount ** 2) * 0.5 * neg
            icon.jumpCount -= 1

        else:
            icon.isJump = False
            icon.jumpCount = 10

    # goblin jumps
    if goblin.jumpCount >= -10:
        neg = 1
        if goblin.jumpCount < 0:
            neg = -1
        goblin.y -= (goblin.jumpCount ** 2) * 0.5 * neg
        goblin.jumpCount -= 1

    else:
        goblin.isJump = False
        goblin.jumpCount = 10

    if not goblin1.visible and not goblin.visible:
        endScreen(hit_cnt)

    redrawGamewindow() # update display every single second

pygame.quit()
