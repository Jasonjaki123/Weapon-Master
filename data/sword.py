import pygame, math
from pygame.locals import *
pygame.init()

class Sword():
    def __init__(self, pos, img, angle):
        self.img = img
        self.img.set_colorkey((0, 0, 0))
        self.size = [0, 0]
        self.size[0] = self.img.get_width()
        self.size[1] = self.img.get_height()
        self.pos = pos
        self.angle = angle
    def render(self, surface):
        surface.blit(self.img, self.pos)

    @property
    def center(self):
        return [self.pos[0] + self.size[0] // 2, self.pos[1] + self.size[1] // 2]
    def get_angle(self, target):
        self.angle = math.atan2(target[1] - self.center[1], target[0] - self.center[0])
    def rotate(self):
        pygame.transform.rotate(self.img, self.angle)
