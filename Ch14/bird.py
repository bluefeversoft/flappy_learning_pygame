import pygame
import random
from defs import *
from nnet import Nnet

class Bird():

    def __init__(self, gameDisplay):
        self.gameDisplay = gameDisplay
        self.state = BIRD_ALIVE
        self.img = pygame.image.load(BIRD_FILENAME)
        self.rect = self.img.get_rect()
        self.speed = 0
        self.fitness = 0
        self.time_lived = 0
        self.nnet = Nnet(NNET_INPUTS, NNET_HIDDEN, NNET_OUTPUTS)
        self.set_position(BIRD_START_X, BIRD_START_Y)

    def reset(self):
        self.state = BIRD_ALIVE
        self.speed = 0
        self.fitness = 0
        self.time_lived = 0
        self.set_position(BIRD_START_X, BIRD_START_Y)

    def set_position(self, x, y):
        self.rect.centerx = x
        self.rect.centery = y

    def move(self, dt):

        distance = 0
        new_speed = 0

        distance = (self.speed * dt) + (0.5 * GRAVITY * dt * dt)
        new_speed = self.speed + (GRAVITY * dt)

        self.rect.centery += distance
        self.speed = new_speed

        if self.rect.top < 0:
            self.rect.top = 0
            self.speed = 0

    def jump(self, pipes):
        inputs = self.get_inputs(pipes)
        val = self.nnet.get_max_value(inputs)
        if val > JUMP_CHANCE:
            self.speed = BIRD_START_SPEED

    def draw(self):
        self.gameDisplay.blit(self.img, self.rect)

    def check_status(self, pipes):
        if self.rect.bottom > DISPLAY_H:
            self.state = BIRD_DEAD
        else:
            self.check_hits(pipes)

    def assign_collision_fitness(self, p):
        gap_y = 0
        if p.pipe_type == PIPE_UPPER:
            gap_y = p.rect.bottom + PIPE_GAP_SIZE / 2
        else:
            gap_y = p.rect.top - PIPE_GAP_SIZE / 2

        self.fitness = -(abs(self.rect.centery - gap_y))

    def check_hits(self, pipes):
        for p in pipes:
            if p.rect.colliderect(self.rect):
                self.state = BIRD_DEAD
                self.assign_collision_fitness(p)
                break

    def update(self, dt, pipes):
        if self.state == BIRD_ALIVE:
            self.time_lived += dt
            self.move(dt)
            self.jump(pipes)
            self.draw()
            self.check_status(pipes)


    def get_inputs(self, pipes):

        closest = DISPLAY_W * 2 
        bottom_y = 0  
        for p in pipes:
            if p.pipe_type == PIPE_UPPER and p.rect.right < closest and p.rect.right > self.rect.left:
                closest = p.rect.right
                bottom_y = p.rect.bottom


        horizontal_distance = closest - self.rect.centerx
        vertical_distance = (self.rect.centery) - (bottom_y + PIPE_GAP_SIZE / 2)

        inputs = [
            ((horizontal_distance / DISPLAY_W) * 0.99) + 0.01,
            ((( vertical_distance + Y_SHIFT) / NORMALIZER ) * 0.99 ) + 0.01
        ]

        return inputs



class BirdCollection():

    def __init__(self, gameDisplay):
        self.gameDisplay = gameDisplay
        self.birds = []
        self.create_new_generation()

    def create_new_generation(self):
        self.birds = []
        for i in range(0, GENERATION_SIZE):
            self.birds.append(Bird(self.gameDisplay))

    def update(self, dt, pipes):
        num_alive = 0
        for b in self.birds:
            b.update(dt, pipes)
            if b.state == BIRD_ALIVE:
                num_alive += 1

        return num_alive

    def evolve_population(self):

        for b in self.birds:
            b.fitness += b.time_lived * PIPE_SPEED

        self.birds.sort(key=lambda x: x.fitness, reverse=True)

        for b in self.birds[0:10]:
            print('fitness:', b.fitness)

        self.create_new_generation()


















