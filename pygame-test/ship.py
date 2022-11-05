""" This module is responsible for all the functionality related to the spaceship"""

import pygame as pg
import os

class Ship:

    TEXTURE_RATIO = 10

    TEXTURE_WIDTH = 500 // TEXTURE_RATIO
    TEXTURE_HEIGHT = 413 // TEXTURE_RATIO

    WIDTH = TEXTURE_WIDTH
    HEIGHT = TEXTURE_HEIGHT

    velocity = 5
    health = 10

    def __init__(self, player_name, position_x, position_y, texture_file_name) -> None:
        self.texture_file_name = texture_file_name
        self.player_name = player_name
        self.position_x = position_x
        self.position_y = position_y
        self.texture = self.init_texture()
        self.rectangle = pg.Rect(position_x, position_y, Ship.WIDTH, Ship.HEIGHT)

    def init_texture(self):
        tmp_texture = pg.image.load(os.path.join('Assets',self.texture_file_name))
        tmp_texture = pg.transform.scale(tmp_texture, (Ship.TEXTURE_WIDTH, Ship.TEXTURE_HEIGHT))
        # Implement rotation pg.transform.rotate(ship_yellow_img, 90)

        return tmp_texture