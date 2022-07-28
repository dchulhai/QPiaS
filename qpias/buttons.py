import numpy as np
import pygame

class Buttons():
    """Store the information necessary to generate clickable menu buttons.

    :param game: A QPiaS Game object
    :type game: :class:`qpias.game.Game`

    """

    def __init__(self, game, texts, font=None,
            text_color=(255,255,255), highlight_color=(225,225,100),
            show=None, hidden_text_color=(100,100,100)):
        """Initialize the Buttons class."""

        self.game = game
        self.texts = texts
        self.ntexts = len(texts)
        self.text_color = text_color
        self.highlight_color = highlight_color
        self.hidden_text_color = hidden_text_color
        if font is None:
            self.font = game.menu_font
        else:
            self.font = font

        if show is None:
            self.show = [True] * self.ntexts
        else:
            self.show = show
        
        self.selected = 0

        # generate each text as a surface
        self.update()

    def update(self):
        # generate each text as a surface
        game = self.game
        self.text_surfs = []
        text_widths = []
        text_heights = []
        for i in range(self.ntexts):

            if self.show[i]:
                text_color = self.text_color
            else:
                text_color = self.hidden_text_color

            if i == self.selected: text_color = self.highlight_color
            surf = self.font.render(self.texts[i], True, text_color)
            self.text_surfs.append(surf)

            w = surf.get_width()
            h = surf.get_height()
            text_widths.append(w)
            text_heights.append(h)
        self.text_widths = np.array(text_widths)
        self.text_heights = np.array(text_heights)

        # get spacing between texts
        self.text_spacing = (game.height - self.text_heights.sum()) / (self.ntexts+1)

        
        # get origin position for each text
        text_origins = []
        for i in range(self.ntexts):
            origin_y = self.text_spacing * (i+0.5) + self.text_heights[:i+1].sum()
            origin_x = game.width / 2 - self.text_widths[i] / 2
            text_origins.append((origin_x, origin_y))
        self.text_origins = text_origins

        # check if mouse is over button
        mouse = pygame.mouse.get_pos() 
        for i in range(self.ntexts):
            if not self.show[i]: continue
            if ((self.text_origins[i][0] <= mouse[0] <= self.text_origins[i][0]
                + self.text_widths[i]) and
                (self.text_origins[i][1] <= mouse[1] <= self.text_origins[i][1]
                + self.text_heights[i])):
                self.selected = i

        self.draw()

    def draw(self):

        game = self.game

        for i in range(self.ntexts):
            game.screen.blit(self.text_surfs[i], self.text_origins[i])

    def select_next(self):
        looping = True
        while looping:
            self.selected += 1
            if self.selected == self.ntexts:
                self.selected = 0
            if self.show[self.selected]: looping = False

    def select_previous(self):
        looping = True
        while looping:
            self.selected -= 1
            if self.selected == -1:
                self.selected = self.ntexts - 1
            if self.show[self.selected]: looping = False

