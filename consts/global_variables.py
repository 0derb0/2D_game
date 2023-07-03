from dataclasses import dataclass


@dataclass
class Global_data:
    height: int
    width: int
    fps: int

    run: bool
    gameplay: bool
    pause: bool
    game_menu: bool

    score: int
    life: int


@dataclass
class Robot_data:
    current_time: float
    robot1_time: int
    robot2_time: int
    standard_robot_speed: int
    wave_count: int
    final_wave: int
    spawned1: int
    spawned2: int
    level_boss_alive: bool


@dataclass
class Gun_data:
    reloading: bool
    cage_count_const: int
    cage_count: int
    cd_time_const: int
    cd_time:int