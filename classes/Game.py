import sys
import pygame
import numpy as np
import random
import copy
import json
import os
from classes.Board import Board
from classes.AI import AI

from classes.constants import *

from classes.button import *


# initialise PYGAME in the model ==> SetUp

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Mopion IA ')
screen.fill(Bg_COLOR)

header_font = pygame.font.Font(None, 30)


class Game:

    # each time we create new object will be execute
    def __init__(self):
        self.board = Board()
        self.ai = AI()
        self.show_lines()
        self.gamemode = 'ai'  # pvp  or ai
        self.running = True  # game is not over
        self.player = 1  # 1-cross #2-circle

        self.reset_button = Button(RESET_X, RESET_Y, RESET_WIDTH, RESET_HEIGHT,
                                   RESET_TEXT, RESET_BACKGROUND_COLOR, RESET_TEXT_COLOR, self.reset)
        self.switch_mode_level = Button(MODE_X, MODE_Y, MODE_WIDTH, MODE_HEIGHT,
                                        MODE_TEXT, MODE_BACKGROUND_COLOR, MODE_TEXT_COLOR, self.change_gamemode)
        self.switch_turn_button = Button(TURN_X, TURN_Y, TURN_WIDTH, TURN_HEIGHT,
                                         TURN_TEXT, TURN_BACKGROUND_COLOR, TURN_TEXT_COLOR, self.switch_turn)
        self.save_game_button = Button(SAVE_X, SAVE_Y, SAVE_WIDTH, SAVE_HEIGHT,
                                       SAVE_TEXT, SAVE_BACKGROUND_COLOR, SAVE_TEXT_COLOR, self.save_game)
        self.load_game_button = Button(LOAD_X, LOAD_Y, LOAD_WIDTH, LOAD_HEIGHT,
                                       LOAD_TEXT, LOAD_BACKGROUND_COLOR, LOAD_TEXT_COLOR, self.load_game)

    def change_gamemode(self):
        print('change mode ')
        # self.gamemode = 'ai' if self.gamemode == 'pvp' else 'pvp'

        if self.gamemode == 'ai' and self.ai.level == 1:
            self.ai.level = 0
        elif self.gamemode == 'ai' and self.ai.level == 0:
            self.gamemode = 'pvp'
        elif self.gamemode == 'pvp':
            self.gamemode = 'ai'
            self.ai.level = 1
        else:
            print('error')

        self.updateScreen()

    def switch_turn(self):
        if self.board.marked_sqrs == 0:
            print('switch_turn')
        # self.ai.player = 1
        # self.player = 2
            self.next_turn()

    def save_game(self):
        if self.board.marked_sqrs != 0:
            # Define the game state
            game_state = {
                "board": self.board.squares.tolist(),
                "marked_squares": self.board.marked_sqrs,
                "game_mode": self.gamemode,
                "current_player": self.player,
                "ai_level": self.ai.level,
                "running": self.running
            }

            # Serialize and save to a file
            with open("game_save.json", "w") as file:
                json.dump(game_state, file)

            print("Game saved!")

    def load_game(self):

        if os.path.exists('game_save.json') and self.board.marked_sqrs == 0:
            try:
                with open("game_save.json", "r") as file:
                    game_state = json.load(file)

                    # Restore the game state
                    self.board.squares = np.array(game_state["board"])
                    self.board.marked_sqrs = game_state["marked_squares"]
                    self.gamemode = game_state["game_mode"]
                    self.player = game_state["current_player"]
                    self.ai.level = game_state["ai_level"]
                    self.running = game_state["running"]

                    # Draw the figures
                    for row in range(len(self.board.squares)):
                        # row 1
                        for col in range(len(self.board.squares[row])):
                            # If the square  is not empty
                            if self.board.squares[row][col] != 0:
                                # Temporarily set the current player to the value in the square
                                # so the correct figure gets drawn
                                self.player = self.board.squares[row][col]
                                self.draw_fig(row, col)

                    print("Game loaded!")
                    # Call updateScreen to refresh the display
                    self.updateScreen()

            except Exception as e:
                print(f"Error loading game: {e}")

    def show_lines(self):
        # pygame.draw.line(surface, color, start_pos, end_pos, width=1) ==> start_pos and  end_pos ( x , y ) ==> screen is like a matrix

        # Draw the header at the top

        # Vertical Lines

        for i in range(1, COLS):
            x = i * SQSIZE
            pygame.draw.line(screen, LINE_COLOR,
                             (x, HEADER_HEIGHT), (x, HEIGHT), LINE_WIDTH)

        # Horizontal Lines
        pygame.draw.line(screen, LINE_COLOR, (0, HEADER_HEIGHT),
                         (WIDTH, HEADER_HEIGHT), LINE_WIDTH)

        for i in range(1, ROWS):
            y = HEADER_HEIGHT + i * (GAME_HEIGHT // ROWS)
            pygame.draw.line(screen, LINE_COLOR, (0, y),
                             (WIDTH, y), LINE_WIDTH)

        pygame.draw.line(screen, LINE_COLOR, (0,  HEIGHT-5),
                         (WIDTH,  HEIGHT-5), LINE_WIDTH)

    def next_turn(self):
        self.player = self.player % 2 + 1  # ==>  1 or 2

    def isover(self):
        return self.board.final_state(show=True) != 0 or self.board.isfull()

    def make_move(self, row, col):
        self.board.mark_sqr(row, col, self.player)
        self.draw_fig(row, col)
        if not self.isover():
            self.next_turn()

    # ----- updateScreen fc
    def updateScreen(self):

        # Clear the area where the header is displayed
        pygame.draw.rect(screen, Bg_COLOR, (0, 0, WIDTH, HEADER_HEIGHT - 10))

        player = int(self.player)

        if self.gamemode == 'ai':
            if self.player == 1:
                text = "your Turn .. "
            else:
                text = "AI's Turn .. "
        else:
            text = f" player {player} Turn .."

        if self.isover():
            if self.gamemode == 'ai':
                if self.player == 1:
                    text = 'you win ! congratulations  '
                else:
                    text = 'you lose ! Artificial intelligence wins '
            else:
                text = f'player {player} wins ! congratulations'

        if self.board.final_state(show=True) == 0 and self.board.isfull():
            text = 'There is no winner !'
        # Blit the header text onto the screen
        header_text = header_font.render(text, True, TEXT_COLOR1)

        # mode text

        if self.gamemode == 'ai' and self.ai.level == 1:
            text_mode = 'IA VS person : HARD '
        elif self.gamemode == 'ai' and self.ai.level == 0:
            text_mode = 'IA VS person : EASY '
        elif self.gamemode == 'pvp':
            text_mode = ' person  VS  person'
        else:
            text_mode = 'text_mode'

        mode_text = header_font.render(text_mode, True, TEXT_COLOR2)
        screen.blit(header_text, (10, 10))

        screen.blit(mode_text, (200, 60))

        self.reset_button.draw(screen)
        if not self.isover():
            self.switch_mode_level.draw(screen)

        if self.board.marked_sqrs == 0:
            self.switch_turn_button.draw(screen)
        else:
            self.save_game_button.draw(screen)

        if os.path.exists('game_save.json') and self.board.marked_sqrs == 0:
            self.load_game_button.draw(screen)

        pygame.display.update()

    # ----- reset fc
    def reset(self):

        screen.fill(Bg_COLOR)  # Clear the screen to its background color
        self.__init__()
        print('reset')

        self.updateScreen()

    # ----- draw_fig fc
    def draw_fig(self, row, col):

        if self.player == 1:
            # draw croos
            # desc line
            start_desc = (col * SQSIZE + OFFSET,
                          (row * SQSIZE + OFFSET) + HEADER_HEIGHT)
            end_desc = (col * SQSIZE + SQSIZE - OFFSET,
                        (row * SQSIZE + SQSIZE - OFFSET) + HEADER_HEIGHT)
            pygame.draw.line(screen, CROSS_COLOR, start_desc,
                             end_desc, CROSS_WIDTH)

            # asc line
            start_asc = (col * SQSIZE + OFFSET,
                         (row * SQSIZE + SQSIZE - OFFSET) + HEADER_HEIGHT)
            end_asc = (col * SQSIZE + SQSIZE - OFFSET,
                       (row * SQSIZE + OFFSET) + HEADER_HEIGHT)
            pygame.draw.line(screen, CROSS_COLOR, start_asc,
                             end_asc, CROSS_WIDTH)

            pass
        elif self.player == 2:
            # draw circle
            center = (col * SQSIZE + SQSIZE // 2, (row *
                      SQSIZE + SQSIZE // 2) + HEADER_HEIGHT)  # center(x,y)
            pygame.draw.circle(screen, CIRC_COLOR, center, RADIUS, CIRC_WIDTH)


# -----------------------------------------------------------------------

#  main function
