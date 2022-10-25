from multiprocessing import parent_process
import turtle
import time
import random
from models import *
from board import *

color_scheme = [
    # order = board, background, 7tiles, screen background, text color

    # the classic board, just the way everybody loves the blocks to be like
    ['black','lightblue', 'yellow', 'orange', 'green', 'purple', 'blue', 'red', 'wheat', 'black'],
    # a glacial color designed to hurt your eyes
    ['snow', 'cornflower blue', 'royal blue', 'powder blue', 'sky blue', 'steel blue', 'light blue', 'deep sky blue', 'alice blue', 'navy'],
    # the peacock color design, blue green, and a tiny bit of light orange
    ['azure', 'light sea green', 'cadet blue', 'coral','gold','medium aquamarine','cornflower blue', 'turquoise','light slate gray', 'aquamarine'],
    # some of our favorite food, now in turtle colors
    ['antique white', 'salmon', 'light salmon', 'dark salmon', 'tomato', 'coral', 'orange red', 'chocolate', 'cornsilk', 'maroon']]

# each time a new window opens, select a random set of presets colors from color scheme 
seed = random.randint(0, len(color_scheme) - 1)
colors = color_scheme[seed]

# render the GUI window
ws = turtle.Screen()
ws.title("CS10 PROJ-V Pyturis")
bgcolor = colors[8]
ws.bgcolor(bgcolor)
ws.setup(width=450, height=700)
ws.tracer(0)

# single source of truth: delay, colors (list), init_x, init_y as positions
delay = 0.3 # defaulted to medium
delay_cpy = delay # for acceleration purposes only; used when updating frames

init_x = -100
init_y = -300
init_pos = (init_x, init_y)

x_spawn = 4
y_spawn = 21

# other global variables 
score = 0
held = False
gameover = False

acceleration = False
accel_factor = 0.993

# instantiate a new turtle pen for rendering
tp = turtle.Turtle()
tp.penup()
tp.shape('square')
tp.speed('fastest')

# instantiate a Board object; default size is 10 * 20
board = Board(cell_item=0)

# generate a list of turtles to render each level of difficulty separately
level_turtle_lst = [turtle.Turtle() for _ in range(4)]
for t in level_turtle_lst:
    t.penup()
    t.hideturtle()
level_str_lst = ['(1) - Easy', '(2) - Medium', '(3) - Hard', '(4) - Expert']

# lists of available keys in each scene
main_keys = ['s', 't', 'd', 'q']
return_keys = ['b']
difficulty_keys = ['1', '2', '3', '4', 'f']
game_keys = ['Up', 'Down', 'Left', 'Right', 'z', 'c', 'space']
total_t_keys = main_keys + return_keys + difficulty_keys


# create the shape for the start of the game
pytro = None # the current pytro
pytro_next = pytromino_factory(Pytromino.Types(random.randint(1, 7))) # the next pytro
pytro_pos = (x_spawn, y_spawn) # position of the current pytro 

# create a holder for holding a block value
holder = Holder()

# overwrite get_board_item to avoid IndexError
def get_board_item_safe(board, x, y):
    global get_board_item
    try:
        return get_board_item(board, x, y)
    except:
        return 

def set_board_item_safe(board, x, y, item):
    global set_board_item
    try:
        return set_board_item(board, x, y, item)
    except:
        return 

shift_left_hof = lambda steps: lambda pos: shift_left_fn(pos, steps)
shift_down_hof = lambda steps: lambda pos: shift_down_fn(pos, steps)

def add_pos(p1, p2, p3=(0, 0)):
    assert all(map(lambda p: len(p) == 2, [p1, p2, p3])), "Position must be a two-element tuple"
    return p1[0] + p2[0] + p3[0], p1[1] + p2[1] + p3[1]

def mul_pos(p, multi):
    assert len(p) == 2, "Position must be a two-element tuple"
    return p[0] * multi, p[1] * multi 
 
def render_board(board, tp):
    """
    Renders the board with all the blocks. 
    """
    try: 
        tp.clear()
        for x in range(board.get_num_cols()):
            for y in range(board.get_num_rows() - 2):
                pos_x, pos_y = add_pos(init_pos, mul_pos((x, y), 20))
                pos_item = get_board_item_safe(board, x, y)
                # if pos_item:
                pos_color = colors[pos_item]
                tp.color(pos_color)
                tp.goto(pos_x, pos_y)
                tp.stamp()
    except Exception as err:
        pass

def render_pytro(pytro, tp, pytro_pos, checker, renderer):
    """
    Render a pytro in or out of the board.
    """
    pos_color = colors[pytro.get_index()]
    for i in pytro.blocks_pos:
        if checker(i):
            pos_x, pos_y = add_pos(init_pos, mul_pos(add_pos(pytro_pos, i), 20))
            tp.color(pos_color)
            tp.goto(pos_x, pos_y)
            renderer()

def render_pytro_in(pytro, tp, pytro_pos):
    """
    Render a pytro inside the board. 
    """
    try: 
        render_pytro(pytro, tp, pytro_pos, lambda i: pytro_pos[1] + i[1] < 20, tp.stamp)
    except Exception as er:
        pass

def render_pytro_out(pytro, tp, pytro_pos):
    """
    Render a pytro outside the board. 
    """
    render_pytro(pytro, tp, pytro_pos, lambda i: pytro_pos[1] + i[1] >= 20, tp.stamp)

def render_ghost(pytro, tp, ghost_pos):
    """
    Render a preview of the pytro on the board.
    """
    render_pytro(pytro, tp, ghost_pos, lambda i: True, tp.dot)

def render_score(tp, score):
    """
    Render the player's current score, the holder, and the next pytro during a game.
    """
    font_size = 20
    font_set = ("Arial", font_size, "normal")
    tp.color(colors[9])
    tp.hideturtle()
    tp.goto(50, 300)
    tp.write("Score: {}".format(score), move=False, align="left", font=font_set)
    tp.goto(-160, 200)
    tp.write("Holder:", move=False, align="left", font=font_set)
    tp.goto(20, 200)
    tp.write("Next:", move=False, align="left", font=font_set)

def render_holder(tp, holder):
    """
    Render the pytro in the holder. 
    """
    pytro_held = holder.get_item()
    new_pytro = pytromino_factory(Pytromino.Types(pytro_held.get_index()))
    render_pytro_out(new_pytro, tp, (0, 23))

def render_next(tp, pytro_next):
    """
    Render the next pytro. 
    """
    render_pytro_out(pytro_next, tp, (8, 23))

def check_all_rows(board):
    """
    Checks for and removes any full row from board.
    """
    try: 
        full_rows_idx = [i for i in range(board.get_num_rows()) if check_row_full(board, i)]
        counter = 0
        global score
        full_rows_total = len(full_rows_idx)
        if 0 < full_rows_total < 4:
            score += (full_rows_total * 2 - 1) * 100
        elif full_rows_total >= 4:
            score += 800
        for i in full_rows_idx:
            pop_row(board, i - counter)
            counter += 1
    except Exception as err:
        pass

# helper functions
def check_all_pos(checker, pytro, pytro_pos):
    return all([checker(pytro_pos, pos) for pos in pytro.blocks_pos])

def check_bottom(pytro, pytro_pos, dist):
    return check_all_pos(lambda p1, p2: p1[1] - dist + p2[1] > 0, pytro, pytro_pos)

def can_drop(pytro, board, dist=pytro_pos[1]):
    return check_all_pos(lambda p1, p2: (lambda p: not get_board_item_safe(board, p[0], p[1] - dist))(add_pos(p1, p2)), pytro, pytro_pos)

def can_left(pytro, board):
    return check_all_pos(lambda p1, p2: (lambda p: not get_board_item_safe(board, p[0] - 1, p[1]))(add_pos(p1, p2)), pytro, pytro_pos)

def can_right(pytro, board):
    return check_all_pos(lambda p1, p2: (lambda p: not get_board_item_safe(board, p[0] + 1, p[1]))(add_pos(p1, p2)), pytro, pytro_pos)

def can_rotate_cw(pytro, board):
    return check_all_pos(lambda p1, p2: (lambda p: not get_board_item_safe(board, p[0], p[1])) \
        (add_pos(add_pos(p1, p2), rotate_block_90_cw(pytro, p2))), pytro, pytro_pos)

def can_rotate_acw(pytro, board):
    return check_all_pos(lambda p1, p2: (lambda p: not get_board_item_safe(board, p[0], p[1])) \
        (add_pos(add_pos(p1, p2), rotate_block_90_ccw(pytro, p2))), pytro, pytro_pos)

def find_ghost_pos(board, pytro):
    i = 0
    while can_drop(pytro, board, i) and check_bottom(pytro, pytro_pos, i):
        i += 1
    if not can_drop(pytro, board, i):
        i -= 1
    return (pytro_pos[0], pytro_pos[1] - i)

def spawn_new_pytro():
    """
    Update pytro to be pytro_next, and pytro_next to be a new random pytromino. 
    """
    global pytro, pytro_next
    pytro = pytro_next
    pytro_next = pytromino_factory(Pytromino.Types(random.randint(1, 7)))

def pytro_in_grid(pytro):
    global board
    item = pytro.get_index()
    for i in pytro.blocks_pos:
        pos_x = pytro_pos[0] + i[0]
        pos_y = pytro_pos[1] + i[1]
        board = set_board_item_safe(board, pos_x, pos_y, item)

def rotation_cw():
    return lambda x: rotate_block_90_cw(pytro, x)

def rotation_acw():
    return lambda x: rotate_block_90_cw(pytro, rotate_block_90_cw(pytro, rotate_block_90_cw(pytro, x)))

def validator(coord, checker):
    return valid_coordinate(board, add_pos(pytro_pos, coord)) and checker(pytro, board)

def validator_left(coordinate):
    return validator(coordinate, can_left)

def validator_right(coordinate):
    return validator(coordinate, can_right)

def validator_down(coordinate):
    return validator(coordinate, can_drop)

def validator_rotate_cw(coordinate):
    return validator(coordinate, can_rotate_cw)

def validator_rotate_acw(coordinate):
    return validator(coordinate, can_rotate_acw)

def hold():
    global held, pytro, holder, pytro_pos
    if not held:
        if not holder.get_item():
            holder.store(pytro)
            spawn_new_pytro()
            pytro_pos = (x_spawn, y_spawn)
        else:
            dummy = holder.get_item()
            holder.store(pytro)
            pytro = dummy
            pytro_pos = (x_spawn, y_spawn)
        held = True  

def endpyt():
    global pytro, board, pytro_pos, held, ghost_pos, delay_cpy
    pytro_in_grid(pytro)
    check_all_rows(board)
    spawn_new_pytro()
    pytro_pos = (x_spawn, y_spawn)
    held = False
    ghost_pos = find_ghost_pos(board, pytro)
    if acceleration:
        delay_cpy *= accel_factor

def spawn_new_pytro():
    global pytro, pytro_next
    pytro = pytro_next
    pytro_next = pytromino_factory(Pytromino.Types(random.randint(1, 7)))
    
def rocket():
    global pytro_pos, ghost_pos
    ghost_pos = find_ghost_pos(board, pytro)
    pytro_pos = ghost_pos
    endpyt()

def check_over(board, pytro, pytro_pos):
    global gameover
    try: 
        for i in pytro.blocks_pos:
            if pytro_pos[1] + i[1] >= board.get_num_rows() - 2:
                gameover = not can_drop(pytro, board, 1)
    except Exception as err:
        pass

def play_game():
    try:    
        deactivate_all_keys()
        global board, gameover, delay_cpy, holder, score
        board = Board(cell_item=0)
        holder = Holder()
        score = 0
        gameover = False
        ws.listen()
        ws.onkeypress(lambda: validated_apply_safe("Left"), "Left")
        ws.onkeypress(lambda: validated_apply_safe("Right"), "Right")
        ws.onkeypress(lambda: validated_apply_safe("Up"), "Up")
        ws.onkeypress(lambda: validated_apply_safe("z"), "z")
        ws.onkeypress(lambda: validated_apply_safe("Down"), "Down")
        ws.onkeypress(lambda: hold(), "c")
        ws.onkeypress(lambda: rocket(), "space")
        ws.onkeypress(lambda: quit_game(), "q")
        delay_cpy = delay
    
        while not gameover:
            ws.update()

            # check for the bottom
            global pytro_pos
            for i in pytro.blocks_pos:
                pos_y = pytro_pos[1] + i[1]
                # if hit bottom
                if pos_y == 0:
                    endpyt()

            # check if the pytro can drop by one grid
            if can_drop(pytro, board, 1):
                pytro_pos = (pytro_pos[0], pytro_pos[1] - 1)
                render_pytro_in(pytro, tp, pytro_pos)
            else:
                endpyt()

            render_board(board, tp)
            if holder.get_item():
                render_holder(tp, holder)
            render_next(tp, pytro_next)
            render_pytro_in(pytro, tp, pytro_pos)
            ghost_pos = find_ghost_pos(board, pytro)
            render_ghost(pytro, tp, ghost_pos)
            render_score(tp, score)

            time.sleep(delay_cpy)

            check_over(board, pytro, pytro_pos)
        ws.update()
        game_over()
    except Exception as er:
        pass

def game_over():
    deactivate_all_keys()
    tp.clear()
    tp.goto((0, 0))
    tp.write('GAME OVER!', move=False, align="center", font=("Arial", 32, "normal"))
    tp.goto((0, -50))
    tp.write('Press (b) to return to main menu.', move=False, align="center", font=("Arial", 15, "italic"))
    turtle.listen()
    turtle.onkey(display_main_menu, 'b')
    ws.mainloop()
    tp.hideturtle()

def view_tutorial():
    deactivate_all_keys()
    tp.clear()
    align_str = 'left'
    font_setting = ("Cambria", 15, "normal")
    x_p = -200
    tp.goto((x_p, 200))
    tp.write('(key) - function', move=False, align=align_str, font=("Cambria", 15, "bold"))
    tp.goto((x_p, 150))
    tp.write('(up) - rotate the pytromino clockwise. ', move=False, align=align_str, font=font_setting)
    tp.goto((x_p, 100))
    tp.write('(z) - rotate the pytromino counterclockwise. ', move=False, align=align_str, font=font_setting)
    tp.goto((x_p, 50))
    tp.write('(down) - accelerate the drop. ', move=False, align=align_str, font=font_setting)
    tp.goto((x_p, 0))
    tp.write('(space) - hard-drop the pytromino. ', move=False, align=align_str, font=font_setting)
    tp.goto((x_p, -50))
    tp.write('(left) - left-shift the pytromino. ', move=False, align=align_str, font=font_setting)
    tp.goto((x_p, -100))
    tp.write('(right) - right-shift the pytromino. ', move=False, align=align_str, font=font_setting)
    tp.goto((x_p, -150))
    tp.write('(c) - put the pytromino in hold. ', move=False, align=align_str, font=font_setting)
    tp.goto((x_p, -200))
    tp.write('Note:', move=False, align=align_str, font=font_setting)
    tp.goto((x_p, -220))
    tp.write('If acceleration is ON, the pytro(s) will drop faster', move=False, align=align_str, font=font_setting)
    tp.goto((x_p, -240))
    tp.write('as the game proceeds. ', move=False, align=align_str, font=font_setting)
    tp.goto((x_p, -300))
    tp.write('Press (b) to go back to the main menu. ', move=False, align=align_str, font=("Cambria", 16, "italic"))
    turtle.listen() 
    turtle.onkey(display_main_menu, 'b')
    ws.mainloop()

def set_level(level, select=False):
    global delay
    t = level_turtle_lst[level]
    t.clear()
    t.hideturtle()
    t.goto(-50, 50 * (1 - level))
    sty = 'bold' if select else 'normal'
    if select:
        delay = 0.4 - level * 0.1
    t.write(level_str_lst[level], move=False, align='left', font=("Cambria", 15, sty))

spawn_new_pytro()
ghost_pos = find_ghost_pos(board, pytro)

easy_reset= lambda: set_level(0)
medium_reset = lambda: set_level(1)
hard_reset = lambda: set_level(2)
expert_reset = lambda: set_level(3)

def reset_all_levels():
    easy_reset()
    medium_reset()
    hard_reset()
    expert_reset()

def clear_and_set_level(level):
    reset_all_levels()
    set_level(level, True)

easy_select = lambda: clear_and_set_level(0)
medium_select = lambda: clear_and_set_level(1)
hard_select = lambda: clear_and_set_level(2)
expert_select = lambda: clear_and_set_level(3)

def select_difficulty():
    deactivate_all_keys()
    tp.clear()
    tp.goto((0, 100))
    tp.write('Select the difficulty of the game.', move=False, align='center', font=("Cambria", 20, "normal"))
    reset_all_levels()
    tp.goto((0, -200))
    tp.write('Press (f) to confirm', move=False, align='center', font=("Cambria", 15, "italic"))
    tp.goto((0, -220))
    tp.write('and return to the main menu.', move=False, align='center', font=("Cambria", 15, "italic"))
    turtle.listen()
    turtle.onkey(easy_select, '1')
    turtle.onkey(medium_select, '2')
    turtle.onkey(hard_select, '3')
    turtle.onkey(expert_select, '4')
    turtle.onkey(return_main_from_d, 'f')
    ws.mainloop()

def accelerate():
    global acceleration
    acceleration = not acceleration
    display_main_menu()


def return_main_from_d():
    deactivate_all_keys()
    for t in level_turtle_lst:
        t.clear()
        t.penup()
        t.hideturtle()
    display_main_menu()

def quit_game():
    try: 
        ws.bye()
    except Exception as err:
        pass

def deactivate_keys(keys, focus='turtle'):
    if focus == 'turtle':
        for k in keys:
            turtle.onkey(None, k)
    else:
        for k in keys:
            ws.onkeypress(None, k)

def deactivate_all_keys():
    deactivate_keys(total_t_keys, 'turtle')
    deactivate_keys(game_keys, 'screen')

def validated_apply_safe(key_pressed):
    global pytro
    if key_pressed == "Left":
        pytro = validated_apply(pytro, shift_left_hof(1), False, validator_left)
    elif key_pressed == "Right":
        pytro = validated_apply(pytro, shift_left_hof(-1), False, validator_right)
    elif key_pressed == "Up":
        pytro = validated_apply(pytro, rotation_cw(), True, validator_rotate_cw)
    elif key_pressed == "z":
        pytro = validated_apply(pytro, rotation_acw(), True, validator_rotate_acw)
    elif key_pressed == "Down":
        pytro = validated_apply(pytro, shift_down_hof(1), True, validator_down)


# initial interface 
def display_main_menu(): 
    global acceleration
    font_size = 18
    acc = 'ON' if acceleration else 'OFF'
    diff_level_str = level_str_lst[4 - round(delay * 10)][6:]
    upper_left_pos = -200
    deactivate_all_keys()
    tp.clear()
    tp.goto((0, 200))
    tp.write('Welcome to CS10 PROJ-V Pyturis!', move=False, align='center', font=("Cambria", font_size + 3, "bold"))
    tp.goto((0, 50))
    tp.write('Press (s) to start.', move=False, align='center', font=("Cambria", font_size, "normal"))
    tp.goto((0, 0))
    tp.write('Press (t) to view tutorial.', move=False, align='center', font=("Cambria", font_size, "normal"))
    tp.goto((0, -50))
    tp.write('Press (d) to select difficulty level.', move=False, align='center', font=("Cambria", font_size, "normal"))
    tp.goto((0, -100))
    tp.write('Press (a) to set acceleration', move=False, align='center', font=("Cambria", font_size, "normal"))
    tp.goto((0, -150))
    tp.write('Press (q) to quit.', move=False, align='center', font=("Cambria", font_size, "normal"))
    tp.goto((upper_left_pos,320))
    tp.write(f'acceleration: {acc}', move=False, align='left', font=("Cambria", 13, "normal"))
    tp.goto((upper_left_pos,300))
    tp.write(f'difficulty level: {diff_level_str}', move=False, align='left', font=("Cambria", 13, "normal"))
    tp.hideturtle()
    
    turtle.onkey(play_game, 's')
    turtle.onkey(view_tutorial, 't')
    turtle.onkey(select_difficulty, 'd')
    turtle.onkey(quit_game, 'q')
    turtle.onkey(accelerate, 'a')
    turtle.listen()
    ws.mainloop()
