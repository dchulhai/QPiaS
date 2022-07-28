import pygame
from pygame.locals import QUIT, VIDEORESIZE, KEYDOWN, MOUSEBUTTONUP

from qpias.buttons import Buttons


class Menu():
    """Creates a game menu with selectable text.

    :param game: A QPiaS Game object.
    :type game: :class:`qpias.game.Game`

    :param list options: A list of options available in the menu.

    """


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
                if event.type == VIDEORESIZE:
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
                if ( event.type == MOUSEBUTTONUP or
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
    from qpias.concepts import concepts_mode
    from qpias.sandbox import sandbox_information

    # show the title screen
    title_screen(game)

    options = [['CORE CONCEPTS', concepts_mode],
               ['MODEL POTENTIALS', potentials_menu],
               ['SANDBOX', sandbox_information],
               ['ABOUT', about_menu],
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


def about_menu(game):

    background_colors = []
    background_colors.append(game.get_background_color)

    welcome_text = ("Welcome to Quantum Particle-in-a-Sandbox, where "
                    "you explore what happens to a 1-dimensional "
                    "quantum mechanical wave function.\n\n"
                    "Quantum Particle-in-a-Sandbox was developed by Dhabih "
                    "V. Chulhai (chulhaid@uindy.edu) (c) 2022 and "
                    "may be used according to the Apache License v 2.0")

    instruction_text1 = ("Press [ESC] to return to the previous screen "
                         "or press any other key for more instruction.")

    instruction_text2 = ("Press [ESC] to return to the previous screen.")

    keys_text = ("Keys:\n"
                 "[Esc] - Return to previous screen.\n"
                 "[Right Arrow] - Speed up animation.\n"
                 "[Left Arrow] - Slow down animation.\n"
                 "[Up Arrow] - Collapse and increase energy.\n"
                 "[Down Arrow] - Collapse and decrease energy.\n"
                 "[X] - Collapse to a position.\n"
                 "[P] - Collapse to a momentum.\n"
                 "[G] - Collapse to the ground-state.\n"
                 "[S] - Show wave function as a superposition.\n"
                 "[E] - Show all energy eigenfunctions.\n")

    modes_text = ("CORE CONCEPTS - achieve certain goals by collapsing "
                  "your particle's energy (using [UP] or [DOWN]) to match the "
                  "green horizontal region or by collapsing your particle's "
                  "position (using [X] or [P]) to match the green vertical region.\n\n"
                  "MODEL POTENTIALS - explore the wave function in these commonly used "
                  "model potentials.\n\n"
                  "SANDBOX - draw your own potential, then see how the quantum "
                  "wave function evolves in this potential.")

    texts = [[welcome_text, instruction_text1],
             [keys_text, instruction_text1],
             [modes_text, instruction_text2]]

    # to keep tract of which informational screen is being shown
    current_layer = 0

    in_menu = True
    while in_menu:

        # listen to game events
        for event in pygame.event.get():

            # quit the game if requested
            if event.type == QUIT:
                game.quit()

            # check if user changed the video size
            if event.type == VIDEORESIZE:
                game.resize(event.w, event.h)

            # check key events
            if event.type == KEYDOWN or event.type == MOUSEBUTTONUP:

                # check for the [ESC] event
                escape = False
                try:
                    if event.key == pygame.K_ESCAPE:
                        escape = True
                except Exception:
                    pass

                # advance screen or go back
                if escape:
                    if current_layer == 0:
                        in_menu = False
                    else:
                        current_layer -= 1
                else:
                    if current_layer < len(texts)-1:
                        current_layer += 1
                    #if current_layer > 1: in_menu = False

        # fill screen with a color
        if current_layer == len(background_colors):
            background_colors.append(game.get_background_color)
        game.screen.fill(background_colors[current_layer])

        game.blit_texts(texts[current_layer])

        # updates the frames of the game 
        pygame.display.flip()
        game.clock.tick(game.fps)
