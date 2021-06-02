import pygame
from pygame.locals import *
import sys 
import os
import numpy as np


def title_screen(game):

    texts = ['QUANTUM', 'PARTICLE', 'in a', 'SANDBOX']

    # text color
    color = (240, 240, 240)

    # fill the screen
    background_color = game.get_background_color
    game.screen.fill(background_color)

    def resize(game):
        # get the perfect font size
        size = int(40 * min(game.width, game.height) / 600.)
        font = pygame.font.Font(os.path.join(os.path.dirname(__file__),
               'fonts/chintzy.ttf'), size)
        word = font.render(' SANDBOX ', True, color)
        word_width, word_height = word.get_size()
#        size = min(game.height/(9*word_height), game.width/word_width)
        size = int(40 * min(game.width, game.height) / 600. *
                min(game.height/(9*word_height), game.width/word_width))
        font = pygame.font.Font(os.path.join(os.path.dirname(__file__),
               'fonts/chintzy.ttf'), size)
    
        # get the origin point for each word and letter
        word_origins = []
        letter_origins = []
        for i in range(len(texts)):
    
            # calculate word origin
            text = texts[i]
            word = font.render(text, True, color)
            word_width, word_height = word.get_size()
            word_origins.append((game.width/2 - word_width/2, (i*2+1)*game.height/9))
    
            # calculate each letter origin (x-pos only)
            letter_origin_x = []
            previous_letter_length = 0
            for i in range(len(text)):
                letter = font.render(text[i], True, color)
                l_w, l_h = letter.get_size()
                letter_origin_x.append(word_origins[-1][0] + previous_letter_length)
                previous_letter_length += l_w
            letter_origins.append(letter_origin_x)

        # get a smaller font size
        font_small = pygame.font.Font(os.path.join(os.path.dirname(__file__),
               'fonts/chintzy.ttf'), int(size/3))
        instruction = font_small.render('Press any key to continue...',
            True, (235,235,165))

        # return
        return font, instruction, word_origins, letter_origins, l_h

    font, instruction, word_origins, letter_origins, l_h = resize(game)

    # animate the "press any key..." instruction
    running = True
    t = 0
    while running:

        t += 1
        theta = t * np.pi / (2 * game.fps)
        game.screen.fill(background_color)

        # listen to game events
        for event in pygame.event.get():

            # quit the game if requested
            if event.type == QUIT:
                game.quit()

            # proceed to the next screen on keypress
            if event.type == KEYDOWN or event.type == pygame.MOUSEBUTTONUP:
                running = False

            # check if user changed the video size
            if event.type == pygame.VIDEORESIZE:
                game.resize(event.w, event.h)
                game.screen.fill(background_color)
                font, instruction, word_origins, letter_origins, l_h = resize(game)


        # wavy animation of all the words
        for j in range(len(texts)):

            text = texts[j]
            origin = word_origins[j]

            for i in range(len(text)):
                origin_x = letter_origins[j][i]
                origin_y = np.sin(theta) * np.sin(origin_x) * l_h / 2 + origin[1]
                letter = font.render(text[i], True, color)
                game.screen.blit(letter, (origin_x, origin_y))

        # animate the "press any key to continue..."
        alpha = abs(int(np.cos(theta) * 255))
        ins_w, ins_h = instruction.get_size()
        alpha_img = pygame.Surface((ins_w, ins_h), pygame.SRCALPHA)
        alpha_img.fill((255, 255, 255, alpha))
        ins_copy = instruction.copy()
        ins_copy.blit(alpha_img, (0,0), special_flags=pygame.BLEND_RGBA_MULT)
        game.screen.blit(ins_copy, (game.width/2 - ins_w/2, (8.5*game.height/9)
            - ins_h/2))

        pygame.display.flip()
        game.clock.tick(game.fps)

