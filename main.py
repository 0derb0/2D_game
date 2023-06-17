import pygame
from random import randint


class Turret(pygame.sprite.Sprite):
    def __init__(self, path, x, y, flip, velocity): #, cage_count, cd_time
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(path)
        self.image = pygame.transform.flip(self.image, flip, False)
        self.image = pygame.transform.scale(self.image, (200, 200))

        self.position_x = x
        self.position_y = y

        self.velocity = velocity

        self.rect = self.image.get_rect(center=(x, y))

        # self.cage_count = cage_count
        # self.cage_count_const = cage_count
        # self.cd_time = cd_time
        #
        # self.key = pygame.key.get_pressed()

    def move(self, up, down):
        key = pygame.key.get_pressed()
        if key[up]:
            self.position_y -= self.velocity
        if key[down]:
            self.position_y += self.velocity

        self.rect.center = [self.position_x, self.position_y]

    # def reload(self, reload_key):
    #     key = pygame.key.get_pressed()
    #     if self.cage_count <= 0 or key[reload_key]:
    #         self.cd_time -= 1
    #         if self.cd_time <= 0:
    #             self.cage_count = self.cage_count_const


class Bullet(pygame.sprite.Sprite):
    def __init__(self, path, x, y, speed):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(path)
        self.image = pygame.transform.scale(self.image, (30, 30))

        self.position_x = x
        self.position_y = y

        self.speed = speed

        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        self.rect.x += self.speed


class Robot(pygame.sprite.Sprite):
    def __init__(self, path, x, y, speed):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(path)
        self.image = pygame.transform.scale(self.image, (100, 100))

        self.position_x = x
        self.position_y = y

        self.rect = self.image.get_rect(center=(x, y))

        self.speed = speed

    def update(self):
        self.rect.x -= self.speed


class RedLine(pygame.sprite.Sprite):
    def __init__(self, path, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(path)
        self.image = pygame.transform.scale(self.image, (5, screen_height))

        self.position_x = x
        self.position_y = y

        self.rect = self.image.get_rect(topleft=(x, y))


pygame.init()

fps = 100
clock = pygame.time.Clock()

screen_width = 1500
screen_height = 800

screen = pygame.display.set_mode(size=(screen_width, screen_height))
pygame.display.set_caption('UwU')
icon = pygame.image.load('img/icon1.png')
pygame.display.set_icon(icon)

# score and life draw
score = 0
life = 10

font = pygame.font.Font(None, 36)

current_time = 0
robot_group = pygame.sprite.Group()
robot1 = Robot('img/robot_11.png', screen_width, screen_height/3, 5)
robot1_time = 105
robot2 = Robot('img/robot_2.png', x=screen_width, y=screen_height/2, speed=5)
robot2_time = 125

gun = Turret(path='img/gun1.png', x=100, y=screen_height/2, flip=True, velocity=8) # , cage_count=30, cd_time=4

red_line = RedLine('img/1.png', screen_width/5, 0)

bullet_group = pygame.sprite.Group()

gun_group = pygame.sprite.GroupSingle(gun)
red_group = pygame.sprite.GroupSingle(red_line)

reloading = False
cage_count_const = 30
cage_count = 30
cd_time_const = 90
cd_time = 90


run = True
while run:
    key = pygame.key.get_pressed()

    clock.tick(fps)
    screen.fill((200, 162, 200))
    score_text = font.render(f'Score: {score}', True, (180, 0, 0))
    life_text = font.render(f'{life} lifes', True, (180, 0, 0))
    cage_count_text = font.render(f'{cage_count} bullets', True, (180, 0, 0))
    # screen.blit(score_text, (60, 60))
    # screen.blit(life_text, (60, 100))
    # screen.blit(cage_count_text, (60, 140))

    for e in pygame.event.get():
        key = pygame.key.get_pressed()
        if e.type == pygame.QUIT:
            run = False

        if e.type == pygame.KEYDOWN:
            if key[pygame.K_SPACE] and reloading == False:
                x = gun.rect.x + 110
                y = gun.rect.y + 35
                bullet_group.add(Bullet('img/bomb.png', x, y, speed=50))
                cage_count -= 1
                if cage_count <= 0:
                    reloading = True

    if (key[pygame.K_r]) or reloading == True:
        reloading = True
        cd_time -= 1
        screen.blit(cage_count_text, (60, 140))
        if cd_time <= 0:
            cage_count = cage_count_const
            cd_time = cd_time_const
            screen.blit(cage_count_text, (60, 140))
            reloading = False

    screen.blit(score_text, (60, 60))
    screen.blit(life_text, (60, 100))
    screen.blit(cage_count_text, (60, 140))

    if current_time >= robot1_time:
        robot_group.add(Robot('img/robot_11.png', screen_width, randint(20, screen_height - 30), 2))
        robot1_time += 105
    if current_time >= robot2_time:
        robot_group.add(Robot('img/robot_2.png', x=screen_width, y=randint(20, screen_height - 30), speed=2))
        robot2_time += 125

    gun.move(pygame.K_w, pygame.K_s)
    if gun.position_y > screen_height:
        gun.position_y = screen_height
    if gun.position_y < 1:
        gun.position_y = 1

    robot_group.draw(screen)
    robot_group.update()

    bullet_group.draw(screen)
    bullet_group.update()

    gun_group.draw(screen)
    gun_group.update()

    red_group.draw(screen)
    red_group.update()

    # screen.blit(robot1.image, (500, 700))
    # screen.blit(robot2.image, (100, 700))

    red_collide = pygame.sprite.groupcollide(red_group, robot_group, False, True)
    if red_collide:
        life -= 1
        screen.blit(life_text, (60, 100))
        if life <= 0:
            run = False

    robot_collide = pygame.sprite.groupcollide(bullet_group, robot_group, True, True)
    if robot_collide:
        score += 1

    pygame.display.update()
    current_time += 1.25
pygame.quit()