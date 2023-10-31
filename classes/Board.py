import sys
import pygame
import numpy as np
import random
import copy
import json
import os

from classes.constants import *

#from button import *
#from AI import *

from classes.Game import *


# initialise PYGAME in the model ==> SetUp

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Mopion IA ')
screen.fill(Bg_COLOR)

header_font = pygame.font.Font(None, 30)


# -----------------------------------------------------------------------
# class Board


class Board:

    def __init__(self):
        self.squares = np.zeros((ROWS, COLS))  # ==> matrix of 0
        self.empty_sqrs = self.squares  # ==> list of squares
        self.marked_sqrs = 0

    # check if we have a winner
    def final_state(self, show=False):
        '''
        @return 0 if there is no win yet 
        @return 1 if player 1  win  
        @return 2 if player 2  win 
        '''

        # vertical wins
        for col in range(COLS):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0:

                if show:
                    color = CIRC_COLOR if self.squares[0][col] == 2 else CROSS_COLOR
                    iPos = (col * SQSIZE + SQSIZE // 2, 20 + HEADER_HEIGHT)
                    fPos = (col * SQSIZE + SQSIZE // 2,
                            HEIGHT - 20)
                    pygame.draw.line(screen, color, iPos, fPos, LINE_WIDTH)
                # ==> we have a winner , can be 1 or 2
                return self.squares[0][col]

        # horizontal wins
        for row in range(ROWS):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:
                if show:
                    color = CIRC_COLOR if self.squares[row][0] == 2 else CROSS_COLOR
                    iPos = (20, (row * SQSIZE + SQSIZE // 2)+HEADER_HEIGHT)
                    fPos = (WIDTH - 20, (row * SQSIZE +
                            SQSIZE // 2) + HEADER_HEIGHT)
                    pygame.draw.line(screen, color, iPos, fPos, LINE_WIDTH)
                # ==> we have a winner , can be 1 or 2
                return self.squares[row][0]

        # desc  diagonal
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
            if show:
                color = CIRC_COLOR if self.squares[1][1] == 2 else CROSS_COLOR
                iPos = (20, 20 + HEADER_HEIGHT)
                fPos = (WIDTH - 20, (HEIGHT - 20))
                pygame.draw.line(screen, color, iPos, fPos, CROSS_WIDTH)
            return self.squares[0][0]

        # asc  diagonal
        if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] != 0:
            if show:
                color = CIRC_COLOR if self.squares[1][1] == 2 else CROSS_COLOR
                iPos = (20,   HEIGHT - 20)
                fPos = (WIDTH - 20, 20 + HEADER_HEIGHT)
                pygame.draw.line(screen, color, iPos, fPos, CROSS_WIDTH)
            return self.squares[2][0]

        # ==> we dont have a winner
        return 0

    #  mrk sqrs with the player id

    def mark_sqr(self, row, col, player):
        self.squares[row][col] = player  # ==> squares is an matrix !!
        self.marked_sqrs += 1

    # is empty ?
    def empty_sqr(self, row, col):
        return self.squares[row][col] == 0

    # get all the empty sqrs
    def get_empty_sqrs(self):
        empty_sqrs = []

        for row in range(ROWS):
            for col in range(COLS):
                if self.empty_sqr(row, col):
                    empty_sqrs.append((row, col))

        return empty_sqrs

    # is isfull  ?
    def isfull(self):
        return self.marked_sqrs == 9

    # is isempty  ?
    def isempty(self):
        return self.marked_sqrs == 0
