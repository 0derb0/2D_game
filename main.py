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
menu_font = pygame.font.Font(None, 55)

# recharge
reloading = False
cage_count_const = 30
cage_count = 30
cd_time_const = 90
cd_time = 90

# run the game
run = True
gameplay = False
pause = False
game_menu = True

# robot group and timers
current_time = 0
robot_group = pygame.sprite.Group()
robot1_time = 105
robot2_time = 125
standard_robot_speed = screen_width/240
wave_count = 0
final_wave = 11
spawned1 = 0
spawned2 = 0
level_boss_alive = True

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

images = []
for num in range(8):
    img = pygame.image.load(f"img/robots2/robot_2.{num}.png")
    img = pygame.transform.scale(img, (180, 140))
    images.append(img)

old_images = []
for num in range(1, 5):
    img = pygame.image.load(f'img/mob/mob{num}-removebg-preview.png')
    img = pygame.transform.scale(img, (100, 100))
    old_images.append(img)

while run:
    if gameplay:

        # wave_count = 1
        key = pygame.key.get_pressed()

        # fps, bg-color, texts
        clock.tick(fps)
        screen.fill((200, 162, 200))
        score_text = font.render(f'Score: {score}', True, (180, 0, 0))
        life_text = font.render(f'{life} lifes', True, (180, 0, 0))
        cage_count_text = font.render(f'{cage_count} bullets', True, (180, 0, 0))
        data = font.render(f'1:{spawned1}, 2:{spawned2}, wave: {wave_count}, ct: {current_time}, rb1: {robot1_time}, rb2: {robot2_time}', True, (180, 0, 0))

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
        screen.blit(data, (20, screen_height-25))

        if robot2_time <= 1250:
            wave_count = 1
        if robot2_time > 1250 and robot2_time <= 3000:
            wave_count = 2
        if 3000 < robot2_time and robot2_time <= 5000:
            wave_count = 3
        if 5000 < robot2_time and robot2_time <= 8000:
            wave_count = 4
        if 8000 < robot2_time and robot2_time <= 11000:
            wave_count = 5
        if 11000 <= robot2_time and robot2_time <= 13000:
            wave_count = 6
        if 13000 <= robot2_time and robot2_time <= 15000:
            wave_count = 7
        if 15000 <= robot2_time and robot2_time <= 16500:
            wave_count = 8
        if 16500 <= robot2_time and robot2_time <= 18000:
            wave_count = 9
        if 18000 <= robot2_time and robot2_time <= 19000:
            wave_count = 10
        if 19000 <= robot2_time and level_boss_alive:
            wave_count = 11



        if current_time >= robot1_time and 0 < wave_count < 4:
            robot_group.add(animatedItem(
                    path='img/robots2/robot_2.0.png',
                    x=screen_width, y=randint(20, screen_height - 30),
                    width=100, height=100,
                    speed=standard_robot_speed, anim=images
                ))
            spawned1 += 1
            robot1_time += 105
        if current_time >= robot2_time and 0 < wave_count < 4:
            robot_group.add(
                animatedItem(
                    path='img/mob/mob1-removebg-preview.png',
                    x=screen_width, y=randint(20, screen_height - 30),
                    width=100, height=100,
                    speed=standard_robot_speed, anim=old_images
                )
            )
            spawned2 += 1
            robot2_time += 125
            # 10 robot2 = 1250
            # 3000 - 24rb2
            # 40rb2 = 5000

        if current_time >= robot1_time and 3 < wave_count < 8:
            robot_group.add(animatedItem(
                    path='img/robots2/robot_2.0.png',
                    x=screen_width, y=randint(20, screen_height - 30),
                    width=100, height=100,
                    speed=standard_robot_speed, anim=images
                ))
            spawned1 += 1

            robot1_time += 90
        if current_time >= robot2_time and 3 < wave_count < 8:
            robot_group.add(
                animatedItem(
                    path='img/mob/mob1-removebg-preview.png',
                    x=screen_width, y=randint(20, screen_height - 30),
                    width=100, height=100,
                    speed=standard_robot_speed, anim=old_images
                )
            )
            spawned2 += 1

            robot2_time += 115


        if current_time >= robot1_time and wave_count > 7:
            robot_group.add(animatedItem(
                path='img/robots2/robot_2.0.png',
                x=screen_width, y=randint(20, screen_height - 30),
                width=100, height=100,
                speed=standard_robot_speed, anim=images
            ))
            spawned1 += 1

            robot1_time += 80

        if current_time >= robot2_time and wave_count > 7:
            robot_group.add(
                animatedItem(
                    path='img/mob/mob1-removebg-preview.png',
                    x=screen_width, y=randint(20, screen_height - 30),
                    width=100, height=100,
                    speed=standard_robot_speed, anim=old_images
                )
            )
            spawned2 += 1

            robot2_time += 105

        if current_time >= robot1_time and wave_count == final_wave:
            robot_group.add(animatedItem(
                path='img/robots2/robot_2.0.png',
                x=screen_width, y=randint(20, screen_height - 30),
                width=100, height=100,
                speed=standard_robot_speed, anim=images
            ))
            robot_group.add(animatedItem(
                    path='img/mob/mob1-removebg-preview.png',
                    x=screen_width, y=randint(20, screen_height - 30),
                    width=100, height=100,
                    speed=standard_robot_speed, anim=old_images
                ))
            robot1_time += 90

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
                if score != 0:
                    result = inJson('results.json').new_value(score)

        robot_collide = pygame.sprite.groupcollide(bullet_group, robot_group, True, True)
        if robot_collide:
            score += 1

        # update display and mob spawn timer
        pygame.display.update()
        current_time += 1.25
    elif not gameplay and not pause and not game_menu:

        text_color = (0, 0, 0)
        text_width = screen_width/2-100
        text_height = screen_height/3

        lose_label = menu_font.render('Вы проиграли!', False, text_color)
        score_label = menu_font.render(f'Счет: {score}', False, text_color)
        lose_btn = menu_font.render('Заново', False, text_color)
        lose_btn_rect = lose_btn.get_rect(topleft=(text_width, text_height+120))
        exit_btn = menu_font.render('Выйти', False, text_color)
        exit_btn_rect = exit_btn.get_rect(topleft=(text_width, text_height+180))

        screen.fill((255, 55, 0))

        screen.blit(lose_label, (text_width, text_height))
        screen.blit(score_label, (text_width, text_height+60))

        # pygame.draw.rect(screen, (50, 168, 70), (730, 390, 110, 45))
        screen.blit(lose_btn, lose_btn_rect)

        # pygame.draw.rect(screen, (50, 168, 70), (730, 450, 110, 45))
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

        color_text = (255, 255, 255)
        text_width = screen_width/2-100
        text_height = screen_height/3

        pause_label = menu_font.render('Пауза', False, color_text)
        score_label = menu_font.render(f'Счет: {score}', False, color_text)
        life_label = menu_font.render(f'Жизней: {life}', False, color_text)
        continue_btn = menu_font.render('Продолжить', False, color_text)
        continue_btn_rect = continue_btn.get_rect(topleft=(text_width, text_height+180))
        exit_btn = menu_font.render('Выйти', False, color_text)
        exit_btn_rect = exit_btn.get_rect(topleft=(text_width, text_height+240))

        screen.fill((0, 0, 0))

        screen.blit(pause_label, (text_width, text_height))
        screen.blit(score_label, (text_width, text_height+60))
        screen.blit(life_label, (text_width, text_height+120))

        # pygame.draw.rect(screen, (50, 168, 70), (screen_width/2, screen_height/2+90, 170, 45))
        screen.blit(continue_btn, continue_btn_rect)

        # pygame.draw.rect(screen, (50, 168, 70), (screen_width/2, screen_height/2+120, 110, 45))
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
    if not gameplay and game_menu:

        text_color = (121, 168, 50)
        text_width = screen_width / 2 - 100
        text_height = screen_height / 3

        game_label = menu_font.render('UwU', False, text_color)
        label = menu_font.render('Меню', False, text_color)
        go_btn = menu_font.render('Начать', False, text_color)
        go_btn_rect = go_btn.get_rect(topleft=(text_width, text_height + 120))
        result_btn = menu_font.render('Результаты', False, text_color)
        result_btn_rect = result_btn.get_rect(topleft=(text_width, text_height + 180))
        exit_btn = menu_font.render('Выйти', False, text_color)
        exit_btn_rect = exit_btn.get_rect(topleft=(text_width, text_height + 240))

        screen.fill((0, 0, 0))


        screen.blit(game_label, (text_width, text_height))
        screen.blit(label, (text_width, text_height + 60))

        screen.blit(go_btn, go_btn_rect)
        screen.blit(result_btn, result_btn_rect)
        screen.blit(exit_btn, exit_btn_rect)

        for ev in pygame.event.get():
            key = pygame.key.get_pressed()
            if ev.type == pygame.QUIT:
                run = False
            if key[pygame.K_ESCAPE]:
                run = False
            if key[pygame.K_q]:
                gameplay = True
                game_menu = False

        mouse = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:
            if go_btn_rect.collidepoint(mouse):
                gameplay = True
                game_menu = False
            if exit_btn_rect.collidepoint(mouse):
                run = False

        pygame.display.update()

pygame.quit()