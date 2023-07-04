import pygame
from newItem import Item, movingItem, controlItem
from work_with_json import inJson
from Robot_spawn import *
import consts


pygame.init()

clock = pygame.time.Clock()

# creating a display
screen = pygame.display.set_mode()
pygame.display.set_caption('UwU')
icon = pygame.image.load('img/icon1.png')
pygame.display.set_icon(icon)

# global variables

# screen size
screen_size = pygame.display.get_window_size()

# create font
font = pygame.font.Font(None, 36)
menu_font = pygame.font.Font(None, 55)
wave_font = pygame.font.Font(None, 100)

gun_data = consts.Gun_data(
    reloading=False, cage_count_const=30, cage_count=30,
    cd_time_const=90, cd_time=90
)

glob_data = consts.Global_data(
    height=screen_size[1], width=screen_size[0], fps=100,
    run=True, gameplay=False, pause=False, game_menu=True,
    wave_label=False, label_timer=0, score=0, life=10
)

# robot group and timers

robot_group = pygame.sprite.Group()

rb_data = consts.Robot_data(
    current_time=0, robot1_time=105, robot2_time=125,
    standard_robot_speed=glob_data.width / 240,
    wave_count=0, final_wave=11, spawned1=0, spawned2=0,
    level_boss_alive=True
)

# items

# create a gun
gun = controlItem(
    pash='img/gun1.png',
    x=100, y=glob_data.height/2,
    width=200, height=200,
    flip=True, velocity=8
)
gun_group = pygame.sprite.GroupSingle(gun)

# create a collide line
red_line = Item(
    path='img/1.png',
    x=glob_data.width/5, y=0,
    width=5, height=glob_data.height
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


while glob_data.run:
    if glob_data.gameplay:

        key = pygame.key.get_pressed()

        # fps, bg-color, texts
        clock.tick(glob_data.fps)
        screen.fill((200, 162, 200))

        text_color = (180, 0, 0)
        text_width = glob_data.width - 200
        text_height = 60

        labels = (
            f'Score: {glob_data.score}',
            f'Wave: {rb_data.wave_count}',
            f'{glob_data.life} lifes',
            f'{gun_data.cage_count} bullets'
        )
        labels = consts.render_labels(
            text_color, labels, font
        )

        data = font.render(f'1:{rb_data.spawned1}, 2:{rb_data.spawned2}, wave: {rb_data.wave_count}, rb1: {rb_data.robot1_time}, rb2: {rb_data.robot2_time}, ct: {rb_data.current_time}', True, (180, 0, 0))

        # get events
        for e in pygame.event.get():
            key = pygame.key.get_pressed()

            # leave the game
            if e.type == pygame.QUIT:
                glob_data.run = False
            if key[pygame.K_ESCAPE]:
                glob_data.run = False
            if key[pygame.K_q]:
                glob_data.pause = True

            # shooting
            if key[pygame.K_SPACE] and not gun_data.reloading and e.type == pygame.KEYDOWN:
                x = gun.rect.x + 110
                y = gun.rect.y + 35
                bullet_group.add(movingItem(
                    path='img/bomb.png',
                    x=x, y=y,
                    width=30, height=30,
                    speed=50
                ))
                gun_data.cage_count -= 1
                if gun_data.cage_count <= 0:
                    gun_data.reloading = True

        # reloading
        if (key[pygame.K_r]) or gun_data.reloading:
            gun_data.reloading = True
            gun_data.cd_time -= 1
            screen.blit(labels[3], (glob_data.width-200, 180))
            if gun_data.cd_time <= 0:
                gun_data.cage_count = gun_data.cage_count_const
                gun_data.cd_time = gun_data.cd_time_const
                screen.blit(labels[3], (glob_data.width-200, 140))
                gun_data.reloading = False

        space = 0
        for label in labels:
            screen.blit(label, (text_width, text_height + space))
            space += 40
        screen.blit(data, (20, glob_data.height-25))

        last_wave = rb_data.wave_count
        new_wave = Wave_count(rb_data.robot2_time, rb_data.level_boss_alive)
        if new_wave != last_wave:
            print(f'->{new_wave == last_wave}<->{new_wave}<->{last_wave}<-')
            glob_data.gameplay = False
            glob_data.wave_label = True
            rb_data.wave_count = new_wave

        if rb_data.current_time >= rb_data.robot1_time:
            robot_group.add(new_robot(
                glob_data.width, glob_data.height,
                rb_data.standard_robot_speed, images
            ))
            rb_data.robot1_time += rb_time(rb_data.wave_count, 'rb1')

        if rb_data.current_time >= rb_data.robot2_time:
            robot_group.add(new_robot(
                glob_data.width, glob_data.height,
                rb_data.standard_robot_speed, old_images
            ))
            rb_data.robot2_time += rb_time(rb_data.wave_count, 'rb2')

        if rb_data.current_time >= rb_data.robot1_time \
                and rb_data.wave_count == rb_data.final_wave:
            robot_group.add(new_robot(
                glob_data.width, glob_data.height,
                rb_data.standard_robot_speed, images
            ))
            robot_group.add(new_robot(
                glob_data.width, glob_data.height,
                rb_data.standard_robot_speed, old_images
            ))
            rb_data.robot1_time += 90

        # gun move
        gun.move(pygame.K_w, pygame.K_s)
        if gun.position_y > glob_data.height:
            gun.position_y = glob_data.height
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
            glob_data.life -= 1
            screen.blit(labels[2], (glob_data.width-200, 100))
            if glob_data.life <= 0:
                if glob_data.score != 0:
                    result = inJson('results.json').new_value(glob_data.score, rb_data.wave_count)
                glob_data.gameplay = False

        robot_collide = pygame.sprite.groupcollide(bullet_group, robot_group, True, True)
        if robot_collide:
            glob_data.score += 1

        # update display and mob spawn timer
        pygame.display.update()
        rb_data.current_time += 1.25
    elif not glob_data.gameplay and glob_data.wave_label:
        from time import sleep



        if glob_data.label_timer <= 300:
            text_color = (180, 0, 0)
            labels = (f'Wave: {rb_data.wave_count}', )
            labels = consts.render_labels(text_color, labels, wave_font)
            height = glob_data.height / 2
            width = glob_data.width / 2 - 100
            for label in labels:
                screen.blit(label, (width, height))
            glob_data.label_timer += 1
            pygame.display.update()
        else:
            glob_data.label_timer = 0
            glob_data.gameplay = True
            glob_data.wave_label = False



    elif not glob_data.gameplay and not glob_data.pause \
            and not glob_data.game_menu:

        text_color = (0, 0, 0)
        text_width = glob_data.width/2-100
        text_height = glob_data.height/3

        screen.fill((255, 55, 0))

        space = 0

        labels = (
            'Вы проиграли!',
            f'Score: {glob_data.score}',
            f'Wave: {rb_data.wave_count}'
        )
        labels = consts.render_labels(text_color, labels, menu_font)
        for label in labels:
            screen.blit(label, (text_width, text_height + space))
            space += 60

        buttons = ('Заново', 'Выйти')
        buttons = consts.render_buttons(
            text_color, buttons, menu_font,
            text_width, text_height, space, 60
        )
        for btn in buttons:
            screen.blit(btn[0], btn[1])

        mouse = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:
            if buttons[0][1].collidepoint(mouse):
                glob_data.gameplay = True
                robot_group.empty()
                bullet_group.empty()

                glob_data.life = 10
                gun_data.cage_count = gun_data.cage_count_const
                glob_data.score = 0
                rb_data.wave_count = 0
                rb_data.current_time = 0
                rb_data.robot1_time, rb_data.robot2_time = 0, 0
            if buttons[1][1].collidepoint(mouse):
                glob_data.run = False

        for e in pygame.event.get():
            key = pygame.key.get_pressed()
            if e.type == pygame.QUIT:
                glob_data.run = False
            if key[pygame.K_ESCAPE]:
                glob_data.run = False
        pygame.display.update()
    elif glob_data.pause:
        glob_data.gameplay = False

        color_text = (255, 255, 255)
        text_width = glob_data.width/2-100
        text_height = glob_data.height/3

        screen.fill((0, 0, 0))

        space = 0

        labels = (
            'Пауза',
            f'Счет: {glob_data.score}',
            f'Жизней: {glob_data.life}'
        )
        labels = consts.render_labels(
            color_text, labels, menu_font
        )
        for label in labels:
            screen.blit(label, (text_width, text_height + space))
            space += 60
        buttons = (
            'Продолжить',
            'Выйти'
        )
        buttons = consts.render_buttons(
            color_text, buttons, menu_font, text_width,
            text_height, space, 60
        )
        for btn in buttons:
            screen.blit(btn[0], btn[1])

        mouse = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:
            if buttons[0][1].collidepoint(mouse):
                glob_data.gameplay = True
                glob_data.pause = False
            if buttons[1][1].collidepoint(mouse):
                glob_data.run = False

        for e in pygame.event.get():
            key = pygame.key.get_pressed()
            if e.type == pygame.QUIT:
                glob_data.run = False
            if key[pygame.K_ESCAPE]:
                glob_data.run = False
            if key[pygame.K_q]:
                glob_data.gameplay = True
                glob_data.pause = False
        pygame.display.update()
    elif not glob_data.gameplay and glob_data.game_menu:

        text_color = (121, 168, 50)
        text_width = glob_data.width / 2 - 100
        text_height = glob_data.height / 3

        screen.fill((0, 0, 0))

        space = 0

        labels = ('UwU', 'Меню')
        labels = consts.render_labels(text_color, labels, menu_font)
        for label in labels:
            screen.blit(label, (text_width, text_height + space))
            space += 60

        buttons = ('Играть', 'Результаты', 'Выйти')
        buttons = consts.render_buttons(
            text_color, buttons, menu_font,
            text_width, text_height, space, 60
        )
        for btn in buttons:
            screen.blit(btn[0], btn[1])

        for ev in pygame.event.get():
            key = pygame.key.get_pressed()
            if ev.type == pygame.QUIT:
                glob_data.run = False
            if key[pygame.K_ESCAPE]:
                glob_data.run = False
            if key[pygame.K_q]:
                glob_data.gameplay = True
                glob_data.game_menu = False

        mouse = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:
            if buttons[0][1].collidepoint(mouse):
                glob_data.gameplay = True
                glob_data.game_menu = False
            if buttons[2][1].collidepoint(mouse):
                glob_data.run = False

        pygame.display.update()

pygame.quit()