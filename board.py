import numpy as np
class Board:
    '''Creates a 2D board for 2 player games with the given width and height in the console and fills it with zeros.\\
    Attributes:
        board: A 2D array of zeros with the given width and height.
        player1_symbol: The symbol of player 1
        player2_symbol: The symbol of player 2
    Methods:
        draw_board: Draws the board in the console with the given symbols.
        is_space_empty: Checks if the given position is empty
        update_board: Updates the board with the given position and value
    '''
    def __init__(self, width:int, height:int, player1_symbol:str, player2_symbol:str) -> None:
        '''Initializes the board with the given symbols for players, width and height and fills it with zeros.\\
        Args:
            width: The width of the board
            height: The height of the board
            player1_symbol: The symbol of player 1
            player2_symbol: The symbol of player 2
        Returns:
            None
        '''
        self.board = np.zeros((height, width), dtype=int)
        self.player1_symbol = player1_symbol
        self.player2_symbol = player2_symbol

    def draw_board(self) -> None:
        '''Draws the board in the console. 0 represents empty space, 1 represents player1 and -1 represents player2. Use update_board() for updating the board with desired values.\\
        Args:
            None
        Returns:
            None
        '''
        for i in range(self.board.shape[1] + 1):
                print("+", end="")
                if i!= self.board.shape[1]:
                    print("-"*3, end="")
        print()
        for i in range(self.board.shape[0]):
            for j in range(self.board.shape[1]):
                print("|", end="")
                if self.board[i][j] == 0:
                    print("   ", end= "")
                if self.board[i][j] == 1:
                    print(" {} ".format(self.player1_symbol), end = "")
                if self.board[i][j] == -1:
                    print(" {} ".format(self.player2_symbol), end = "")
            print("|", end = "")
            print()
            for i in range(self.board.shape[1] + 1):
                print("+", end="")
                if i!= self.board.shape[1]:
                    print("-"*(3), end="")
            print()
    
    def is_space_empty(self, position:tuple) -> bool:
        '''Checks if the given position is empty.\\
        Args:
            position: The position to check
        Returns:
            True if the position is empty, False otherwise
        '''
        if self.board[position[0],position[1]] == 0:
            return True
        else:
            return False
    
    def update_board(self, position:tuple, value:int) -> None:
        '''Updates the board with the given position and value.\\
        Args:
            position: The position to update
            value: The value to update the position with
        Returns:
            None
        '''
        self.board[position[0],position[1]] = value