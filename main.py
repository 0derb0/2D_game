import pygame
from random import randint
from newItem import Item, movingItem, controlItem


pygame.init()

# create fps
fps = 100
clock = pygame.time.Clock()

# creating a display
screen = pygame.display.set_mode()
pygame.display.set_caption('UwU')
icon = pygame.image.load('img/icon1.png')
pygame.display.set_icon(icon)

# global variables

# screen size
screen_size = pygame.display.get_window_size()
screen_width = screen_size[0]
screen_height = screen_size[1]

# score and life
score = 0
life = 10

# create font
font = pygame.font.Font(None, 36)

# recharge
reloading = False
cage_count_const = 30
cage_count = 30
cd_time_const = 90
cd_time = 90

# run the game
run = True

# robot group and timers
current_time = 0
robot_group = pygame.sprite.Group()
robot1_time = 105
robot2_time = 125

# items

# create a gun
gun = controlItem(
    pash='img/gun1.png',
    x=100, y=screen_height/2,
    width=200, height=200,
    flip=True, velocity=8
)
gun_group = pygame.sprite.GroupSingle(gun)

# create a collide line
red_line = Item(
    path='img/1.png',
    x=screen_width/5, y=0,
    width=5, height=screen_height
)
red_group = pygame.sprite.GroupSingle(red_line)

# create bullet group
bullet_group = pygame.sprite.Group()

mob_images = [
    'img/mob/mob1-removebg-preview.png',
    'img/mob/mob2-removebg-preview.png',
    'img/mob/mob3-removebg-preview.png',
    'img/mob/mob4-removebg-preview.png',
]
mob_image = 0
mobs = []

while run:
    key = pygame.key.get_pressed()

    # fps, bg-color, texts
    clock.tick(fps)
    screen.fill((200, 162, 200))
    score_text = font.render(f'Score: {score}', True, (180, 0, 0))
    life_text = font.render(f'{life} lifes', True, (180, 0, 0))
    cage_count_text = font.render(f'{cage_count} bullets', True, (180, 0, 0))

    # get events
    for e in pygame.event.get():
        key = pygame.key.get_pressed()

        # leave the game
        if e.type == pygame.QUIT:
            run = False
        if key[pygame.K_ESCAPE]:
            run = False

        # shooting
        if key[pygame.K_SPACE] and not reloading and e.type == pygame.KEYDOWN:
            x = gun.rect.x + 110
            y = gun.rect.y + 35
            bullet_group.add(movingItem(
                path='img/bomb.png',
                x=x, y=y,
                width=30, height=30,
                speed=50, to_Right=True
            ))
            cage_count -= 1
            if cage_count <= 0:
                reloading = True

    # reloading
    if (key[pygame.K_r]) or reloading == True:
        reloading = True
        cd_time -= 1
        screen.blit(cage_count_text, (60, 140))
        if cd_time <= 0:
            cage_count = cage_count_const
            cd_time = cd_time_const
            screen.blit(cage_count_text, (60, 140))
            reloading = False

    # write a texts
    screen.blit(score_text, (60, 60))
    screen.blit(life_text, (60, 100))
    screen.blit(cage_count_text, (60, 140))

    # mob spawn
    if current_time >= robot1_time:
        robot_group.add(movingItem(
                path='img/robot_11.png',
                x=screen_width, y=randint(20, screen_height - 30), 
                width=100, height=100,
                speed=5, to_Left=True
            ))
        robot1_time += 105
    if current_time >= robot2_time:
        robot_group.add(
            movingItem(
                path='img/robot_2.png',
                x=screen_width, y=randint(20, screen_height - 30),
                width=100, height=100,
                speed=5, to_Left=True
            )
        )
        robot2_time += 125

    # gun move
    gun.move(pygame.K_w, pygame.K_s)
    if gun.position_y > screen_height:
        gun.position_y = screen_height
    if gun.position_y < 1:
        gun.position_y = 1

    # draw groups
    robot_group.draw(screen)
    robot_group.update()

    bullet_group.draw(screen)
    bullet_group.update()

    gun_group.draw(screen)
    gun_group.update()

    red_group.draw(screen)
    red_group.update()

    # collides
    red_collide = pygame.sprite.groupcollide(red_group, robot_group, False, True)
    if red_collide:
        life -= 1
        screen.blit(life_text, (60, 100))
        if life <= 0:
            run = False

    robot_collide = pygame.sprite.groupcollide(bullet_group, robot_group, True, True)
    if robot_collide:
        score += 1

    # update display and mob spawn timer
    pygame.display.update()
    current_time += 1.25

pygame.quit()