#!/usr/bin/env python3
# coding:utf-8
import pygame


class Item(pygame.sprite.Sprite):
    def __init__(self, x, y, type_: str = 'coin', ext: str = "jpg", loot: dict = None,
                 color_key: list = None):
        super().__init__()
        if loot is None:
            loot = {'coin': 1}
        if color_key is None:
            color_key = [0, 0, 0]
        self.sprite_sheet = pygame.image.load(f"{type_}.{ext}")
        self.image = self.get_image(0, 0)
        self.image.set_colorkey(color_key)
        self.image = pygame.transform.scale(self.image, (24, 24))
        self.rect = self.image.get_rect()
        self.position = [x, y]
        self.loot = loot

    def update(self):
        self.rect.topleft = self.position

    def get_image(self, x, y):
        image = pygame.Surface([24, 24])
        image.blit(self.sprite_sheet, (0, 0), (x, y, 24, 24))
        return image
