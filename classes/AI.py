import numpy as np
import random
import copy


# -----------------------------------------------------------------------
# class AI

# level : 0 ==> random IA ,
# level : 1 ==> max min  IA ,

# player 2 ==> default IA

class AI:
    def __init__(self, level=1, player=2):
        self.level = level
        self.player = player

    # Random IA fc
    def rnd(self, board):
        empty_sqrs = board.get_empty_sqrs()  # return an array
        idx = random.randrange(0, len(empty_sqrs))

        return empty_sqrs[idx]  # return 1 sqr( row , col ) with rand  index

    def minimax(self, board, maximizing):
        # terminal case
        case = board.final_state()

        # player 1 wins
        if case == 1:
            return 1, None  # eval , move

        # player 2 wins ==> we are the IA
        if case == 2:
            return -1, None  # Ia is the minimizing

        elif board.isfull():
            return 0, None

        # we are here ==> we dont have a winner yet

        if maximizing:
            max_eval = -100  # any nb greater than 1 , 0  , -1
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, 1)
                # eval ==> evaluation
                eval = self.minimax(temp_board, False)[0]

                if eval > max_eval:
                    max_eval = eval
                    best_move = (row, col)

            return max_eval, best_move

        elif not maximizing:
            min_eval = 100  # any nb greater than 1 , 0  , -1
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, self.player)
                # eval ==> evaluation
                eval = self.minimax(temp_board, True)[0]
                # [0] is the min_eval  =>  minimax return min_eval, best_move

                if eval < min_eval:
                    min_eval = eval
                    best_move = (row, col)

            return min_eval, best_move

    # main function IA

    def eval(self, main_board):
        if self.level == 0:
            # Random choice
            eval = 'random'  # nothing ==> not important
            move = self.rnd(main_board)

        else:
            # MinMax  choice
            # in this game the IA is the minimizing
            eval, move = self.minimax(main_board, False)

        if move is not None:
            print(
                f'AI has chosen to mark the square in pos {move} with an eval of: {eval}')
        else:
            print('AI cannot find a valid move.')

        return move  # row , col


# -----------------------------------------------------------------------
# class GAME
