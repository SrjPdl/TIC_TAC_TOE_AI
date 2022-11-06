import os
import numpy as np
import time
from board import Board

class Game:
    '''Creates a game of tic-tac-toe using Board\\
    Attributes:
        board: The board of the game
        player: The value representing the human player.
        opponent: The value representing the AI player.
        current_player: The value representing the current player.
    Methods:
        main_loop: The main loop of the game.
        is_game_over: Checks if the game is over.
        player_move: Gets the move of the human player.
        evaluation: Evaluates the terminal state of board.
        is_draw: Checks if the game is a draw.
        is_winner: Checks if a player has won the game.
        minimax: The minimax algorithm.
        minimax_alpha_beta: The minimax algorithm with alpha-beta pruning.
    '''
    def __init__(self) -> None:
        '''Initializes the game.\\
        Args:
            None
        Returns:
            None
        '''
        self.board = Board(3,3,'X','O')
        self.player = -1
        self.opponent = 1
        self.current_player = self.opponent

    def main_loop(self):
        '''The main loop of the game.\\
        Args:
            None
        Returns:
            None
        '''
        os.system("clear")
        print("""\n\
            ████████╗██╗░█████╗░░░░░░░████████╗░█████╗░░█████╗░░░░░░░████████╗░█████╗░███████╗
            ╚══██╔══╝██║██╔══██╗░░░░░░╚══██╔══╝██╔══██╗██╔══██╗░░░░░░╚══██╔══╝██╔══██╗██╔════╝
            ░░░██║░░░██║██║░░╚═╝█████╗░░░██║░░░███████║██║░░╚═╝█████╗░░░██║░░░██║░░██║█████╗░░
            ░░░██║░░░██║██║░░██╗╚════╝░░░██║░░░██╔══██║██║░░██╗╚════╝░░░██║░░░██║░░██║██╔══╝░░
            ░░░██║░░░██║╚█████╔╝░░░░░░░░░██║░░░██║░░██║╚█████╔╝░░░░░░░░░██║░░░╚█████╔╝███████╗
            ░░░╚═╝░░░╚═╝░╚════╝░░░░░░░░░░╚═╝░░░╚═╝░░╚═╝░╚════╝░░░░░░░░░░╚═╝░░░░╚════╝░╚══════╝""")
        first_turn = input("Do you want to play first? (y/n): ")
        if first_turn == "y":
            self.current_player = self.player
        else:
            self.current_player = self.opponent
        while True:
            os.system("clear")
            self.board.draw_board()
            if self.current_player == self.player:
                start_time = time.time()
                _, move_x, move_y = self.minimax_alpha_beta(self.board, 9, False, -np.inf, np.inf)
                print("Time taken for evaluation: " + str(time.time()-start_time) +" seconds.")
                print("Best move: {}, {}".format(move_x, move_y))
                # pos = self.player_move()
                pos = (move_x, move_y)
                self.board.update_board(pos, self.player)
                self.current_player = self.opponent
            else:
                start_time = time.time()
                value,move_x,move_y = self.minimax_alpha_beta(self.board, 9, True, -np.inf, np.inf)
                print("Time taken for evaluation: " + str(time.time()-start_time) +" seconds.")
                print("Best move: {},{} with value: {}".format(move_x,move_y,value))
                self.board.update_board((move_x,move_y), self.opponent)
                self.current_player = self.player
            
            if self.is_winner(self.opponent, self.board):
                os.system("clear")
                self.board.draw_board()
                print("AI won")
                break
            if self.is_draw(self.board):
                os.system("clear")
                self.board.draw_board()
                print("Draw!! Game Over")
                break
            if self.is_winner(self.player, self.board):
                os.system("clear")
                self.board.draw_board()
                print("Human won")
                break
            
    def is_game_over(self, board:Board) -> bool:
        '''Checks if the game is over using current board state.\\
            Args:
                board: The board state of the game.
                Returns:
                    True if the game is over, False otherwise.
        '''
        return self.is_winner(self.player, board) or self.is_winner(self.opponent, board) or self.is_draw(board)

    def player_move(self) -> tuple:
        '''Gets the move of the human player.\\
        Args:
            None
        Returns:
            The position of the move.
        '''
        pos = tuple(map(int, input("Enter the position you want to play: ").replace(" ","")))
        if pos[0]>2 or pos[1]>2:
            print("Invalid position")
            return self.player_move()
        if self.board.is_space_empty(pos):
            return pos
        else:
            print("Position is not empty")
            return self.player_move()
    

    def evaluation(self,board:Board) -> int:
        '''Evaluates the terminal state of board.\\
        Args:
            board: The board state of the game.
        Returns:
            The static evaluation of the board state.
        '''
        if self.is_winner(self.opponent, board):
            return 1
        elif self.is_winner(self.player, board):
            return -1
        else:
            return 0


    def minimax(self, board:Board, depth:int, is_maximizing:bool) -> tuple:
        '''The minimax algorithm.\\
        Args:
            board: The board state of the game.
            depth: The depth of the search tree.
            is_maximizing: True if the current player is maximizing, False otherwise.
        Returns:
            The best move and the value of the best move.
        '''

        if depth==0 or self.is_game_over(board):
            return self.evaluation(board), 0, 0
        if is_maximizing:
            max_eval = -np.inf
            for i in range(3):
                for j in range(3):
                    if board.is_space_empty((i,j)):
                        board.update_board((i,j),self.opponent)
                        evaluation,_,_ = self.minimax(board, depth-1, False)
                        board.update_board((i,j),0)
                        if evaluation > max_eval:
                            max_eval = evaluation
                            best_move = (i,j)
            return max_eval, best_move[0], best_move[1]
        else:
            min_eval = +np.inf
            for i in range(3):
                for j in range(3):
                    if board.is_space_empty((i,j)):
                        board.update_board((i,j),self.player)
                        evaluation,_,_ = self.minimax(board, depth-1, True)
                        board.update_board((i,j),0)
                        if evaluation < min_eval:
                            min_eval = evaluation
                            best_move = (i,j) 
            return min_eval, best_move[0], best_move[1]

    def minimax_alpha_beta(self, board:Board, depth:int, is_maximizing:bool, alpha:int, beta:int) -> tuple:
        '''The minimax algorithm with alpha-beta pruning.\\
        Args:
            board: The board state of the game.
            depth: The depth of the search tree.
            is_maximizing: True if the current player is maximizing, False otherwise.
            alpha: The alpha value for alpha-beta prunning.
            beta: The beta value for alpha-beta prunning.
        Returns:
            The best move and the value of the best move.

        '''
        if depth==0 or self.is_game_over(board):
            return self.evaluation(board), 0, 0
        if is_maximizing:
            max_eval = -np.inf
            for i in range(3):
                for j in range(3):
                    if board.is_space_empty((i,j)):
                        board.update_board((i,j),self.opponent)
                        evaluation,_,_ = self.minimax_alpha_beta(board, depth-1, False, alpha, beta)
                        board.update_board((i,j),0)
                        if evaluation > max_eval:
                            max_eval = evaluation
                            best_move = (i,j)
                        if max_eval > alpha:
                            alpha = max_eval

                        if alpha >= beta:
                            return max_eval, best_move[0], best_move[1]

                                   
            return max_eval, best_move[0], best_move[1]
        else:
            min_eval = +np.inf
            for i in range(3):
                for j in range(3):
                    if board.is_space_empty((i,j)):
                        board.update_board((i,j),self.player)
                        evaluation,_,_ = self.minimax_alpha_beta(board, depth-1, True, alpha, beta)
                        board.update_board((i,j),0)
                        if evaluation < min_eval:
                            min_eval = evaluation
                            best_move = (i,j)
                        if min_eval < beta:
                            beta = min_eval 
                        if alpha >= beta:
                            return min_eval, best_move[0], best_move[1]
                        
            return min_eval, best_move[0], best_move[1]


    def is_draw(self, board:Board) -> bool:
        '''Checks if the game is a draw.\\
        Args:
            board: The board state of the game.
        Returns:
            True if the game is a draw, False otherwise.
        '''
        for i in range(3):
            for j in range(3):
                if board.board[i][j] == 0:
                    return False
        return True

        
    def is_winner(self, value:int, board:Board) -> bool:
        '''Checks if the player with value has won.\\
        Args:
            value: The value representing the player to test if it has won.
            board: The board state of the game.
        Returns:
            True if the player has won, False otherwise.
        '''
        return board.board[0][0] == board.board[0][1] == board.board[0][2] == value or \
            board.board[1][0] == board.board[1][1] == board.board[1][2] == value or \
            board.board[2][0] == board.board[2][1] == board.board[2][2] == value or \
            board.board[0][0] == board.board[1][0] == board.board[2][0] == value or \
            board.board[0][1] == board.board[1][1] == board.board[2][1] == value or \
            board.board[0][2] == board.board[1][2] == board.board[2][2] == value or \
            board.board[0][0] == board.board[1][1] == board.board[2][2] == value or \
            board.board[0][2] == board.board[1][1] == board.board[2][0] == value
           

def main():
    '''The main function of the program.
    '''
    game = Game()
    game.main_loop()

if __name__ == "__main__":
    main()