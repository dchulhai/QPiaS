#!/usr/bin/env python3

from qpias.game import Game
from qpias.menu import main_menu

def Start_Game(dpi=96, width=800, height=600, dt=1e-4, fps=60):
    """Starts the QPiaS game.

    :param dpi: Dots-per-inch, default 96
    :type dpi: int, optional

    :param width: Screen width in pixels, default 800
    :type width: int, optional

    :param height: Screen height in pixels, default 600
    :type height: int, optional

    :param dt: Game time step, default 1e-4
    :type dt: float, optional

    :param fps: Frames-per-second, default 60
    :type fps: int, optional

    **Example**::

        >>> import qpias
        >>> qpias.run.Start_Game()
    """

    # set up the game
    game = Game(dpi=dpi, width=width, height=height, dt=dt, fps=60)

    # start the game in the main menu
    main_menu(game)

if __name__ == '__main__':
    Start_Game()
