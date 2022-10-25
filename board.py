import random
import copy 
from models import *

class Board:
    """ 
    An object to represent a 2-Dimensional rectangular board
    """

    def __init__(self, num_cols=10, num_rows=22, cell_item=None, grid=None):
        """ 
        Create a Board instance that has num cols and num rows.
        The 2D board is represented with a single list, if the board looks like:
        col  col  col
         0    1    2
        -------------
        | 0 | 1 | 2 |  row 0
        ----+---+----
        | 3 | 4 | 5 |  row 1
        -------------
        Where num cols = 3, num rows = 2
        Then the underlying representation looks like:
        [0, 1, 2, 3, 4, 5]

        Parameters
        ----------
        num_cols (int, required):
            number of columns. Defaults to 10.
        num_rows (int, required):
            number of rows. Defaults to 22 (only the bottom 20 rows will be displayed).
        cell_item (any, optional):
            create default items. Defaults to None.
        grid (list[any], optional): a list to create the underlying board representation.
                However len(grid) = num_cols * num_rows. Defaults to None.
        Returns
        -------
            type: Board object
            brief: the Board object created with the parameters
        """
        assert num_cols is not None and num_rows is not None
        assert type(num_cols) == int and type(num_rows) == int
        assert num_cols >= 0 and num_rows >= 0
        self.num_rows = num_rows
        self.num_cols = num_cols
        if grid:
            assert num_cols * num_rows == len(grid)
            self.grid = grid[:]
        else:
            self.grid = [cell_item for _ in range(num_cols * num_rows)]

# ---------------------------------------------------------------------------- #
# --------------------------- Helpers: Not Required -------------------------- #
# ---------------------------------------------------------------------------- #

    def get_num_rows(self):
        return self.num_rows

    def get_num_cols(self):
        return self.num_cols
    
    def update_grid(self, new_grid):
        """ 
        Overwrite existing underlying board with a new board
        """
        assert len(new_grid) == len(self.grid), 'unequal grid lengths'
        self.grid = new_grid
    
    def __eq__(self, other):
        """
        Checks whether or not two boards are equal. 
        >>> board_1 = Board(2, 3, grid=list(range(6)))
        >>> board_2 = Board(2, 3, grid=list(range(6)))
        >>> board_1 == board_2
        True
        """
        assert type(self) == type(other), 'Must compare two Board objects'
        return self.num_cols == other.num_cols and self.num_rows == other.num_rows and self.grid == other.grid

    def __repr__(self):
        return f'<Board num_cols: {self.num_cols} num_rows: {self.num_rows}>'

    def __str__(self):
        """ 
        Print out the board items in a grid
        >>> board = Board(2, 3, grid=list(range(6)))
        >>> print(board)
        ===
        0 1
        2 3
        4 5
        ===
        """
        s = '=' * (self.num_cols * 2 - 1) + '\n'
        for i, val in enumerate(self.grid):
            s += str(val)
            if (i + 1) % self.num_cols != 0:
                s += ' '
            if (i + 1) % self.num_cols == 0:
                s += '\n'
        s += '=' * (self.num_cols * 2 - 1)
        return s


def pop_row(board,y):
    start_index = y * board.num_cols
    before = board.grid[0:start_index]
    after = board.grid[start_index + board.num_cols:]
    new_zero = [0 for _ in range(board.num_cols)]
    new_grid = before + after + new_zero
    board.update_grid(new_grid)

# ---------------------------------------------------------------------------- #
# --------------------------------- Required --------------------------------- #
# ---------------------------------------------------------------------------- #

# Q1: get_board_item
def get_board_item(board, x, y):
    """
    Get the item at coordinate (x, y).

    Parameters
    ----------
    board:
        type: Board object
        brief: the target board to get item from
    x:
        type: int
        brief: column number
    y:
        type: int
        brief: row number
    Returns
    -------
        type: any
        brief: the item stored at the board's (x,y) coordinate
    
    >>> board = Board(2, 2, grid=[1, 0, 2, 4])
    >>> get_board_item(board, 0, 1)
    2
    >>> get_board_item(board, 1, 0)
    0
    >>> get_board_item(test_board_1, 0, 0)
    5
    >>> get_board_item(test_board_2, 1, 0)
    2
    """
    # BEGIN QUESTION 1
    """TODO: your solution here"""
    # END QUESTION 1

# Q2: set_board_item
def set_board_item(board, x, y, item):
    """
    Set the item at coordinate (x, y) and return a new Board object.

    Parameters
    ----------
    board:
        type: Board object
        brief: the target board to get item from
    x:
        type: int
        brief: column number
    y:
        type: int
        brief: row number
    item:
        type: any
        brief: the item to replace
    Returns
    -------
        type: Board object
        brief: A new Board object with the item at (x, y) set to the passed in item.
    
    >>> board = Board(2, 2, grid=[1, 0, 2, 4])
    >>> new_board = set_board_item(board, 0, 1, 3)
    >>> get_board_item(new_board, 0, 1)
    3
    >>> set_board_item(test_board_1, 0, 0, 1) == Board(3, 2, grid=[1, 4, 1, 3, 0, 6])
    True
    >>> set_board_item(test_board_2, 3, 0, 1000) == Board(4, 1, grid=[9, 2, 4, 1000])
    True
    """
    new_board = copy.deepcopy(board) 
    # The line above creates a copy of the original Board object. 
    # Do any manipulation using new_board. DO NOT modify board. 
    # BEGIN QUESTION 2
    """TODO: your solution here"""
    # END QUESTION 2
    return new_board

# Q3: valid_coordinate
def valid_coordinate(board, coordinate):
    """
    Check whether coordinate (x, y) is on the board.

    Parameters
    ----------
    board:
        type: Board object
        brief: the target board to get item from
    coordinate:
        type: tuple(x, y)
        brief: an (x: int, y: int) coordinat
    Returns
    -------
        type: boolean
        brief: whether the coordinate is valid within this board
    
    >>> board = Board(2, 2, grid=[1, 0, 2, 4])
    >>> valid_coordinate(board, (1, 0))
    True
    >>> valid_coordinate(board, (1, 2))
    False
    >>> valid_coordinate(test_board_1, (0, 0))
    True
    >>> valid_coordinate(test_board_2, (-1, 0))
    False
    """
    # BEGIN QUESTION 3
    """TODO: your solution here"""
    # END QUESTION 3

# Q4: get_row
def get_row(board, y):
    """
    Get a row of items at row y.

    Parameters
    ----------
    board:
        type: Board object
        brief: the target board to get column from
    y:
        type: int
        brief: row number
    Returns
    -------
        type: list of any
        brief: a list of the items stored at the board's y row
    
    >>> board = Board(2, 2, grid=[1, 0, 2, 4])
    >>> get_row(board, 0)
    [1, 0]
    >>> get_row(board, 1)
    [2, 4]
    >>> get_row(test_board_1, 1)
    [3, 0, 6]
    >>> get_row(test_board_2, 0)
    [9, 2, 4, 1]
    """
    assert 0 <= y < board.num_rows, f'Invalid y: {y}' # validating the row number
    # BEGIN QUESTION 4
    """TODO: your solution here"""
    # END QUESTION 4

# Q5: check_row_full
def check_row_full(board, y):
    """
    Check if a row is full, such that it all of its grids contain a non-zero value.

    Parameters
    ----------
    board:
        type: Board object
        brief: the target board to get column from
    y:
        type: int
        brief: row number
    Returns
    -------
        type: boolean
        brief: True if the row at index y is full, False otherwise. 
        
    >>> board = Board(2, 2, grid=[1, 0, 2, 4])
    >>> check_row_full(board, 0)
    False
    >>> check_row_full(board, 1)
    True
    >>> check_row_full(test_board_2, 0)
    True
    >>> check_row_full(test_board_1, 1)
    False
    """
    # BEGIN QUESTION 5
    """TODO: your solution here"""
    # END QUESTION 5
    
# OBJECT FOR AUTOGRADER
# ------------- IMPORTANT: don't edit below this line! ---------------
test_board_1 = Board(3, 2, grid=[5, 4, 1, 3, 0, 6])
test_board_2 = Board(4, 1, grid=[9, 2, 4, 1])
test_board_r = [Board(6, 6, grid=[random.randint(0,9) for _ in range(36)]) for _ in range(18)]
test_pytro_T = Pytromino([(0, 0), (0, -1), (-1, 0), (1, 0)], Color.PURPLE.value, Pytromino.Types.T, 1) # type T
test_pytro_S = Pytromino([(0, 0), (-1, 0), (0, -1), (1, -1)], Color.GREEN.value, Pytromino.Types.S, 2) # type S