import pygame


class Item(pygame.sprite.Sprite):
    def __init__(self, path, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(path)
        self.image = pygame.transform.scale(self.image, (width, height))

        self.position_x = x
        self.position_y = y

        self.rect = self.image.get_rect(topleft=(x, y))


class movingItem(Item):
    def __init__(self, path, x, y, width, height, speed):
        Item.__init__(self, path, x, y, width, height)
        self.speed = speed
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        self.rect.x += self.speed


class animatedItem(movingItem):
    def __init__(self, path, x, y, height, width, speed, anim):
        movingItem.__init__(self, path, x, y, height, width, speed)
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 125
        self.width = width
        self.height = height

        self.anim = anim

    def update(self):
        self.rect.x -= self.speed

        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(self.anim):
                self.frame = 0

            self.image = self.anim[self.frame]
            # self.image = pygame.transform.scale(self.image, (self.width, self.height))


class controlItem(Item):
    def __init__(
            self, pash,
            x, y,
            width, height,
            flip, velocity
    ):
        Item.__init__(self, pash, x, y, width, height)
        self.image = pygame.transform.flip(self.image, flip, False)
        self.rect = self.image.get_rect(center=(x, y))
        self.velocity = velocity

    def move(self, up, down):
        key = pygame.key.get_pressed()
        if key[up]:
            self.position_y -= self.velocity
        if key[down]:
            self.position_y += self.velocity

        self.rect.center = [self.position_x, self.position_y]