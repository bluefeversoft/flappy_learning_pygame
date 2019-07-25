import pygame
import random
from defs import *


class Pipe():

    def __init__(self, gameDisplay, x, y, pipe_type):
        self.gameDisplay = gameDisplay
        self.state = PIPE_MOVING
        self.pipe_type = pipe_type
        self.img = pygame.image.load(PIPE_FILENAME)
        self.rect = self.img.get_rect()
        if pipe_type == PIPE_UPPER:
            y = y - self.rect.height
        self.set_position(x, y)

    def set_position(self, x, y):
        self.rect.left = x
        self.rect.top = y

    def move_position(self, dx, dy):
        self.rect.centerx += dx
        self.rect.centery += dy

    def draw(self):
        self.gameDisplay.blit(self.img, self.rect)

    def check_status(self):
        if self.rect.right < 0:
            self.state = PIPE_DONE

    def update(self, dt):
        if self.state == PIPE_MOVING:
            self.move_position(-(PIPE_SPEED * dt), 0)
            self.draw()
            self.check_status()


class PipeCollection():

    def __init__(self, gameDisplay):
        self.gameDisplay = gameDisplay
        self.pipes = []


    def add_new_pipe_pair(self, x):

        top_y = random.randint(PIPE_MIN, PIPE_MAX - PIPE_GAP_SIZE)
        bottom_y = top_y + PIPE_GAP_SIZE

        p1 = Pipe(self.gameDisplay, x, top_y, PIPE_UPPER)
        p2 = Pipe(self.gameDisplay, x, bottom_y, PIPE_LOWER)

        self.pipes.append(p1)
        self.pipes.append(p2)

    def create_new_set(self):
        self.pipes = []
        placed = PIPE_FIRST

        while placed < DISPLAY_W:
            self.add_new_pipe_pair(placed)
            placed += PIPE_ADD_GAP

    def update(self, dt):

        rightmost = 0

        for p in self.pipes:
            p.update(dt)
            if p.pipe_type == PIPE_UPPER:
                if p.rect.left > rightmost:
                    rightmost = p.rect.left

        if rightmost < (DISPLAY_W - PIPE_ADD_GAP):
            self.add_new_pipe_pair(DISPLAY_W)

        self.pipes = [p for p in self.pipes if p.state == PIPE_MOVING]

































































