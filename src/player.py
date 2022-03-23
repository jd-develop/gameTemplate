#!/usr/bin/env python3
# coding:utf-8
import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.sprite_sheet = pygame.image.load("player.png")
        self.animation_index = 0
        self.clock = 0
        self.image = self.get_image(0, 0)
        self.image.set_colorkey([255, 0, 255])
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()
        self.position = [x, y]
        self.images = {
            # "down": self.get_images(0),
            # "left": self.get_images(32),
            # "right": self.get_images(64),
            # "up": self.get_images(96)
        }
        self.feet = pygame.Rect(0, 0, self.rect.width / 2, 12)
        self.old_position = self.position.copy()
        self.speed = 1.5
        self.default_speed = self.speed
        self.inventory = {}

    def save_location(self):
        self.old_position = self.position.copy()

    def change_animation(self, name):
        self.image = self.images[name][self.animation_index]
        self.image.set_colorkey([255, 0, 255])
        self.clock += self.speed * 8

        if self.clock >= 100:

            self.animation_index += 1
            if self.animation_index >= len(self.images[name]):
                self.animation_index = 0

            self.clock = 0

        self.image = pygame.transform.scale(self.image, (30, 30))

    def get_images(self, y):
        images = []

        for i in range(0, 3):
            x = i * 32
            images.append(self.get_image(x, y))

        return images

    def move_right(self):
        self.position[0] += self.speed
        self.change_animation("right")

    def move_left(self):
        self.position[0] -= self.speed
        self.change_animation("left")

    def move_up(self):
        self.position[1] -= self.speed
        self.change_animation("up")

    def move_down(self):
        self.position[1] += self.speed
        self.change_animation("down")

    def update(self):
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

    def move_back(self):
        self.position = self.old_position
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

    def get_image(self, x, y):
        image = pygame.Surface([32, 32])
        image.blit(self.sprite_sheet, (0, 0), (x, y, 32, 32))
        return image

    def loot(self, loot):
        for item in loot:
            try:
                self.inventory[item] += loot[item]
            except KeyError:
                # the player have never seen this item: we can imagine a code that explain what the item is...?
                self.inventory[item] = loot[item]
