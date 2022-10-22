from sys import argv

try:
    from models import Holder
    from models import *
    from board import *
    from colors import Color
except ImportError as err:
    print(err)
    exit(1)

try:
    TESTS = {
        'Q1': [get_board_item],
        'Q2': [set_board_item],
        'Q3': [valid_coordinate],
        'Board': [get_board_item, set_board_item, valid_coordinate], 
        'Q4': [rotate_block_90_cw],
        'Q5': [filter_blocks_pos],
        'Q6': [shift_down_fn],
        'Q7': [shift_left_fn],
        'Q8': [validated_apply_non_rot],
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
