import pygame
from pygame.locals import *
pygame.init()

class cursor():
    def __init__(self, pos, cursor_img):
        self.img = pygame.image.load(cursor_img)
        self.img.set_colorkey((0, 0, 0))
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.pos = pos
    def render(self, surface, pos):
        surface.blit(self.img, (pos[0] - self.width // 2, pos[1] - self.height // 2))
