import pygame
from pygame.locals import *
import sys 
import os
import numpy as np
import scipy as sp
from scipy import interpolate

from .particle import Particle

class Stage():

    def __init__(self, game, potential, initial_conditions=None,
        goal=None, level_options=None, events=None):

        self.game = game
        self.game._level_reset()

        # set goal and level options
        if level_options is None:
            self.level_options = ['ESC', 'LEFT', 'RIGHT', 'UP',
                'DOWN', 'X', 'P', 'G']
        else:
            self.level_options = level_options
        game._level_options = self.level_options
        self.goal = goal
        game._goal = goal

        self.events = events

        # generate the particle
        particle = Particle(potential=potential)
        particle.calculate_wave_functions()

        # set initial conditions if given 
        if initial_conditions is not None:

            # set initial energy condition
            if 'n' in initial_conditions:
                C = np.zeros_like(particle.C)
                C[initial_conditions['n']-1] = 1
                particle.C = C
                particle.average_energy = particle.energies[
                    initial_conditions['n']-1]

        self.particle = particle

        # some checks
        self._n_events = 0
        self._completed = False

    def run(self, *args):

        particle = self.particle
        game = self.game

        self.occurances = {'RIGHT': 0,
                           'LEFT': 0,
                           'UP': 0,
                           'DOWN': 0,
                           'X': 0,
                           'P': 0,
                           'G': 0,
                           'EVENT': 0,
                           'TIME': 0}
        self.last_occurance = self.occurances.copy()

        self.running = True
        while self.running:

            # fill screen with white 
            game.screen.fill((255,255,255))

            # advance game and particle times 
            game.time += game.dt
            particle.time = game.time
            self.occurances['TIME'] += 1 / game.fps

            # get and plot the wave function
            psi = particle.get_wave_function(particle.C, game.time)
            game.plot_wave_function(particle, psi)
            game.draw_bottom_bar()
    
            # listen to game events
            for event in pygame.event.get():
    
                # quit the game if requested
                if event.type == QUIT:
                    game.quit()
    
                # check key events
                elif event.type == KEYDOWN or event.type == pygame.MOUSEBUTTONUP:
    
                    # get selection
                    selection = self.get_selection(event)
    
                    # if the x key is pressed - position collapse
                    if selection == 'X':
                        C_new, x0, k0 = particle.position_momentum_collapse(
                                            psi, momentum=False)
                        game.collapse_animation(particle, particle.C, C_new)
                        particle.C = C_new
                        game.time = 0

                        # check whether goal is achieved
                        if self.goal is not None and 'position' in self.goal:
                            if (self.goal['position'][0] <= x0
                               <= self.goal['position'][1]):
                                self.level_completed()

                    # if the P key is pressed - momentum collapse            
                    elif selection == 'P':
                        C_new, x0, k0 = particle.position_momentum_collapse(
                                            psi, momentum=True)
                        game.collapse_animation(particle, particle.C, C_new)
                        particle.C = C_new
                        game.time = 0

                        # check whether goal is achieved
                        if self.goal is not None and 'position' in self.goal:
                            if (self.goal['position'][0] <= x0
                               <= self.goal['position'][1]):
                                self.level_completed()

                    # if the G key is pressed - return to the ground state
                    elif selection == 'G':
                        C_new = np.zeros((particle.nmax))
                        C_new[0] = 1
                        game.collapse_animation(particle, particle.C, C_new)
                        particle.C = C_new
                        game.time = 0

                        # check whether goal is achieved
                        if self.goal is not None and 'energy' in self.goal:
                            if self.goal['energy'][0] <= e0 <= self.goal['energy'][1]:
                                self.level_completed()

                    # if the RIGHT key is pressed - speed up
                    elif selection == 'RIGHT':
                        game.dt *= 2.0
    
                    # if the LEFT key is pressed - slow down
                    elif selection == 'LEFT':
                        game.dt /= 2.0
    
                    # if the UP key is pressed - increased energy quantum
                    elif selection == 'UP':
                        C_new, e0 = particle.energy_collapse(n_change=1)
                        game.collapse_animation(particle, particle.C, C_new)
                        particle.C = C_new
                        game.time = 0

                        # check whether goal is achieved
                        if self.goal is not None and 'energy' in self.goal:
                            if self.goal['energy'][0] <= e0 <= self.goal['energy'][1]:
                                self.level_completed()

                    # if the DOWN key is pressed - decrease energy quantum
                    elif selection == 'DOWN':
                        C_new, e0 = particle.energy_collapse(n_change=-1)
                        game.collapse_animation(particle, particle.C, C_new)
                        particle.C = C_new
                        game.time = 0
    
                        # check whether goal is achieved
                        if self.goal is not None and 'energy' in self.goal:
                            if self.goal['energy'][0] <= e0 <= self.goal['energy'][1]:
                                self.level_completed()

                    # if the ESC key is pressed - exit the wave function
                    elif selection == 'ESC':
                        self.running = False

                    # count occurances of a key
                    if selection is not None:
                        try:
                            self.occurances[selection] += 1
                        except KeyError:
                            pass

                # check if user changed the video size
                elif event.type == pygame.VIDEORESIZE:
                    game.resize(event.w, event.h)
                    game.screen.fill((255,255,255))
   
            if self.events is not None:
                # check for events
                self.check_event()

            # update and tick clock
            pygame.display.flip()
            game.clock.tick(game.fps)


        # reset the game level parameters
        game._level_reset()

        return self._completed

    def check_event(self):

        try:
            current_event = self.events[self.occurances['EVENT']]
        except IndexError:
            return

        if ((self.occurances[current_event[0]] - self.last_occurance[current_event[0]])
            >= current_event[1]):
            self.popup_text(current_event[2])

            self.last_occurance = self.occurances.copy()
            self.occurances['EVENT'] += 1

    def get_selection(self, event):

        keys = {'X': pygame.K_x,
                'P': pygame.K_p,
                'G': pygame.K_g,
                'LEFT': pygame.K_LEFT,
                'RIGHT': pygame.K_RIGHT,
                'UP': pygame.K_UP,
                'DOWN': pygame.K_DOWN,
                'ESC': pygame.K_ESCAPE}

        if event.type == KEYDOWN:
            for key in keys:
                if event.key == keys[key] and key in self.level_options:
                    return key
    
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.game._button_selected in self.level_options:
                return self.game._button_selected

    def level_completed(self):
        self.popup_text(['LEVEL COMPLETED!'])
        self.running = False
        self._completed = True

    def popup_text(self, words):

        game = self.game

        background_color = (45,15,70)
        font_color = (240,240,240)

        self._n_events += 1

        show_text = True
        while show_text:

            # listen to game events
            for event in pygame.event.get():

                # quit the game if requested
                if event.type == QUIT: game.quit()

                # check if user changed the video size
                if event.type == pygame.VIDEORESIZE:
                    game.resize(event.w, event.h)
                    game.screen.fill((255,255,255)) 

                # check key events
                if event.type == KEYDOWN or event.type == pygame.MOUSEBUTTONUP:
                    show_text = False

            # get popup size and location
            dimensions = (game.width * 0.05, game.height * 0.35,
                          game.width * 0.9, game.height * 0.3)
            border_radius = int(min(game.width*0.9, game.height*0.3) * 0.1)

            # add popup to screen
            popup = pygame.draw.rect(game.screen, background_color, dimensions,
                border_radius=border_radius)

            # get text size and locations
            max_width = game.width * 0.8
            max_height = game.height * 0.25
            xstart = game.width * 0.1
            ystart = game.height * 0.375
            x = xstart + 0
            y = ystart + 0

            # blit text to screen
            space = game.text_font.size(' ')[0]  # The width of a space.
            for line in words:
                for word in line.split():
                    word_surface = game.text_font.render(word, True, font_color)
                    word_width, word_height = word_surface.get_size()
                    if x + word_width >= max_width:
                        x = xstart + 0  # Reset the x.
                        y += word_height  # Start on new row.
                    game.screen.blit(word_surface, (x, y))
                    x += word_width + space
                x = xstart + 0  # Reset the x.
                y += word_height  # Start on new row.

            y += word_height  # Start on new row.

            # add white rectangle at the bottom
            bottom_bar = pygame.draw.rect(game.screen, (255,255,255),
                (0, game.height*0.9, game.width, game.height*0.1))

            # add "press any key to continue" at the bottom
            word_surface = game.text_font.render('Press any key to continue...', True,
                (0,0,0))
            word_width, word_height = word_surface.get_size()
            game.screen.blit(word_surface, (game.width*0.05,
                game.height * 0.95 - word_height/2))

            # update the screen
            pygame.display.update()
