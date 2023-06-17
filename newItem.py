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
    def __init__(
            self, path,
            x, y,
            width, height,
            speed,
            to_Right=False, to_Left=False
    ):
        Item.__init__(self, path, x, y, width, height)
        self.speed = speed
        self.rect = self.image.get_rect(center=(x, y))
        self.to_Right = to_Right
        self.to_Left = to_Left

    def update(self):
        if self.to_Right:
            self.rect.x += self.speed
        if self.to_Left:
            self.rect.x -= self.speed


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