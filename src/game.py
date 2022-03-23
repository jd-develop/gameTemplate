#!/usr/bin/env python3
# coding:utf-8
import pygame
from pygame import mixer
from pygame import locals
import pytmx
import pyscroll

from src import player
from src import item


STATES = {  # here to add UIs
    "playing": 0,
    "game_title": 1
}


class Game:
    """Our game class"""
    def __init__(self, version) -> None:
        self.FPS = 60

        self.version = version
        self.state = STATES["game_title"]

        self.screen = pygame.display.set_mode((800, 600), locals.RESIZABLE)
        pygame.display.set_caption("GameTemplate")

        pygame.font.init()
        self.pixel_verdana = pygame.font.Font("font.ttf", 12)

        # charger la carte
        self.tmx_data = pytmx.util_pygame.load_pygame("map.tmx")
        self.map_data = pyscroll.data.TiledMapData(self.tmx_data)
        self.map_layer = pyscroll.orthographic.BufferedRenderer(self.map_data, self.screen.get_size())
        self.map_layer.zoom = 2
        self.map = "actual_map"

        # générer un joueur
        player_position = self.tmx_data.get_object_by_name("playerspawn")
        self.player = player.Player(player_position.x, player_position.y)
        self.group = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer=2)
        self.group.add(self.player)

        # liste de collisions + items
        self.walls = []
        self.items = []
        for obj in self.tmx_data.objects:
            if obj.type == "collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            if obj.name == "coin":
                coin = item.Item(obj.x, obj.y, 'coin', loot={
                    'coin': 1,
                }
                                 )
                self.group.add(coin)
                self.items.append(coin)

    def update(self):
        self.group.update()

        if self.state == STATES["playing"]:
            # vérification des collisions
            for sprite in self.group.sprites():
                if isinstance(sprite, player.Player):
                    # objets collisions
                    if sprite.feet.collidelist(self.walls) > -1:
                        sprite.move_back()
                    # ITEMS
                    items_collided = sprite.rect.collidelistall(self.items)
                    if len(items_collided) > 0:
                        indexes = []
                        for item_idx in items_collided:
                            item_ = self.items[item_idx]
                            self.group.remove(item_)
                            self.player.loot(item_.loot)
                            indexes.append(item_idx)
                        # remove collected item from the map :
                        self.items = [e for i, e in enumerate(self.items) if i not in indexes]

    def handle_input(self):
        pressed = pygame.key.get_pressed()

        if self.state == STATES["playing"]:
            if pressed[pygame.K_z] or pressed[pygame.K_UP]:
                # self.player.change_animation("up")
                # self.player.move_up()
                ...
            elif pressed[pygame.K_s] or pressed[pygame.K_DOWN]:
                # self.player.change_animation("down")
                # self.player.move_down()
                ...
            elif pressed[pygame.K_d] or pressed[pygame.K_RIGHT]:
                # self.player.change_animation("right")
                # self.player.move_right()
                ...
            elif pressed[pygame.K_q] or pressed[pygame.K_LEFT]:
                # self.player.change_animation("left")
                # self.player.move_left()
                ...

    def change_map(self, map_name: str = "map"):
        # charger la carte
        self.tmx_data = pytmx.util_pygame.load_pygame(f"{map_name}.tmx")
        self.map_data = pyscroll.data.TiledMapData(self.tmx_data)
        self.map_layer = pyscroll.orthographic.BufferedRenderer(self.map_data, self.screen.get_size())
        self.map_layer.zoom = 2
        self.map = map_name

    def run(self):
        mixer.music.load("music.ogg")
        mixer.music.play(-1)
        running = True
        clock = pygame.time.Clock()

        while running:
            # Our game loop
            if self.state == STATES['playing']:
                self.player.save_location()
                self.handle_input()
                self.update()
                self.group.center(self.player.rect.center)
                self.group.draw(self.screen)
                self.screen.blit(self.pixel_verdana.render("GameTemplate " + self.version, False, (0, 0, 0)), (5, 0))
            elif self.state == STATES["game_title"]:
                self.update()
                self.group.center(self.player.rect.center)
                self.group.draw(self.screen)
                self.screen.blit(self.pixel_verdana.render("GameTemplate " + self.version, False, (0, 0, 0)), (5, 0))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == locals.VIDEORESIZE:
                    width, height = event.size
                    if width < 800:
                        width = 800
                    if height < 600:
                        height = 600
                    self.screen = pygame.display.set_mode((width, height), locals.RESIZABLE)
                    self.map_layer.set_size(self.screen.get_size())
                elif event.type == pygame.KEYUP:
                    if self.state == STATES['playing']:
                        if event.key == pygame.K_ESCAPE:
                            self.state = STATES['game_title']
                    elif self.state == STATES['game_title']:
                        if event.key == pygame.K_p:
                            self.state = STATES['playing']

            clock.tick(self.FPS)

        pygame.quit()
