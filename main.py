import pygame
from random import randint
from newItem import Item, movingItem, animatedItem, controlItem
from work_with_json import inJson


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
gameplay = True
pause = False

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

while run:
    if gameplay:
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
            if key[pygame.K_q]:
                pause = True

            # shooting
            if key[pygame.K_SPACE] and not reloading and e.type == pygame.KEYDOWN:
                x = gun.rect.x + 110
                y = gun.rect.y + 35
                bullet_group.add(movingItem(
                    path='img/bomb.png',
                    x=x, y=y,
                    width=30, height=30,
                    speed=50
                ))
                cage_count -= 1
                if cage_count <= 0:
                    reloading = True

        # reloading
        if (key[pygame.K_r]) or reloading == True:
            reloading = True
            cd_time -= 1
            screen.blit(cage_count_text, (screen_width-200, 140))
            if cd_time <= 0:
                cage_count = cage_count_const
                cd_time = cd_time_const
                screen.blit(cage_count_text, (screen_width-200, 140))
                reloading = False

        # write a texts
        screen.blit(score_text, (screen_width-200, 60))
        screen.blit(life_text, (screen_width-200, 100))
        screen.blit(cage_count_text, (screen_width-200, 140))

        # mob spawn
        anim = [
                pygame.image.load('img/mob/mob1-removebg-preview.png'),
                pygame.image.load('img/mob/mob2-removebg-preview.png'),
                pygame.image.load('img/mob/mob3-removebg-preview.png'),
                pygame.image.load('img/mob/mob4-removebg-preview.png'),
            ]
        if current_time >= robot1_time:
            robot_group.add(animatedItem(
                    path='img/mob/mob1-removebg-preview.png',
                    x=screen_width, y=randint(20, screen_height - 30),
                    width=100, height=100,
                    speed=5, anim=anim
                ))
            robot1_time += 105
        if current_time >= robot2_time:
            robot_group.add(
                animatedItem(
                    path='img/mob/mob1-removebg-preview.png',
                    x=screen_width, y=randint(20, screen_height - 30),
                    width=100, height=100,
                    speed=5, anim=anim
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
            screen.blit(life_text, (screen_width-200, 100))
            if life <= 0:
                from datetime import datetime
                if score != 0:
                    now = datetime.now()
                    key = f'{now.year}_{now.month}_{now.day}={now.hour}_{now.minute}_{now.second}'
                    result = inJson('results.json').new_value(key, score)
                gameplay = False

        robot_collide = pygame.sprite.groupcollide(bullet_group, robot_group, True, True)
        if robot_collide:
            score += 1

        # update display and mob spawn timer
        pygame.display.update()
        current_time += 1.25
    elif not gameplay and not pause:
        lose_label = font.render('Вы проиграли!', False, (180, 0, 0))
        score_label = font.render(f'Счет: {score}', False, (180, 0, 0))
        lose_btn = font.render('Заново', False, (180, 0, 0))
        lose_btn_rect = lose_btn.get_rect(topleft=(740, 400))
        exit_btn = font.render('Выйти', False, (180, 0, 0))
        exit_btn_rect = exit_btn.get_rect(topleft=(745, 460))

        screen.fill((87, 88, 89))

        screen.blit(lose_label, (700, 300))
        screen.blit(score_label, (740, 350))

        pygame.draw.rect(screen, (50, 168, 70), (730, 390, 110, 45))
        screen.blit(lose_btn, lose_btn_rect)

        pygame.draw.rect(screen, (50, 168, 70), (730, 450, 110, 45))
        screen.blit(exit_btn, exit_btn_rect)

        mouse = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:
            if lose_btn_rect.collidepoint(mouse):
                gameplay = True
                robot_group.empty()
                bullet_group.empty()

                life = 10
                cage_count = cage_count_const
                score = 0
            if exit_btn_rect.collidepoint(mouse):
                run = False

        for e in pygame.event.get():
            key = pygame.key.get_pressed()
            if e.type == pygame.QUIT:
                run = False
            if key[pygame.K_ESCAPE]:
                run = False
        pygame.display.update()

    if pause:
        gameplay = False

        pause_label = font.render('Пауза', False, (180, 0, 0))
        score_label = font.render(f'Счет: {score}', False, (180, 0, 0))
        life_label = font.render(f'Жизней: {life}', False, (180, 0, 0))
        continue_btn = font.render('Продолжить', False, (180, 0, 0))
        continue_btn_rect = continue_btn.get_rect(topleft=(710, 430))
        exit_btn = font.render('Выйти', False, (180, 0, 0))
        exit_btn_rect = exit_btn.get_rect(topleft=(745, 490))

        screen.fill((87, 88, 89))

        screen.blit(pause_label, (740, 300))
        screen.blit(score_label, (740, 350))
        screen.blit(life_label, (710, 380))

        pygame.draw.rect(screen, (50, 168, 70), (700, 420, 170, 45))
        screen.blit(continue_btn, continue_btn_rect)

        pygame.draw.rect(screen, (50, 168, 70), (730, 480, 110, 45))
        screen.blit(exit_btn, exit_btn_rect)

        mouse = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:
            if continue_btn_rect.collidepoint(mouse):
                gameplay = True
                pause = False
            if exit_btn_rect.collidepoint(mouse):
                run = False

        for e in pygame.event.get():
            key = pygame.key.get_pressed()
            if e.type == pygame.QUIT:
                run = False
            if key[pygame.K_ESCAPE]:
                run = False
            if key[pygame.K_q]:
                gameplay = True
                pause = False
        pygame.display.update()


pygame.quit()