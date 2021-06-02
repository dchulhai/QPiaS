#!/usr/bin/env python3

from qpias.game import Game
from qpias.menu import main_menu

def start_game(dpi=96, width=800, height=600, dt=1e-4, fps=60):

    # set up the game
    game = Game(dpi=dpi, width=width, height=height, dt=dt, fps=60)

    # start the game in the main menu
    main_menu(game)

if __name__ == '__main__':
    start_game()
