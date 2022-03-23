#!/usr/bin/env python3
# coding:utf-8
import pygame
from src.game import Game

with open("version") as versionFile:
    version = versionFile.read().replace("\n", "")
    versionFile.close()

pygame.init()
game = Game(version=version)
game.run()
