import sys
import pygame
import numpy as np
import player_name

from classes.Game import *

from player_name import GameSetupUI


# -----------------------------------------------------------------------

#  main function


def main():

    # create Game Object ==> start the game
    game = Game()

    ai = game.ai
    # header_text = header_font.render(
    #     "Player " + str(game.player), True, LINE_COLOR)  # Initial header text

    board = game.board

    # main loop
    while True:
        game.updateScreen()
        #  All the Events is here : ex any click is an event
        for event in pygame.event.get():
            # event Quit
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit

            if event.type == pygame.MOUSEBUTTONDOWN:

                # reset btn
                if game.reset_button.rect.collidepoint(event.pos):
                    game.reset()
                    board = game.board
                    ai = game.ai
                # switch_mode_level btn
                if game.switch_mode_level.rect.collidepoint(event.pos):
                    game.change_gamemode()
                # switch_turn_button btn
                if game.switch_turn_button.rect.collidepoint(event.pos):
                    game.switch_turn()
                # save btn
                if game.save_game_button.rect.collidepoint(event.pos):
                    game.save_game()
                # load_game btn
                if game.load_game_button.rect.collidepoint(event.pos):
                    game.load_game()

                pos = event.pos
                # ==> in this way we have the x , y  : 112 / 233 = 0 ==>  x=0

                # if human
                if HEADER_HEIGHT <= pos[1] <= HEIGHT:
                    row = (pos[1] - HEADER_HEIGHT) // SQSIZE
                    col = pos[0] // SQSIZE
                    if (board.empty_sqr(row, col)) and game.running:

                        if game.gamemode == 'ai' and game.player != ai.player:
                            game.make_move(row, col)
                        else:
                            print('you cant ')

                        # if person vs person
                        if game.gamemode != 'ai':
                            game.make_move(row, col)

                        # check if  game over
                        if game.isover():
                            game.running = False

                        # print(board.squares)
        # if AI
        if game.gamemode == 'ai' and game.player == ai.player and game.running:

            # update the screen

            game.updateScreen()

            row, col = ai.eval(board)
            game.make_move(row, col)
            # print(board.squares)
            if game.isover():
                game.running = False

        game.updateScreen()


if __name__ == "__main__":
    game_setup_ui = GameSetupUI(main)
    game_setup_ui.run()
