from newItem import animatedItem
from random import randint


def new_robot(sc_width, sc_height, speed, images):
    return animatedItem(
        path='img/robots2/robot_2.0.png',
        x=sc_width, y=randint(20, sc_height - 30),
        width=100, height=100,
        speed=speed, anim=images
    )


def Wave_count(rb_time: int, lba: bool) -> int:
    if rb_time <= 1250:
        return 1
    if 1250 < rb_time <= 3000:
        return 2
    if 3000 < rb_time <= 5000:
        return 3
    if 5000 < rb_time <= 8000:
        return 4
    if 8000 < rb_time <= 11000:
        return 5
    if 11000 <= rb_time <= 13000:
        return 6
    if 13000 <= rb_time <= 15000:
        return 7
    if 15000 <= rb_time <= 16500:
        return 8
    if 16500 <= rb_time <= 18000:
        return 9
    if 18000 <= rb_time <= 19000:
        return 10
    if rb_time >= 19000 and lba:
        return 11


def rb_time(wave: int, rb: str) -> int:
    match rb:
        case 'rb1':
            if 0 < wave < 4:
                return 105
            if 3 < wave < 8:
                return 90
            if wave > 7:
                return 80
        case 'rb2':
            if 0 < wave < 4:
                return 125
            if 3 < wave < 8:
                return 115
            if wave > 7:
                return 105