#!/usr/bin/env python3

import os
import sys

import pygame
from pygame.locals import QUIT, KEYDOWN, MOUSEBUTTONUP
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.backends.backend_agg as agg
import numpy as np
import scipy as sp

class Game():
    '''
    A class to store all the information about the game state.
    '''

    def __init__(self, dpi=96, width=800, height=600, dt=1e-4, fps=60):
        '''
        Initializes the game state.
        '''

        # set the size defaults
        self.dpi = dpi
        self.width = width
        self.height = height
        self._lw_ratio = 1/4.
        self.menu_font_size = 40
        self.adventure_menu_font_size = 26
        self.text_font_size = 40
        self.top_bar_font_size = 25

        # initialize pygame
        self.pygame = pygame.init()
        self.font = pygame.font.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.width,
                        self.height), pygame.RESIZABLE)
        pygame.display.set_caption('Quantum Particle-in-a-Sandbox')

        # initialize font objects
        self.menu_font = pygame.font.Font(self.resource_path('fonts/chintzy.ttf'),
                self.menu_font_size)
        self.adventure_menu_font = pygame.font.Font(
                self.resource_path('fonts/chintzy.ttf'), self.adventure_menu_font_size)
        self.text_font = pygame.font.Font(self.resource_path('fonts/ccr.ttf'),
                self.text_font_size)
        self.top_bar_font = pygame.font.Font(
                self.resource_path('fonts/instruction.ttf'), self.top_bar_font_size)

        # set up game timer
        self.time = 0
        self.dt = dt
        self.fps = fps

        # resize variables as needed
        self.resize(width, height)

        # set up the figure to plot
        self.figure = plt.figure(figsize=(self.plot_width,
                        self.plot_height), dpi=self.dpi)
        self.ax = self.figure.add_subplot(111)
        self.canvas = agg.FigureCanvasAgg(self.figure)
        plt.tight_layout()
        self.ax.set_facecolor((0.85,0.85,0.85))
        self.ax.tick_params(axis='both', which='both', bottom=False, top=False,
            labelbottom=False, right=False, left=False, labelleft=False)
        for axis in ['top', 'bottom', 'left', 'right']:
            self.ax.spines[axis].set_linewidth(self.lw*3)

        # other attributes
        # how often to calculate the wave function properties
        self.__properties_time = 0
        self.__properties_duration = 10 # recalculate every n frames

        # how long a wave function collapse takes
        self._collapse_time = 0.75 # in seconds?

        # show superposition waves
        self.superposition_mode = False

        # show all eigenvectors
        self.eigenvectors_mode = False

        # ADVENTURE MODE SPECIFIC VARIABLES
        self._level_reset()
        self._show_levels = [True] * 1 + [False] * 4 + [True]
        self._levels_available = 1
        self._levels_completed = {'QUANTA': 0,
                                  'LENGTH': 0,
                                  'CAT': 0,
                                  'UNCERTAINTY': 0,
                                  'TUNNELING': 0}


    def resource_path(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        # split relative path as needed
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.dirname(__file__)

        return os.path.join(base_path, relative_path)

    @property
    def _all_level_options(self):
        return ['ESC', 'LEFT', 'RIGHT', 'UP', 'DOWN', 'X', 'P', 'G', 'S', 'E'].copy()

    def plot_wave_function(self, particle, psi, average_energy=None):
        '''
        Plots the wave function to the screen.
        '''

        # some defaults
        ax = self.ax
        potential = particle.potential
        energies = particle.energies
        canvas = self.canvas
        x = particle.x

        ymax = 50#/particle.length

        # use the average energy to shift the wave function up/down 
        if average_energy is None:
            average_energy = particle.average_energy
        yshift = average_energy * ymax / particle._emax

        # clear/reset axis and set thickness of graph box
        ax.cla()
        ax.grid()
        ax.set_ylim((0,ymax))
        ax.set_xlim((x[0],x[-1]))
        if particle.length < 1.0:
            space = (1 - particle.length) / 2.
            ax.set_xlim((0,1))
            ax.fill_between([0,space], 10000, 0, color='#646464')
            ax.fill_between([space+x[-1],1], 10000, 0, color='#646464')
        else:
            space = 0

        # scale and plot the potential surface
        scaled_potential = potential * ymax / particle._emax
        ax.fill_between(x+space, scaled_potential, 0, color='#646464')

        # draw a green goal region if present
        goal = self._goal
        if goal is not None:
            if 'energy' in goal:
                emin = goal['energy'][0] * ymax / particle._emax
                emax = goal['energy'][1] * ymax / particle._emax
                ax.fill_between([x.min()+space,x.max()+space], [emin, emin],
                    [emax, emax], color='#2ca02c', alpha=0.5)
            if 'position' in goal:
                xmin = goal['position'][0]
                xmax = goal['position'][1]
                ax.fill_between([xmin+space, xmax+space], [ymax, ymax], 0,
                    color='limegreen', alpha=0.5)
 
        # prints the expectation values and uncertainties
        self.draw_top_bar(particle, psi, average_energy)

        if self.eigenvectors_mode:

            self.plot_eigenvectors(particle, ymax, space=space)

        elif self.superposition_mode:

            self.plot_superposition(particle, ymax, space=space)

        else:
 
            # plot the real and imaginary parts of the wave function
            ax.plot(x+space, psi.imag+yshift, color='tab:orange', lw=self.lw*4,
                label='$\\mathrm{Im}[\\Psi]$')
            ax.plot(x+space, psi.real+yshift, color='tab:red', lw=self.lw*4,
                label='$\\mathrm{Re}[\\Psi]$')

        # plot the probability density function
        if not self.eigenvectors_mode:
            psi_squared = (psi*psi.conjugate()).real
            ax.fill_between(x+space, yshift+psi_squared,
                yshift-psi_squared, color='tab:blue', lw=self.lw*4, alpha=0.8)

        # plot the graph to the surface/screen
        canvas.draw()
        renderer = canvas.get_renderer()
        raw_data = renderer.tostring_rgb()
        size = canvas.get_width_height()
        surf = pygame.image.fromstring(raw_data, size, "RGB")
        self.screen.blit(surf, self.plot_origin)


    def plot_superposition(self, particle, ymax, space, C=None):

        ax = self.ax
        x  = particle.x
        scale = ymax / particle._emax

        # get coefficients and probabilities
        if C is None: C = particle.Ct
        prob = (C.conjugate()*C).real

        # sort the probabilities
        indx = np.argsort(-prob)

        # plot the highest probability energy eigenfunctions
        for i in range(len(prob)):

            # get index and linewidth
            idx = indx[i]
            lw = self.lw * 4 * np.sqrt(prob[idx])

            # if the probability is small, don't show it
            if lw < 0.5: break

            # plot the axis
            energy = particle.energies[idx] * scale
            ax.plot(x+space, np.zeros_like(x)+energy, 'k-', lw=lw*0.3/4)

            # get and plot the wave function
            wf = C[idx] * particle.wave_functions[idx]
            ax.plot(x+space, wf.imag+energy, color='tab:orange', lw=lw)
            ax.plot(x+space, wf.real+energy, color='tab:red', lw=lw)


    def plot_eigenvectors(self, particle, ymax, space):

        ax = self.ax
        x = particle.x
        scale = ymax / particle._emax

        for i in range(len(particle.energies)):

            energy = particle.energies[i]
            if energy > particle._emax: continue

            energy *= scale

            ax.plot(x+space, np.zeros_like(x)+energy, 'k-', lw=0.3)

            c_temp = np.exp(-1j * particle.energies[i] * self.time)
            wf = c_temp * particle.wave_functions[i] / 2.0

            ax.plot(x+space, wf.real+energy, color='tab:orange', lw=2)
            ax.plot(x+space, wf.imag+energy, color='tab:green', lw=2)


    def draw_top_bar(self, particle, psi, average_energy, coefficient=None):

        # get the coefficient
        if coefficient is None:
            coefficient = particle.Ct

        # check if this is a well defined energy eigenstate
        C_length = (coefficient.conjugate()*coefficient).real
        if C_length.max() > 0.999:
            energy = particle.energies[np.where(C_length>0.999)][0]
        else:
            energy = None

        if self.__properties_time == 0:

            # calculate the average position
            self.__average_position = np.dot(coefficient.conjugate(),
                np.dot(particle._xmat, coefficient)).real

            # calculate position uncertainty
            temp = np.dot(coefficient.conjugate(), np.dot(particle._x2mat,
                    coefficient)).real
            self.__position_uncertainty = np.sqrt(np.abs(temp
                 - self.__average_position**2))

            # calculate the average momentum
            self.__average_momentum = np.dot(coefficient.conjugate(),
                np.dot(particle._pmat, coefficient)).real

            # calculate the momentum uncertainty
            temp = np.dot(coefficient.conjugate(), np.dot(particle._p2mat,
                    coefficient)).real
            self.__momentum_uncertainty = np.sqrt(temp
                - self.__average_momentum**2)

        # update properties time
        self.__properties_time += 1
        if self.__properties_time > self.__properties_duration:
            self.__properties_time = 0

        # print energy
        if energy is None:
            text = 'Energy = ???'
        else:
            text = 'Energy = {0:>8.1f}'.format(energy)
        text_surf = self.top_bar_font.render(text, True, (0,0,0))
        self.screen.blit(text_surf, (self.top_bar_x, self.top_bar_locations[0]))

        # print average energy
        text = 'Average energy = {0:>8.1f}'.format(average_energy)
        text_surf = self.top_bar_font.render(text, True, (0,0,0))
        self.screen.blit(text_surf, (self.top_bar_x, self.top_bar_locations[1]))

        # print average position
        text = 'Average position = {0:>5.3f}'.format(self.__average_position
            / particle.length)
        text_surf = self.top_bar_font.render(text, True, (0,0,0))
        self.screen.blit(text_surf, (self.top_bar_x, self.top_bar_locations[2]))

        # print position uncertainty
        text = 'Position uncertainty = +/- {0:>4.2f}'.format(self.__position_uncertainty
            / particle.length)
        text_surf = self.top_bar_font.render(text, True, (0,0,0))
        self.screen.blit(text_surf, (self.top_bar_x, self.top_bar_locations[3]))

        # print average momentum
        text = 'Average momentum = {0:>+5.0f}'.format(self.__average_momentum)
        text_surf = self.top_bar_font.render(text, True, (0,0,0))
        self.screen.blit(text_surf, (self.top_bar_x, self.top_bar_locations[4]))

        # print momentum uncertainty
        text = 'Momentum uncertainty = +/- {0:>2.0f}'.format(
            self.__momentum_uncertainty)
        text_surf = self.top_bar_font.render(text, True, (0,0,0))
        self.screen.blit(text_surf, (self.top_bar_x, self.top_bar_locations[5]))


    def collapse_animation(self, particle, C_old, C_new):
    
        # draw time steps between current wave function and new wave function
        self.eigenvectors_mode = False
        animating = True
        t = 0
        tmax = self._collapse_time

        C_old = np.copy(C_old)
        while animating:

            self.screen.fill((255,255,255))

            t += 1
            self.time += self.dt
            theta = t * np.pi / (2 * int(self.fps*tmax))

            # get a temporary coefficient
            C_temp = ( np.cos(theta) * C_old
                * np.exp(-1j * particle.energies * self.time)
                + np.sin(theta) * C_new )
            integral = (C_temp.conjugate() * C_temp).sum().real
            C_temp /= np.sqrt(integral)

            # generate an intermediate wave function to plot
            particle.Ct = C_temp
            psi_new = np.einsum('i,ij->j', C_temp, particle.wave_functions)

            # calculate a hybrid state energy
            average_energy = (( np.cos(theta)**2 * (C_old*C_old.conjugate()).real 
                              + np.sin(theta)**2 * (C_new*C_new.conjugate()).real
                              ) * particle.energies ).sum()
    
            surf = self.plot_wave_function(particle, psi_new,
                average_energy=average_energy)

            # listen to game events
            for event in pygame.event.get():

                # quit the game if requested
                if event.type == QUIT:
                    self.quit()

                # ignore the collapsing animation
                if event.type == KEYDOWN or event.type == MOUSEBUTTONUP:
                    animating = False

            # if some time has elapsed, kill animation
            if t >= self.fps * tmax: animating = False # animation takes tmax s

            # print "collapsing wave function..." text on the bottom
            collapsing_text = 'Collapsing wave function: {0:>3d}%'.format(
                int(t * 100 / (self.fps * tmax)))
            collapsing_text_surf = self.top_bar_font.render(collapsing_text,
                True, (0,0,0))
            text_w, text_h = collapsing_text_surf.get_size()
            self.screen.blit(collapsing_text_surf, (self.top_bar_x,
                self.height * 0.95 - text_h / 2))
 
            pygame.display.flip()
            self.clock.tick(self.fps)

        # get new particle average energy
        particle.average_energy = ((C_new*C_new.conjugate()).real
                                   * particle.energies).sum()

        # wait a second before continuing animation
        self.clock.tick(1)


    def resize(self, width, height):
        '''Function to resize the game window and plot window'''

        self.width = width
        self.height = height

        # reset plot size and location
        self.plot_width = self.width / self.dpi
        self.plot_height = self.height * 0.6 / self.dpi
        self.plot_origin = (0, self.height * 0.3)

        # top bar localtions
        self.top_bar_locations = (np.arange(6) + 0.5) * self.height * 0.3 / 7
        self.top_bar_x = self.width * 0.05

        # reset figure size and linewidth
        self.lw = min(self.plot_width, self.plot_height) * self._lw_ratio
        try:
            self.figure.set_size_inches(self.plot_width, self.plot_height)
        except AttributeError:
            pass

        # change font sizes
        self.menu_font_size = int(40 * min(self.width, self.height) / 600.)
        self.adventure_menu_font_size = int(26 * min(self.width, self.height) / 600.)
        self.text_font_size = int(40 * min(self.width, self.height) / 600.)
        self.top_bar_font_size = int(25 * self.height / 600.)

        self.menu_font = pygame.font.Font(self.resource_path('fonts/chintzy.ttf'),
                self.menu_font_size)
        self.adventure_menu_font = pygame.font.Font(
                self.resource_path('fonts/chintzy.ttf'), self.adventure_menu_font_size)
        self.text_font = pygame.font.Font(self.resource_path('fonts/ccr.ttf'),
                self.text_font_size)
        self.top_bar_font = pygame.font.Font(
                self.resource_path('fonts/instruction.ttf'), self.top_bar_font_size)

        # get button sizes
        size = int(min(self.height*0.09, self.width/12))
        self.button_spacing = (self.width - size*10) / 10

        # initialize the buttions

        button_images = {}
        keys = {'ESC':      "images/back.png",
                'ESC_S':    "images/back_s.png",
                'LEFT':     "images/rw.png",
                'LEFT_S':   "images/rw_s.png",
                'RIGHT':    "images/ff.png",
                'RIGHT_S':  "images/ff_s.png",
                'UP':       "images/up.png",
                'UP_S':     "images/up_s.png",
                'DOWN':     "images/down.png",
                'DOWN_S':   "images/down_s.png",
                'X':        "images/x.png",
                'X_S':      "images/x_s.png",
                'P':        "images/p.png",
                'P_S':      "images/p_s.png",
                'G':        "images/g.png",
                'G_S':      "images/g_s.png",
                'S':        "images/superposition.png",
                'S_S':      "images/superposition_s.png",
                'S_ON':     "images/superposition_on.png",
                'E':        "images/states.png",
                'E_S':      "images/states_s.png",
                'E_ON':     "images/states_on.png",}

        for key in keys:
            temp = pygame.image.load(self.resource_path(keys[key]))
            button_images[key] = pygame.transform.scale(temp, (size, size))
        self.button_images = button_images
        self.button_size = size


    def blit_texts(self, texts, color=(245,245,245)):
        '''
        Adds a list of texts to the screen.
        Text is adjustable based on window size. Each "texts" item starts a new
        paragraph.
        '''

        xstart = min(self.width * 0.08, self.height * 0.08)
        ystart = min(self.width * 0.08, self.height * 0.08)
        max_width = self.width - 2 * xstart
        max_height = self.height - 2 * ystart

        x, y = xstart, ystart

        for text in texts:

            # 2D array where each row is a list of words
            words = [word.split(' ') for word in text.splitlines()]
            space = self.text_font.size(' ')[0]  # The width of a space.
            for line in words:
                for word in line:
                    word_surface = self.text_font.render(word, True, color)
                    word_width, word_height = word_surface.get_size()
                    if x + word_width >= max_width:
                        x = xstart + 0  # Reset the x.
                        y += word_height  # Start on new row.
                    self.screen.blit(word_surface, (x, y)) 
                    x += word_width + space
                x = xstart + 0  # Reset the x.
                y += word_height  # Start on new row.
            y += word_height  # Start on new row.

    def draw_bottom_bar(self):

        # keys that can be shown
        keys = ["ESC", "LEFT", "RIGHT", "UP", "DOWN", "X", "P",
                "G", "S", "E"]
    
        # maximum height and width to use
        max_height = self.height * 0.08
        max_width = self.width * 0.1
    
        # figure out ideal font size
        size = 40
        keyfont = pygame.font.Font(self.resource_path('fonts/ccr.ttf'), size)
        word_surface = keyfont.render('[RIGHT]', True, (0,0,0))
        word_width, word_height = word_surface.get_size()
        size = int(min(max_width * 40 / word_width, max_height * 40 / word_height))
        keyfont = pygame.font.Font(self.resource_path('fonts/ccr.ttf'), size)

        # get starting y-position of the buttons   
        button_y = self.height * 0.95 - self.button_size / 2

        # get mouse position
        mouse = pygame.mouse.get_pos()
        self._button_selected = None
 
        for i in range(len(keys)):

            key = keys[i]

            if (self._level_options is not None and
                key not in self._level_options): continue

            # get button position
            button_x = (i + 0.5) * self.button_spacing + i * self.button_size

            # check if mouse is over button
            if ((button_x <= mouse[0] <= button_x+self.button_size) and
                (button_y <= mouse[1] <= button_y+self.button_size)):

                image = self.button_images[key+'_S']
                self._button_selected = key

            else:

                if key == 'S':
                    if self.superposition_mode:
                        image = self.button_images['S_ON']
                    elif key == 'S' and not self.superposition_mode:
                        image = self.button_images['S']

                elif key == 'E':
                    if self.eigenvectors_mode:
                        image = self.button_images['E_ON']
                    elif key == 'E' and not self.eigenvectors_mode:
                        image = self.button_images['E']

                else:
                        image = self.button_images[key]

            self.screen.blit(image, (button_x, button_y))


    def _level_reset(self):
        self._level_options = self._all_level_options
        self._button_selected = None
        self._goal = None
        self.dt = 1e-4
        self.time = 0
        self.superposition_mode = False
        self.eigenvectors_mode = False

    def quit(self, *args, **kwargs):
        pygame.display.quit()
        pygame.quit()
        sys.exit()

    # some common potentials used
    @property
    def harmonic_oscillator_potential(self):
        return ((np.linspace(0,1,500)-0.5))**2 * 40000.0

    @property
    def morse_potential(self, re=0.12, de=2000):
        x = np.linspace(0,1,500)
        return de * (1 - np.exp(-8 * (x - re)))**2

    @property
    def barrier_potential(self, x0=0.46, x1=0.56, de=4500):
        x = np.linspace(0,1,500)
        potential = np.zeros_like(x)
        potential[np.where((x>=x0)&(x<=x1))] = de
        return potential

    @property
    def coulombic_potential(self):
        potential = -1/np.abs(np.linspace(0,1,100)-0.5001)
        potential += 1000
        return potential

    @property
    def get_background_color(self):
        rgb = np.random.random((3))
        total = rgb.sum()
        rgb = rgb * 115 / total
        return np.array(rgb, dtype=int)
