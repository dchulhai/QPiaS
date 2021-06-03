import pygame
from pygame.locals import QUIT, VIDEORESIZE, KEYDOWN, MOUSEBUTTONUP
from pygame.locals import MOUSEMOTION
import numpy as np
import scipy as sp
from scipy import interpolate

from qpias.stage import Stage

def sandbox_information(game):

    welcome_text = ("Welcome to the Sandbox. Here you can draw any "
                    "1-dimensional potential and watch how the quantum "
                    "wave function evolves in this potential.")

    sandbox_help = ("On the next screen, [CLICK] and move your mouse "
                    "to draw a 1-dimensional potential. Press [ENTER] after "
                    "you've drawn your potential to see the wave function.")

    keys_text = ("Keys:\n"
                 "[Esc] - Return to the Main Menu.\n"
                 "[ANY] - Proceed to the next screen.")

    texts = [welcome_text, sandbox_help, keys_text]

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
            if event.type == KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    in_menu = False
                else:
                    sandbox_potential(game)

            if event.type == MOUSEBUTTONUP:
                sandbox_potential(game)

        # fill screen with a color
        game.screen.fill((35,25,60))

        game.blit_texts(texts)

        # updates the frames of the game 
        pygame.display.flip()
        game.clock.tick(game.fps)

def sandbox_potential(game):

    line_positions = []

    text = ["Draw the potential you'd like to use using the mouse. Press [ENTER] "
            "when done."]

    # fill screen with white
    game.screen.fill((255, 255, 255))
    game.blit_texts(text, color=(200,0,0))

    height = game.height

    # temporary potential
    potential = np.zeros((game.width+1))
    x = np.linspace(0,1,game.width+1)
    pen = int(game.width / 50.)

    in_sandbox_potential = True
    while in_sandbox_potential:


        # listen to game events
        for event in pygame.event.get():

            # quit the game if requested
            if event.type == QUIT:
                game.quit()

            # check if user changed the video size
            if event.type == VIDEORESIZE:
                game.resize(event.w, event.h)
                game.screen.fill((255,255,255))
                pen = int(game.width / 50.)
                height = game.height

                x_new = np.linspace(0,1,game.width+1)
                func = sp.interpolate.interp1d(x, potential, kind='nearest')
                potential = func(x_new)
                x = x_new

                for i in range(len(potential)):
                    pygame.draw.line(game.screen, (0,0,0),
                        (int(x[i]*game.width), int(height - potential[i]*height)),
                        (int(x[i]*game.width), game.height), pen)

            # check key events
            if event.type == KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    in_sandbox_potential = False

                # ENTER key saves the potential and calculates the wave function
                if event.key == pygame.K_RETURN:
                    x_new = np.linspace(0,1,1000)
                    func = sp.interpolate.interp1d(x, potential, kind='cubic')
                    potential = func(x_new)
                    stage = Stage(game, potential*10000)
                    stage.run()
                    potential = np.zeros((game.width+1))

                    # reset some things when you return to this screen
                    game.screen.fill((255,255,255))

            # check for mouse motion
            if event.type == MOUSEMOTION:
                if event.buttons[0]: # left mouse button:

                    potential[np.where((x>=(event.pos[0]-pen/2)/game.width)&
                        (x<=(event.pos[0]+pen/2)/game.width))] = (
                        (height - event.pos[1]) / height)

                    pygame.draw.line(game.screen, (0,0,0),
                        event.pos, (event.pos[0],game.height), pen)
                    pygame.draw.line(game.screen, (255,255,255),
                        (event.pos[0],0), event.pos, pen)

        game.blit_texts(text, color=(200,0,0))

        # update and tick clock
        pygame.display.flip()
        game.clock.tick(game.fps)

