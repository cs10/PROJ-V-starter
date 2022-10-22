from enum import Enum, auto, unique
import copy 


class Pytromino:
    """
    An object to represent a block of squares.
    """

    class Types(Enum):
        I = auto()
        O = auto()
        L = auto()
        S = auto()
        T = auto()
        J = auto()
        Z = auto()

    def __init__(self, block_rel_pos, color, pytromino_type, index=-1, center_rot=(0, 0)):
        """ 
        Create a new Pytromino instance. A pytromino consists of a list of
        coordinates for the center points of blocks. One of these blocks should
        have coordinate (0, 0), this is the reference block. All other blocks'
        coordinates are relatively the reference block's coordinate. Additionally,
        the center of rotation can be any point that's relative to center of reference;
        it does not have to be (0, 0).

        Parameters
        ----------
        block_rel_pos:
            type: list[tuple(int, int)]
            brief: a list of tuples (x, y) that represent a block's relative position to the center
        color:
            type: tuple(int, int, int)
            brief: RGB colors of this Pytromino
        pytromino_type: 
            type: Pytromino.Types
            brief: type of Pytromino
        center_rot: 
            type: tuple(int, int)
            brief: (optional) center of rotation coordinate relative to the (0, 0) reference block. 
                   Defaults to (0, 0).
        """
        assert isinstance(pytromino_type, Pytromino.Types)
        assert type(color) == tuple
        self.blocks_pos = block_rel_pos
        self.color = color
        self.type = pytromino_type
        self.center_rot = center_rot
        self.placed = False
        if index < 0:
            index = pytro_dict[pytromino_type]
        self.index = index

# ---------------------------------------------------------------------------- #
# --------------------------- Helpers: Not Required -------------------------- #
# ---------------------------------------------------------------------------- #
    def get_index(self):
        return self.index

    def get_unique_rows(self):
        """ 
        Returns a list of rows spanned by this pytromino
        """
        s = set()
        for pos in self.blocks_pos:
            s.add(pos[1])
        return list(s)

    def place_at(self, coordinate):
        """ 
        Place this Pytromino at coordinate, can only be called ONCE
        in an instance's lifetime
        """
        if not self.placed:
            validated_apply(self, lambda pos: add_pos(pos, coordinate), False)
            self.placed = True

    def is_placed(self):
        return self.placed

    def get_blocks_pos(self):
        """ 
        Returns a COPY of blocks_pos
        """
        return self.blocks_pos[:]

    def get_color(self):
        """ 
        Returns the color of the Pytromino
        """
        return self.color

    def get_type(self):
        return self.type

    def __repr__(self):
        return f"<Pytromino {self.blocks_pos}, {self.color}, {self.type}, {self.center_rot}>"

@unique
class Color(Enum):
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    CYAN = (43, 172, 226)
    YELLOW = (253, 225, 2)
    ORANGE = (247, 150, 34)
    GREEN = (77, 184, 72)
    PURPLE = (146, 44, 140)
    BLUE = (0, 90, 156)
    RED = (238, 40, 51)

pytro_dict = {
        Pytromino.Types.I: [[(0, 0), (-1, 0), (1, 0), (2, 0)], Color.CYAN.value, 1], 
        Pytromino.Types.O: [[(0, 0), (0, -1), (1, -1), (1, 0)], Color.YELLOW.value, 2], 
        Pytromino.Types.L: [[(0, 0), (-1, 0), (1, 0), (1, -1)], Color.ORANGE.value, 3], 
        Pytromino.Types.S: [[(0, 0), (-1, 0), (0, -1), (1, -1)], Color.GREEN.value, 4], 
        Pytromino.Types.T: [[(0, 0), (0, -1), (-1, 0), (1, 0)], Color.PURPLE.value, 5], 
        Pytromino.Types.J: [[(0, 0), (-1, -1), (-1, 0), (1, 0)], Color.BLUE.value, 6], 
        Pytromino.Types.Z: [[(0, 0), (0, -1), (-1, -1), (1, 0)], Color.RED.value, 7]
    }

def pytromino_factory(pytromino_type):
    arg_lst = pytro_dict.get(pytromino_type, None)
    if arg_lst:
        return Pytromino(arg_lst[0], arg_lst[1], pytromino_type, arg_lst[2])
    else:
        raise ValueError(f'Unknown block type: "{pytromino_type}"')


class Holder:
    """
    An object that can hold 1 item at a time, when closed, 
    the item can not be stored or replaced
    """

    def __init__(self):
        """
        Create an instance of Holder
        >>> holder = Holder()
        >>> holder.is_open()
        True
        >>> holder.store(1)
        >>> holder.get_item()
        1
        >>> holder.close()
        >>> holder.get_item()
        1
        >>> holder.is_open()
        False
        >>> holder.open()
        >>> holder.is_open()
        True
        """
        self._item = None
        self._can_store = True

    def store(self, item):
        """
        Hold an item, or replace sn existing item.

        Parameters
        ----------
        item:
            type: any
            brief: the item to hold
        """
        assert self._can_store, "holder is closed"
        self._item = item
        

    def open(self):
        """
        Open *this* holder to be able to store/replace item
        """
        self._can_store = True

    def close(self):
        """
        Close *this* holder so that no new item can be stored,
        or the existing item cannot be replaced.
        """
        self._can_store = False

    def get_item(self):
        """
        Get the item currently being held,
            regardless whether the holder is closed
        Returns
        -------
        any:
            the item currently being held
        """
        return self._item

    def is_open(self):
        """
        Check if *this* holder is currently open so that it can
        store item, or replace existing item.

        Returns
        -------
            type: bool
            brief: True if the holder can accept store/replace item, False otherwise
        """
        return self._can_store

def validated_apply(pytromino, fn, is_rotation=False, validator=lambda pos: True):
    """ 
    Apply fn on all block coordinates of the pytromino, and check the
    validity of each resulting coordinate using a validator function.
    A new pytromino is returned. If ALL resulting coordinates pass the 
    validator check, the returned pytromino will have its corresponding 
    coordinates updated. If is_rotation, self.center_rot of the returned
    pytromino is not changed. 

    Parameters
    ----------
    pytromino:
        type: Pytromino 
        brief: the Pytromino object in focus. 
    fn:
        type: Function, tuple(int, int) -> tuple(int, int)
        brief: a function that takes in a tuple of 2 int, then does some
        transformation, and return a new tuple of 2 int.
    is_rotation:
        type: bool
        brief: If fn is a rotational transfermation, self.center_rot will not
        be applied with fn
    validator:
        type: Function, tuple[int, int] -> bool:
        brief:  function that takes in the result of fn, a tuple of 2 int,
        does some check, then return a boolean of the result. By default,
        there is no meaningful check.
    Returns
    -------
        type: Pytromino object
        brief: the updated Pytromino object, or None if the validator is invalid 
    """
    if is_rotation:
        return validated_apply_rot(pytromino, fn, validator)
    else:
        return validated_apply_non_rot(pytromino, fn, validator)

def validated_apply_rot(pytromino, fn, validator):
    """ 
    Apply fn on all block coordinates of the pytromino, and check the
    validity of each resulting coordinate using a validator function.
    A new pytromino is returned. If ALL resulting coordinates pass the 
    validator check, the returned pytromino will have its corresponding 
    coordinates updated. This function is called when the operation is 
    not a rotation - self.center_rot of the returned pytromino is not changed. 

    Parameters
    ----------
    pytromino:
        type: Pytromino 
        brief: the Pytromino object in focus. 
    fn:
        type: Function, tuple(int, int) -> tuple(int, int)
        brief: a function that takes in a tuple of 2 int, then does some
        transformation, and return a new tuple of 2 int.
    is_rotation:
        type: bool
        brief: If fn is a rotational transfermation, self.center_rot will not
        be applied with fn
    validator:
        type: Function, tuple[int, int] -> bool:
        brief:  function that takes in the result of fn, a tuple of 2 int,
        does some check, then return a boolean of the result. By default,
        there is no meaningful check.
    Returns
    -------
        type: Pytromino object
        brief: the updated Pytromino object, or None if the validator is invalid 
    
    >>> S = Pytromino([(0, 0), (-1, 0), (0, -1), (1, -1)], Color.GREEN.value, Pytromino.Types.S, 2)
    >>> S 
    <Pytromino [(0, 0), (-1, 0), (0, -1), (1, -1)], (77, 184, 72), Types.S, (0, 0)>
    >>> rotator = lambda pos: rotate_block_90_cw(S, pos)
    >>> always_true = lambda pos: True 
    >>> S0 = validated_apply_rot(S, rotator, always_true)
    >>> S0
    <Pytromino [(0, 0), (0, -1), (1, 0), (1, 1)], (77, 184, 72), Types.S, (0, 0)>
    """
    new_pytro = copy.deepcopy(pytromino)
    validated = []
    for pos in pytromino.blocks_pos:
        if pos == pytromino.center_rot:
            validated.append(validator(pos))
        else:
            validated.append(validator(fn(pos)))
    if all(validated):
        new_pytro.blocks_pos = list(map(fn, pytromino.blocks_pos))
    return new_pytro

# ---------------------------------------------------------------------------- #
# ----------------------------- Required Methods ----------------------------- #
# ---------------------------------------------------------------------------- #

# Q4: rotate_block_90_cw
def rotate_block_90_cw(pytromino, pos):
    """
    Returns the position of the center of the Pytromino after rotating 90 degree clockwise.

    Parameters
    -------
    pytromino: 
        type: Pytromino object 
        brief: the pytromino to be rotated 
    pos: 
        type: tuple(int, int)
        brief: position of the center of rotation 
    Returns
    -------
        type: tuple(int, int)
        brief: the position of the center of the pytromino after rotation

    >>> rotate_block_90_cw(test_pytro_T, (-1, 0))
    (0, -1)
    >>> rotate_block_90_cw(test_pytro_T, (0, 1))
    (-1, 0)
    """
    # Hint:
        # The new x value is: center_rot.y - pos.y + center_rot.x
        # The new y value is: pos.x - center_rot.x + center_rot.y
        # You need to translate the above equations to code and
        # return the right solution.
    # BEGIN QUESTION 4
    """TODO: your solution here"""
    # END QUESTION 4

# To rotate the block counter-clockwise, we can simply rotate it clockwise 
# 90 degrees for 3 times!
def rotate_block_90_ccw(pytromino, pos):
    return rotate_block_90_cw(pytromino, rotate_block_90_cw(pytromino, rotate_block_90_cw(pytromino, pos)))

# Q5: filter_blocks_pos
def filter_blocks_pos(pytromino, fn):
    """
    Use a function to filter out blocks positions.

    Parameters
    ----------
    fn: 
        type: Function (tuple(int, int) -> bool)
        brief: a function that takes in a tuple coordinate and returns boolean
    Returns
    -------
        type: list[tuple(int, int)]
        brief: a list of tuple coordinates that satisfy fn

    >>> f = lambda pos: pos[0] == 0
    >>> g = lambda pos: pos[0] * pos[1] < 0
    >>> filter_blocks_pos(test_pytro_S, f)
    [(0, 0), (0, -1)]
    >>> filter_blocks_pos(test_pytro_S, g)
    [(1, -1)]
    """
    # BEGIN QUESTION 5
    """TODO: your solution here"""
    # END QUESTION 5

# Q6: shift_down_fn
def shift_down_fn(pos, steps):
    """
    Given a position as a tuple, return a new position that's shifted 
    down by steps. 

    Parameters
    ----------
    pos: 
        type: tuple(int, int)
        brief: the original location 
    steps:
        type: int 
        brief: number of steps to shift down
    Returns
    -------
        type: tuple(int, int)
        brief: A new location that's shifted down by steps

    >>> shift_down_fn((1, 3), 2)
    (1, 1)
    >>> shift_down_fn((6, 1), 3)
    (6, -2)
    >>> shift_down_fn((-1, 0), 1)
    (-1, -1)
    >>> shift_down_fn((3, 3), -5)
    (3, 8)
    """
    # BEGIN QUESTION 6
    """TODO: your solution here"""
    # END QUESTION 6

# Q7: shift_left_fn
def shift_left_fn(pos, steps):
    """
    Given a position as a tuple, return a new position that's shifted 
    left by steps. 

    Parameters
    ----------
    pos: 
        type: tuple(int, int)
        brief: the original location 
    steps:
        type: int 
        brief: number of steps to shift left 
    Returns
    -------
        type: tuple(int, int)
        brief: A new location that's shifted left by steps

    >>> shift_left_fn((1, 3), 2)
    (-1, 3)
    >>> shift_left_fn((6, 1), 3)
    (3, 1)
    >>> shift_left_fn((-1, 0), 1)
    (-2, 0)
    >>> shift_left_fn((3, 3), -5)
    (8, 3)
    """
    # BEGIN QUESTION 7
    """TODO: your solution here"""
    # END QUESTION 7
    
# Q8: validated_apply
def validated_apply_non_rot(pytromino, fn, validator):
    """ 
    Apply fn on all block coordinates of the pytromino, and check the
    validity of each resulting coordinate using a validator function.
    A new pytromino is returned. If ALL resulting coordinates pass the 
    validator check, the returned pytromino will have its corresponding 
    coordinates updated. Otherwise the returned pytromino has the same 
    coordinates as the original one. This function is called when the 
    operation is not a rotation.

    Parameters
    ----------
    pytromino:
        type: Pytromino 
        brief: the Pytromino object in focus. 
    fn:
        type: Function, tuple(int, int) -> tuple(int, int)
        brief: a function that takes in a tuple of 2 int, then does some
        transformation, and return a new tuple of 2 int.
    is_rotation:
        type: bool
        brief: If fn is a rotational transfermation, self.center_rot will not
        be applied with fn
    validator:
        type: Function, tuple[int, int] -> bool:
        brief:  function that takes in the result of fn, a tuple of 2 int,
        does some check, then return a boolean of the result. By default,
        there is no meaningful check.
    Returns
    -------
        type: Pytromino object
        brief: the updated Pytromino object, or None if the validator is invalid 

    >>> T = Pytromino([(0, 0), (0, -1), (-1, 0), (1, 0)], Color.PURPLE.value, Pytromino.Types.T, 1) 
    >>> T # Checkout the __repr__(self) below if you're curious
    <Pytromino [(0, 0), (0, -1), (-1, 0), (1, 0)], (146, 44, 140), Types.T, (0, 0)>
    >>> right_shift_1 = lambda pos: shift_left_fn(pos, -1)
    >>> positive_x = lambda pos: pos[0] > 0
    >>> T0 = validated_apply_non_rot(T, right_shift_1, positive_x)
    >>> T0 # No change!
    <Pytromino [(0, 0), (0, -1), (-1, 0), (1, 0)], (146, 44, 140), Types.T, (0, 0)>
    >>> always_true = lambda pos: True
    >>> T1 = validated_apply_non_rot(T, right_shift_1, always_true)
    >>> T1 # Notice the change in center_pos below
    <Pytromino [(1, 0), (1, -1), (0, 0), (2, 0)], (146, 44, 140), Types.T, (1, 0)>
    """
    new_pytro = copy.deepcopy(pytromino)
    # The line above creates a copy of the original pytromino object. 
    # Do any manipulation using new_pytro. DO NOT modify pytromino.
    # BEGIN QUESTION 8
    """TODO: your solution here"""
    # END QUESTION 8
    return new_pytro
    

# OBJECT FOR AUTOGRADER
# ------------- IMPORTANT: don't edit below this line! ---------------
test_pytro_T = Pytromino([(0, 0), (0, -1), (-1, 0), (1, 0)], Color.PURPLE.value, Pytromino.Types.T, 1) # type T
test_pytro_S = Pytromino([(0, 0), (-1, 0), (0, -1), (1, -1)], Color.GREEN.value, Pytromino.Types.S, 2) # type S