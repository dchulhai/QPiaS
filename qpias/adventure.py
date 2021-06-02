import sys 
import os

import pygame
from pygame.locals import *
import numpy as np
import scipy as sp
from scipy import interpolate

from qpias.stage import Stage
from qpias.menu import Menu

def adventure_mode(game):

    options = [['1 - Energy tutorial', energy_tutorial],
               ['2 - Position tutorial', position_tutorial],
               ['3 - Momentum tutorial', None],
               ['4 - Break a bond', bond_breaking],
               ['5 - Tunneling', tunneling],
               ["6 - Schrodinger's cat/particle", schrodinger_cat],
               ['7 - Climb up the stairs', climb_the_stairs],
               ['8 - Jump down the well', down_the_well],
               ['9 - ???', cliff],
               ['10 - ???', None],
               ['Back', 'EXIT']]

    menu = Menu(game, options, show=game._show_levels, font=game.adventure_menu_font)
    menu.run()


def energy_tutorial(game):

    goal = {'energy': [1979.9, 2262.7]}
    level_options = ['ESC', 'LEFT', 'RIGHT', 'UP', 'DOWN', 'G']

    events = [('TIME', 0, ['Welcome to the energy tutorial!',
                            'On this screen, you will see a particle in '
                             'a harmonic oscialltor potential.']),
              ('TIME', 1, ['Pretty boring, right? Try pressing the [RIGHT] '
                           'key to speed things up.']),
              ('RIGHT', 3, ['The [RIGHT] and [LEFT] keys will speed up or '
                            'slow down the animation.']),
              ('TIME', 1, ["This wave function still doesn't do much "
                           "because it's a 'stationary state'. 'Stationary' "
                           "means that its properties don't change with time."]),
              ('TIME', 1, ["We can see the properties of this particle in the bar "
                           "above the graph."]),
              ('TIME', 1, ["We can change this stationary state to another stationary "
                           "state by pressing the [UP] or [DOWN] keys."]),
              ('UP', 2, ["[UP] and [DOWN] correspond to absorbing or emitting "
                         "a discrete amount of energy. "
                         "To complete the level, try to match your particle's "
                         "energy with the green bar."]),
              ]

    stage = Stage(game, game.harmonic_oscillator_potential,
        initial_conditions={'n': 3}, goal=goal, level_options=level_options,
        events=events)
    completed = stage.run()

    # make the next stage available
    if completed:
        if game._levels_available == 1:
            game._levels_available += 1
            game._show_levels[game._levels_available-1] = True

def position_tutorial(game):

    goal = {'position': [0.75, 0.95]}
    level_options = ['ESC', 'LEFT', 'RIGHT', 'X']

    events = [('TIME', 0, ["This level has your particle in a box without "
                           "a potential inside of it. You goal is to collapse the "
                           "position of the particle within the green region by "
                           "pressing the [X] key."]),
              ('X', 1, ["When you collapse the position, the uncertainty in your "
                        "particle's momentum is very high, and therefore your particle "
                        "spreads out in both directions."]),
              ('X', 2, ["Notice also that your energy is now undefined. "
                        "This is because your particle is in a superposition of "
                        "energy eigenstates."]),
              ('X', 1, ["How can your energy be undefined? Well, to collpase the "
                        "position, you need to interact with another particle. "
                        "Your energy becomes entangled with this other "
                        "particle's energy."]),
              ('X', 2, ["Try to collapse your position to within the green "
                        "region to complete this level."]),
              ('X', 5, ["Where the particle collapses to is entirely random based on "
                        "the square of the wave function. So this part can be "
                        "frustrating..."]),
              ('X', 5, ["You can do it!"]),
              ('X', 5, ["You almost got it there!"]),
              ('X', 5, ["Try to wait until your probability density distribution "
                        "is large near the green region. Remember that you "
                        "can speed up or slow down the animation."]),
              ('X', 5, ["You should win an award for your persistance!"]),
             ]

    stage = Stage(game, None, initial_conditions={'n': 1}, goal=goal,
            level_options=level_options, events=events)
    completed = stage.run()

    # make the next stage available
    if completed:
        if game._levels_available == 2:
            game._levels_available += 1
            game._show_levels[game._levels_available-1] = True


def bond_breaking(game):

    goal = {'position': [0.8, 1]}
    level_options = game._all_level_options
    events = [('TIME', 0, ["Let's try to break a chemical bond using "
                           "a Morse potential!"])]

    stage = Stage(game, game.morse_potential, initial_conditions={'n': 1},
        goal=goal, level_options=level_options, events=events)
    completed = stage.run()

    # make the next state available
    if completed and game._levels_available == 4:
        game._levels_available += 1
        game._show_levels[game._levels_available-1] = True

def tunneling(game):

    goal = {'position': [0.7, 0.9]}
    level_options = ['ESC', 'LEFT', 'RIGHT', 'X', 'P', 'G']

    events = [('TIME', 0, ["Let's see it's possible to tunnel "

                           "through a potential barrier!"]),
              ('X', 15, ["If tunneling was easy, everyone would do it!"]),
              ('G', 15, ["I think your particle has the momentum this time, "
                         "I can feel it!"]),
             ]

    stage = Stage(game, game.barrier_potential, initial_conditions={'n': 1},
        goal=goal, level_options=level_options, events=events)
    completed = stage.run()

    # make the next state available
    if completed and game._levels_available == 5:
        game._levels_available += 1
        game._show_levels[game._levels_available-1] = True


def schrodinger_cat(game):

    goal = {'position': [0.1, 0.3]}
    level_options = ['ESC', 'LEFT', 'RIGHT', 'X', 'P', 'G']

    events = [('TIME', 0, ["Is the particle on the left or on the right? "
                           "You won't know until you collapse the wave function! "
                           "(HINT: You can always go back to the [G]round state if "
                           "necessary!)"])]

    potential = np.zeros((1001))
    potential[400:601] = 10000

    stage = Stage(game, potential, initial_conditions={'n': 1}, 
        goal=goal, level_options=level_options, events=events)
    completed = stage.run()

    # make the next state available
    if completed and game._levels_available == 6:
        game._levels_available += 1
        game._show_levels[game._levels_available-1] = True


def climb_the_stairs(game):

    goal = {'position': [0.85,0.95]}
    level_options = ['ESC', 'LEFT', 'RIGHT', 'DOWN', 'X', 'P', 'G']

    events = [('TIME', 0, ["Can a quantum particle climb stairs?"])]

    potential = np.zeros((1001))
    potential[200:400] = 1000
    potential[400:600] = 2000
    potential[600:800] = 3000
    potential[800:]    = 4000

    stage = Stage(game, potential, initial_conditions={'n': 1},
        goal=goal, level_options=level_options, events=events)
    completed = stage.run()

    # make the next state available
    if completed and game._levels_available == 7:
        game._levels_available += 1
        game._show_levels[game._levels_available-1] = True

def down_the_well(game):

    goal = {'position': [0.47, 0.53]}
    level_options = ['ESC', 'LEFT', 'RIGHT', 'UP', 'X', 'P']

    events = [('TIME', 0, ["Sometimes it's difficult to go places where "
                           "the potential is low because you just have too "
                           "much energy and no way to loose it!"])]

    potential = np.zeros((1001)) + 4000
    potential[450:551] = 0

    stage = Stage(game, potential, initial_conditions={'n': 5},
        goal=goal, level_options=level_options, events=events)
    completed = stage.run()

    # make the next state available
    if completed and game._levels_available == 8:
        game._levels_available += 1
        game._show_levels[game._levels_available-1] = True

def cliff(game):

    goal = {'position': [0.47, 0.53]}
#    level_options = ['ESC', 'LEFT', 'RIGHT', 'UP', 'X', 'P']
    level_options = game._all_level_options

    events = [('TIME', 0, ["Sometimes it's difficult to go places where "
                           "the potential is low because you just have too "
                           "much energy and no way to loose it!"])]

    potential = np.zeros((1001))
    potential[:200] = 5000

    stage = Stage(game, potential, initial_conditions={'n': 27},
        goal=goal, level_options=level_options, events=events)
    completed = stage.run()

    # make the next state available
    if completed and game._levels_available == 9:
        game._levels_available += 1
        game._show_levels[game._levels_available-1] = True
