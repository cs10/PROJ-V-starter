from sys import argv

try:
    from models import Holder
    from models import *
    from board import *

except ImportError as err:
    print(err)
    exit(1)

try:
    TESTS = {
        'Q1': [get_board_item],
        'Q2': [set_board_item],
        'Q3': [valid_coordinate],
        'Q4': [get_row],
        'Q5': [check_row_full],
        'Board': [get_board_item, set_board_item, valid_coordinate, get_row, check_row_full], 
        'Q6': [rotate_block_90_cw],
        'Q7': [filter_blocks_pos],
        'Q8': [shift_down_fn],
        'Q9': [shift_left_fn],
        'Q10': [validated_apply_non_rot],
        'Pytromino': [rotate_block_90_cw, filter_blocks_pos, shift_down_fn, shift_left_fn, validated_apply_non_rot]
    }
    from doctest import run_docstring_examples
    
    if len(argv) < 2:
        for obj in TESTS.values():
            run_docstring_examples(obj, globals())
        exit(0)

    t = argv[1]
    if t in TESTS:
        objs = TESTS[t]
        for obj in objs:
            run_docstring_examples(obj, globals())
    else:
        print(f'Unrecognized Question: {t}')
        exit(1)
except IndexError as err:
    print(err)
    exit(1)
