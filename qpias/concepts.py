import numpy as np

import pygame
from pygame.locals import QUIT, VIDEORESIZE, KEYDOWN, MOUSEBUTTONUP

from qpias.stage import Stage
from qpias.menu import Menu

def concepts_mode(game):

    options = [['1 - Quanta', lvl_quanta],
               ['2 - Box length', lvl_box_length],
               ["3 - Schrodinger's cat", lvl_schrodinger_cat],
               ['4 - Uncertainty principle', lvl_uncertainty_principle],
               ['5 - Tunneling', lvl_tunneling],
               ['Back', 'EXIT']]

    menu = Menu(game, options, show=game._show_levels)
    menu.run()


def lvl_quanta(game):

    # first sub-level
    if (game._levels_completed['QUANTA'] == 0 or
        game._levels_completed['QUANTA'] > 1):

        goal = {'energy': [1979.9, 2262.7]}
        level_options = ['ESC', 'LEFT', 'RIGHT', 'UP', 'DOWN', 'G']

        events = [('TIME', 0, ["Welcome to the energy tutorial! "
                           "On this screen, you will see a particle in "
                           "a harmonic oscillator potential. "
                           "Your goal is to match the particle's energy "
                           "to the green bar."]),
              ('TIME', 1, ['Pretty boring, right? Try pressing the [RIGHT] '
                           'key to speed things up.']),
              ('RIGHT', 1, ['The [RIGHT] and [LEFT] keys will speed up or '
                            'slow down the animation.']),
              ('LEFT', 1, ['The [RIGHT] and [LEFT] keys will speed up or '
                           'slow down the animation.']),
              ('TIME', 10, ["This wave function still doesn't do much "
                            "because it's a 'stationary state'. 'Stationary' "
                            "means that its properties don't change with time."]),
              ('TIME', 1, ["We can see the properties of this particle in the region "
                           "above the graph."]),
              ('TIME', 1, ["We can change this stationary state to another stationary "
                           "state by pressing the [UP] or [DOWN] keys."]),
              ('UP', 2, ["[UP] and [DOWN] correspond to absorbing or emitting "
                         "a discrete (or fixed) amount of energy. "
                         "Notice that you move up or down in chunks of energy."]),
              ('TIME', 1, ["To complete the level, try to match your particle's "
                           "energy to the energy of the green region."]),
              ]

        stage = Stage(game, game.harmonic_oscillator_potential,
            initial_conditions={'n': 4}, goal=goal, level_options=level_options,
            events=events)
        sublevel_completed = stage.run()
        if sublevel_completed: game._levels_completed['QUANTA'] += 1

    # second sub-level
    if game._levels_completed['QUANTA'] >= 1:
        goal = {'energy': [2200, 2350]}
        level_options = ['ESC', 'LEFT', 'RIGHT', 'UP', 'DOWN', 'G']

        events = [('TIME', 0, ["This time, try to collapse the energy "
                               "to the new green region "]),
                  ('UP', 5, ["Did you skip past it?"]),
                  ('UP', 1, ["Notice that you cannot match exactly "
                             "that energy! This is because the particle "
                             "can only have specific energies."]),
                  ('UP', 1, "EXIT"),
                 ]

        stage = Stage(game, game.harmonic_oscillator_potential,
            initial_conditions={'n': 4}, goal=goal, level_options=level_options,
            events=events)
        sublevel_completed = stage.run()
        game._levels_completed['QUANTA'] += 1

    # make the next stage available
    if game._levels_completed['QUANTA'] >= 2:
        if game._levels_available == 1:
            game._levels_available += 1
            game._show_levels[game._levels_available-1] = True


def lvl_box_length(game):

    # first sublevel
    if (game._levels_completed['LENGTH'] == 0 or
        game._levels_completed['LENGTH'] > 3):

        goal = None
        level_options = ['ESC', 'LEFT', 'RIGHT', 'UP', 'DOWN', 'G', 'E']

        events = [('TIME', 0, ["Let's explore a box that's a bit narrow."]),
                  ('UP', 1, ["Notice how far apart the energies are. "
                             "You can see all possible energies by "
                             "pressing the [E] key."])]

        stage = Stage(game, None, initial_conditions={'length': 0.4, 'emax': 400},
            goal={'energy': [200,300]}, level_options=level_options, events=events)
        sublevel_completed = stage.run()
        if sublevel_completed: game._levels_completed['LENGTH'] += 1

    # second sublevel
    if (game._levels_completed['LENGTH'] == 1 or
        game._levels_completed['LENGTH'] > 3): 

        goal = None
        level_options = ['ESC', 'LEFT', 'RIGHT', 'UP', 'DOWN', 'G', 'E']

        events = [('TIME', 0, ["Let's explore a box that's a bit longer."]),
                  ('UP', 1, ["Press [E] to see the possible energies."]),
                  ('E', 1, ["Do the energy spacings seem a bit closer together?"])]

        stage = Stage(game, None, initial_conditions={'length': 0.6, 'emax': 400},
            goal={'energy': [200,300]}, level_options=level_options, events=events)
        sublevel_completed = stage.run()
        if sublevel_completed: game._levels_completed['LENGTH'] += 1

    # third sublevel
    if (game._levels_completed['LENGTH'] == 2 or
        game._levels_completed['LENGTH'] > 3): 

        goal = None
        level_options = ['ESC', 'LEFT', 'RIGHT', 'UP', 'DOWN', 'G', 'E']

        events = [('TIME', 0, ["Let's explore an even longer box."]),
                  ('UP', 2, ["You can try counting how many times you need to "
                             "absorb a photon to get to the same energy. You "
                             "pressed [UP] twice, so far."])]

        stage = Stage(game, None, initial_conditions={'length': 0.8, 'emax': 400},
            goal={'energy': [200,300]}, level_options=level_options, events=events)
        sublevel_completed = stage.run()
        if sublevel_completed: game._levels_completed['LENGTH'] += 1

    # fourth sublevel
    if game._levels_completed['LENGTH'] >= 3:

        goal = None
        level_options = ['ESC', 'LEFT', 'RIGHT', 'UP', 'DOWN', 'G', 'E']

        events = [('TIME', 0, ["This is the largest box we can make. How many "
                               "photons do you need to absorb to get to the "
                               "required energy?"])]

        stage = Stage(game, None, initial_conditions={'length': 0.8, 'emax': 400},
            goal={'energy': [200,300]}, level_options=level_options, events=events)
        sublevel_completed = stage.run()
        if sublevel_completed: game._levels_completed['LENGTH'] += 1

    # make the next stage available
    if game._levels_completed['LENGTH'] >= 4:
        if game._levels_available == 2:
            game._levels_available += 1
            game._show_levels[game._levels_available-1] = True


def lvl_schrodinger_cat(game):

    # first sublevel
    if (game._levels_completed['CAT'] == 0 or
        game._levels_completed['CAT'] > 1):

        goal = {'position': [0.2, 0.4]}

        level_options = ['ESC', 'LEFT', 'RIGHT', 'UP', 'DOWN', 'X', 'G', 'E']

        events = [('TIME', 0, ["Where is our particle? "
                               "The square of the wave function (blue region) "
                               "gives the probability of finding the particle."]),
                  ('TIME', 0, ["Not until you try to find the position of "
                               "the particle by pressing [X] does it 'decide' "
                               "where it is."]),
                  ('TIME', 0, ["Try to collapse your particle's position to "
                               "somewhere in the green region by pressing [X]."]),
                  ('X', 1, ["Notice that after you find the position, the particle "
                            "can now only be found in that one spot (until it moves "
                            "away). Measuring the position changes the wave function "
                            "of the particle."]),
                  ('TIME', 5, ["Keep trying to collapse the particle's position "
                               "in the green region by pressing [X]."]),
                  ('TIME', 10, ["HINT: You can always try changing your wave "
                                "function's energy by absorbing [UP] or emitting "
                                "[DOWN] a photon to change your probabilities or "
                                "press [G] to return to the ground state."])]

        stage = Stage(game, None, initial_conditions={'n': 5}, goal=goal,
            level_options=level_options, events=events)

        sublevel_completed = stage.run()
        if sublevel_completed: game._levels_completed['CAT'] += 1

    # second sublevel
    if game._levels_completed['CAT'] >= 1:
        goal = {'position': [0.1, 0.3]}
        level_options = ['ESC', 'LEFT', 'RIGHT', 'X', 'G', 'E']

        events = [('TIME', 0, ["Is the particle on the left or the right?"]),
                  ('TIME', 0, ["This is the famous Schrodinger's cat problem, "
                               "where the cat can be thought of as either alive "
                               "or dead, and not until you "
                               "collapse the wave function will you know which it is."]),
                  ('TIME', 0, ["Collapse the wave function by pressing [X]. You can "
                               "always return to the ground state by pressing [G]."]),
                  ('X', 3,    ["You can always return to the ground state by "
                               "pressing [G]."])]

        potential = np.zeros((1001))
        potential[400:601] = 50000

        stage = Stage(game, potential, initial_conditions={'n': 1}, 
            goal=goal, level_options=level_options, events=events)
        sublevel_completed = stage.run()
        if sublevel_completed: game._levels_completed['CAT'] += 1

    # make the next state available
    if game._levels_completed['CAT'] > 1:
        if game._levels_available == 3:
            game._levels_available += 1
            game._show_levels[game._levels_available-1] = True


def lvl_uncertainty_principle(game):

    # first sublevel
    if (game._levels_completed['UNCERTAINTY'] == 0 or
        game._levels_completed['UNCERTAINTY'] > 1):
        goal = {'position': [0.6, 0.73]}
        level_options = ['ESC', 'LEFT', 'RIGHT', 'P', 'G', 'S', 'E']

        events = [('TIME', 0, ["In which direction is the particle moving? "
                               "Press [P] to find the particle's momentum."]),
                  ('P', 1,    ["Notice that you no longer know the energy of the "
                               "particle. This is because it is in a 'superposition' "
                               "of energy states. Press [S] to show you the "
                               "complete superposition."]),
                  ('S', 1,    ["Press [S] to return to the standard view of the "
                               "particle."]),
                  ('S', 1,    ["Try to collapse the particle's position to within the "
                               "green region."]),
                  ('X', 3,    ["You can always return to the ground state by "
                               "pressing [G]."])]

        stage = Stage(game, None, initial_conditions={'n': 6},
            goal=goal, level_options=level_options, events=events)
        sublevel_completed = stage.run()
        if sublevel_completed: game._levels_completed['UNCERTAINTY'] += 1

    # second sublevel
    if game._levels_completed['UNCERTAINTY'] >= 1:
        goal = {'position': [0.2, 0.3]}
        level_options = ['ESC', 'LEFT', 'RIGHT', 'UP', 'DOWN', 'X', 'P', 'G', 'S', 'E']

        events = [('TIME', 0, ["Try to use all of the tools available to you in "
                               "order to collapse the position or momentum of the "
                               "particle to within the green region."]),
                  ('X', 1,    ["Notice that when you find the position of the particle, "
                               "the momentum (direction and speed of travel) is "
                               "completely unknown, so the particle spreads out in both "
                               "directions."]),
                  ('X', 2,    ["The certainty in the position leads to uncertainty in "
                               "the momentum --- this is the uncertainty principle."])]

        potential = np.zeros((1001)) + 500
        potential[200:301] = 600
        potential[600:701] = 0

        stage = Stage(game, potential, initial_conditions={'n': 1}, 
            goal=goal, level_options=level_options, events=events)
        sublevel_completed = stage.run()
        if sublevel_completed: game._levels_completed['UNCERTAINTY'] += 1

    # make the next state available
    if game._levels_completed['UNCERTAINTY'] > 1:
        if game._levels_available == 4:
            game._levels_available += 1
            game._show_levels[game._levels_available-1] = True


def lvl_tunneling(game):

    # first sublevel
    if (game._levels_completed['TUNNELING'] == 0 or
        game._levels_completed['TUNNELING'] > 1):
        goal = {'position': [0.7, 0.9]}
        level_options = ['ESC', 'LEFT', 'RIGHT', 'X', 'P', 'G', 'S']

        events = [('TIME', 0, ["If there is a potential barrier that's not too large, "
                               "there is a small chance to find the particle inside "
                               "the potential region, or even on the other side of the "
                               "barrier!"]),
                  ('TIME', 3, ["Try to collapse your particle's position on the other "
                               "side of the barrier. If you go through the barrier, "
                               "rather than over it, this is called tunneling."]),
                  ('X', 15, ["If tunneling was easy, everyone would do it!"]),
                  ('G', 15, ["I think your particle has the momentum this time, "
                             "I can feel it!"])]

        potential = np.zeros((501))
        potential[230:281] = 800 

        stage = Stage(game, potential, initial_conditions={'n': 9},
                      goal=goal, level_options=level_options, events=events)
        sublevel_completed = stage.run()
        if sublevel_completed: game._levels_completed['TUNNELING'] += 1

    # second sublevel
    if game._levels_completed['TUNNELING'] >= 1:
        goal = {'position': [0.7, 0.9]}
        level_options = ['ESC', 'LEFT', 'RIGHT', 'X', 'P', 'G', 'S']

        events = [('TIME', 0, ["Let's try tunneling through something with a "
                               "higher potential barrier!"]),
                  ('TIME', 10, ["Press [X] or [P] to collapse the position or "
                                "momentum of the particle to see if you made it "
                                "to the other side of the barrier!"]),
                  ('X', 15, ["If tunneling was easy, everyone would do it!"]),
                  ('G', 15, ["I think your particle has the momentum this time, "
                             "I can feel it!"])]

        potential = np.zeros((501))
        potential[230:281] = 1800
        stage = Stage(game, potential,
                      initial_conditions={'n': 9}, goal=goal,
                      level_options=level_options, events=events)
        sublevel_completed = stage.run()
        if sublevel_completed: game._levels_completed['TUNNELING'] += 1

    # display an all levels completed screen
    if game._levels_completed['TUNNELING'] > 1:
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
                    try:
                        if event.key == pygame.K_ESCAPE:
                            in_menu = False
                    except Exception:
                        pass

            # fill screen with a color
            game.screen.fill(game.get_background_color)

            game.blit_texts(["!!!CONGRATULATIONS!!!\nYou completed all the levels!",
                             "Press [ESC] to go back."])

            # updates the frames of the game 
            pygame.display.flip()
            game.clock.tick(game.fps/20)


def lvl_position_tutorial(game):

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


def lvl_momentum_tutorial(game):

    goal = {'energy': [1750, 2100]} 
    level_options = ['ESC', 'LEFT', 'RIGHT', 'DOWN', 'P', 'G', 'S']
    events = [('TIME', 0, ["Let's try to collapse the energy (by pressing "
                           "[DOWN]) to match the energy of the green region. "
                           "However, you can only increase your energy by "
                           "collapsing your momentum with [P]!"])]

    potential = np.abs(0.5 - np.linspace(0,1,1001)) * 5000
    stage = Stage(game, potential, initial_conditions={'n': 1},
        goal=goal, level_options=level_options, events=events)
    completed = stage.run()

    # make the next stage available
    if completed:
        if game._levels_available == 2:
            game._levels_available += 1
            game._show_levels[game._levels_available-1] = True


def lvl_bond_breaking(game):


    goal = {'position': [0.8, 1]}
    level_options = game._all_level_options
    events = [('TIME', 0, ["Let's try to break a chemical bond using "
                           "a Morse potential! Collapse the position "
                           "of the particle such that it is far away from the "
                           "source of the Morse potential"])]

    stage = Stage(game, game.morse_potential, initial_conditions={'n': 1},
        goal=goal, level_options=level_options, events=events)
    completed = stage.run()

    # make the next state available
    if completed and game._levels_available == 4:
        game._levels_available += 1
        game._show_levels[game._levels_available-1] = True


def lvl_climb_the_stairs(game):

    goal = {'position': [0.85,0.95]}
    level_options = ['ESC', 'LEFT', 'RIGHT', 'DOWN', 'X', 'P', 'G', 'S']

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


def lvl_down_the_well(game):

    goal = {'position': [0.47, 0.53]}
    level_options = ['ESC', 'LEFT', 'RIGHT', 'UP', 'X', 'P', 'S']

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

def lvl_cliff(game):

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
