import pygame
from pygame.locals import *
import sys
import os
import numpy as np

from qpias.buttons import Buttons


class Menu():
    def __init__(self, game, options, show=None, font=None):

        self.game = game
        self.show = show

        # turn options into texts and functions
        self.button_texts = []
        self.button_funcs = []
        self.button_args = []
        for i in range(len(options)):
            self.button_texts.append(options[i][0])
            self.button_funcs.append(options[i][1])
            if len(options[i]) == 3:
                self.button_args.append(options[i][2])
            else:
                self.button_args.append([])

        # create buttons and set background color
        self.buttons = Buttons(game, self.button_texts, show=show, font=font)
        self.background_color = game.get_background_color

    def run(self):

        in_menu = True
        while in_menu:

            # listen to game events
            for event in pygame.event.get():

                # quit the game if requested
                if event.type == QUIT:
                    self.game.quit()

                # check if user changed the video size
                if event.type == pygame.VIDEORESIZE:
                    self.game.resize(event.w, event.h)

                # check key events
                if event.type == KEYDOWN:

                    if event.key == pygame.K_ESCAPE:
                        in_menu = False

                    if event.key == pygame.K_DOWN:
                        self.buttons.select_next()

                    if event.key == pygame.K_UP:
                        self.buttons.select_previous()

                # run function from selected option
                if ( event.type == pygame.MOUSEBUTTONUP or
                   (event.type == KEYDOWN and event.key == pygame.K_RETURN)):

                    if self.button_funcs[self.buttons.selected] == 'EXIT':
                        in_menu = False
                    elif self.button_funcs[self.buttons.selected] is None:
                        print ('NOT YET IMPLIMENTED!')
                    else:
                        self.button_funcs[self.buttons.selected](self.game,
                            *self.button_args[self.buttons.selected])

            # fill screen with a color
            self.game.screen.fill(self.background_color)

            # update buttons
            self.buttons.update()

            # updates the frames of the game 
            pygame.display.flip()
            self.game.clock.tick(self.game.fps)


def main_menu(game):
    '''The main menu in pygame'''

    from qpias.title import title_screen
    from qpias.adventure import adventure_mode
    from qpias.sandbox import sandbox_information

    # show the title screen
    title_screen(game)

    options = [['ADVENTUDE MODE', adventure_mode],
               ['MODEL POTENTIALS', potentials_menu],
               ['SANDBOX MODE', sandbox_information],
               ['HOW TO PLAY', how_to_menu],
               ['QUIT', game.quit]]

    menu = Menu(game, options)
    menu.run()


def potentials_menu(game):

    from qpias.stage import Stage

    particle_box = Stage(game, None)
    harmonic_oscillator = Stage(game, game.harmonic_oscillator_potential)
    morse_potential = Stage(game, game.morse_potential)
    coulombic_potential = Stage(game, game.coulombic_potential)
    tunneling = Stage(game, game.barrier_potential)

    options = [['PARTICLE-in-a-BOX', particle_box.run],
               ['HARMONIC OSCILLATOR', harmonic_oscillator.run],
               ['MORSE POTENTIAL', morse_potential.run],
               ['1-D COULOMBIC', coulombic_potential.run],
               ['FINITE BARRIER', tunneling.run],
               ['BACK', 'EXIT']]

    menu = Menu(game, options)
    menu.run()


def how_to_menu(game):

    background_color = game.get_background_color

    welcome_text = ("Welcome to Quantum Particle-in-a-Sandbox, where "
                    "you explore what happens to a 1-dimensional "
                    "quantum mechanical wave function.")

    keys_text = ("Keys:\n"
                 "[Esc] - Return to previous screen.\n"
                 "[Right Arrow] - Speed up animation.\n"
                 "[Left Arrow] - Slow down animation.\n"
                 "[Up Arrow] - Increase energy of wave function.\n"
                 "[Down Arrow] - Decrease energy of wave function.\n"
                 "[g] - Collapse to the ground-state wave function.\n"
                 "[x] - Collapse to a position wave function.\n"
                 "[p] - Collapse to a momentum wave function.\n")

    texts = [welcome_text, keys_text]

    in_menu = True
    while in_menu:

        # listen to game events
        for event in pygame.event.get():

            # quit the game if requested
            if event.type == QUIT:
                game.quit()

            # check if user changed the video size
            if event.type == pygame.VIDEORESIZE:
                game.resize(event.w, event.h)

            # check key events
            if event.type == KEYDOWN:

                if event.key == pygame.K_ESCAPE: in_menu = False

        # fill screen with a color
        game.screen.fill(background_color)

        game.blit_texts(texts)

        # updates the frames of the game 
        pygame.display.flip()
        game.clock.tick(game.fps)
