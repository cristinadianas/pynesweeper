import curses
import time
import random

Y_MAX = 16
X_MAX = 30
RAND_MAX = 1000

# Dimensions
CELL_WIDTH = 5
CELL_HEIGHT = 3
COUNTER_WIDTH = 15
COUNTER_HEIGHT = 3
TIMER_WIDTH = 15
TIMER_HEIGHT = 3
STATUS_WIDTH = 30
STATUS_HEIGHT = 9
DISTANCE_FROM_BOARD = 3

# Colors
COLOR_DEFAULT = 0
MARKEDCELL_ON_BLACK = 1
GREEN_ON_BLACK = 2
BLACK_ON_BLACK = 3
RED_ON_BLACK = 4
MAGENTA_ON_BLACK = 5


class MinesweeperCell:
    def __init__(self):
        self.neighbours = 0
        self.stepped = False
        self.marked = False
        self.mine = False


def bsetup():
    print("\n DIFFICULTY: \n 1 = Beginner (9x9 - 10 Mines)  \n 2 = Medium (16x16 - 40 Mines) \n 3 = Difficult (30x16 - 99 Mines) \n 4 = Custom (max: 30x16 - 480 Mines) \n")

    class Board:
        cols = {
            1: 9,
            2: 16,
            3: 30
        }
        rows = {
            1: 9,
            2: 16,
            3: 16
        }
        mines = {
            1: 10,
            2: 40,
            3: 99
        }

    while (level := int(input())) < 1 or level > 4:
        print("Please enter a valid level of difficulty.")

    if 1 <= level <= 3:
        return Board.cols[level], Board.rows[level], Board.mines[level]

    while (num_cols := int(input("Width = "))) < 1 or num_cols > X_MAX:
        print(f"\nPlease make sure the width entered is in the range 1 to {X_MAX}.")

    while (num_rows := int(input("Height = "))) < 1 or num_rows > Y_MAX:
        print(f"\nPlease make sure the height entered is in the range 1 to {Y_MAX}.")

    while (num_mines := int(input("Mines = "))) < 0 or num_mines > num_cols * num_rows:
        print("\nPlease make sure the number of mines entered is neither greater than the area of the board nor negative.")

    return num_cols, num_rows, num_mines


def valid_cell(row, col):
    global board_rows, board_cols
    if 0 <= row < board_rows and 0 <= col < board_cols:
        return True
    return False


def create_newwin(height, width, starty, startx):
    local_win = curses.newwin(height, width, starty, startx)
    local_win.immedok(True)
    local_win.box()  # 0, 0 gives default characters for the vertical and horizontal lines
    return local_win


def show_in_win(row, col, character, color_pair):
    global winindex
    winindex[row][col].bkgd(curses.color_pair(color_pair))
    # winindex[row][col].wattron(curses.color_pair(color_pair))
    winindex[row][col].addstr(int(CELL_HEIGHT / 2), int(CELL_WIDTH / 2), f"{character}")
    # winindex[row][col].wattroff(curses.color_pair(color_pair))


def move_cursor(row, col, here=True):
    global winindex
    if here:
        winindex[row][col].addch(int(CELL_HEIGHT / 2), int(CELL_WIDTH / 2 - 1), '[')
        winindex[row][col].addch(int(CELL_HEIGHT / 2), int(CELL_WIDTH / 2 + 1), ']')
    else:
        winindex[row][col].addch(int(CELL_HEIGHT / 2), int(CELL_WIDTH / 2 - 1), ' ')
        winindex[row][col].addch(int(CELL_HEIGHT / 2), int(CELL_WIDTH / 2 + 1), ' ')


def go_left(row, col):
    if col > 0:
        move_cursor(row, col, False)
        col -= 1
        move_cursor(row, col)
    return row, col
def go_right(row, col):
    if col < board_cols - 1:
        move_cursor(row, col, False)
        col += 1
        move_cursor(row, col)
    return row, col
def go_up(row, col):
    if row > 0:
        move_cursor(row, col, False)
        row -= 1
        move_cursor(row, col)
    return row, col
def go_down(row, col):
    if row < board_rows - 1:
        move_cursor(row, col, False)
        row += 1
        move_cursor(row, col)
    return row, col


def num_markedneighb(row, col):
    global cell
    neighbours = 0
    for y0 in range(row - 1, row + 2):
        for x0 in range(col - 1, col + 2):
            if valid_cell(y0, x0) is True and cell[y0][x0].marked is True:
                neighbours += 1
    return neighbours


def zero_pressed(row, col):
    global winindex, cell, num_stepped_cells
    num_stepped_cells += 1
    cell[row][col].stepped = True
    winindex[row][col].erase()
    for y0 in range(row - 1, row + 2):
        for x0 in range(col - 1, col + 2):
            if valid_cell(y0, x0) is True and cell[y0][x0].stepped is False and cell[y0][x0].marked is False:
                if cell[y0][x0].neighbours == 0:
                    zero_pressed(y0, x0)
                else:
                    num_stepped_cells += 1
                    cell[y0][x0].stepped = True
                    show_in_win(y0, x0, cell[y0][x0].neighbours, GREEN_ON_BLACK)


def newcell_pressed(row, col):
    global winindex, cell, num_stepped_cells, stepped_on_a_mine
    if cell[row][col].mine is True:
        cell[row][col].stepped = True
        stepped_on_a_mine = True
    elif cell[row][col].neighbours == 0:
        zero_pressed(row, col)
    else:
        num_stepped_cells += 1
        cell[row][col].stepped = True
        show_in_win(row, col, cell[row][col].neighbours, GREEN_ON_BLACK)


board_rows, board_cols, total_mines = bsetup()

exit_requested = False
while exit_requested is False:

    cell = [[MinesweeperCell() for i in range(board_cols)] for j in range(board_rows)]
    laid_mines = 0
    for y in range(board_rows):
        for x in range(board_cols):
            if total_mines - laid_mines != 0 and random.randint(1, RAND_MAX) < (RAND_MAX * (total_mines - laid_mines) / (board_rows * board_cols - (y * board_cols + x))):
                cell[y][x].mine = True
                laid_mines += 1
                for i in range(y-1, y+2):
                    for j in range(x-1, x+2):
                        if valid_cell(i, j) is True and cell[i][j].mine is False:
                            cell[i][j].neighbours += 1

# Enter curses mode
    stdscr = curses.initscr()
    stdscr.keypad(True)
    stdscr.nodelay(True)
    stdscr.refresh()
    curses.cbreak()
    curses.noecho()
    curses.curs_set(False)
# Initialize colors
    curses.start_color()
    COLOR_MARKEDCELL = curses.COLOR_YELLOW
    if curses.can_change_color() is True:
        COLOR_MARKEDCELL = 8
        curses.init_color(COLOR_MARKEDCELL, 1000, 369, 55)  # Orange RGB: 255, 94, 14
    curses.init_pair(MARKEDCELL_ON_BLACK, COLOR_MARKEDCELL, curses.COLOR_BLACK)
    curses.init_pair(GREEN_ON_BLACK, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(BLACK_ON_BLACK, curses.COLOR_BLACK, curses.COLOR_BLACK)
    curses.init_pair(RED_ON_BLACK, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(MAGENTA_ON_BLACK, curses.COLOR_MAGENTA, curses.COLOR_BLACK)

    winindex = [[create_newwin(CELL_HEIGHT, CELL_WIDTH, i*CELL_HEIGHT, j*CELL_WIDTH) for j in range(board_cols)] for i in range(board_rows)]
    num_marked_cells, num_stepped_cells = (0, 0)
    stepped_on_a_mine = False

    counter = create_newwin(COUNTER_HEIGHT, COUNTER_WIDTH, 0, board_cols * CELL_WIDTH + DISTANCE_FROM_BOARD)
    counter.addstr(1, 2, f"{num_marked_cells}/{total_mines} Mines ")

    status = create_newwin(STATUS_HEIGHT, STATUS_WIDTH, COUNTER_HEIGHT, board_cols * CELL_WIDTH + DISTANCE_FROM_BOARD)
    status.addstr(4, 7, "You've got this!")

    start_clock = time.time()
    timer = create_newwin(TIMER_HEIGHT, TIMER_WIDTH, 0, board_cols * CELL_WIDTH + COUNTER_WIDTH + DISTANCE_FROM_BOARD)
    timer.addstr(1, 2, f"{int(time.time() - start_clock)} seconds")

    move_cursor(0, 0)
    x, y = (0, 0)

    while stepped_on_a_mine is False and num_stepped_cells != (board_rows * board_cols) - total_mines and exit_requested is False:
        while (ch := stdscr.getch()) == curses.ERR or ch == curses.KEY_LEFT or ch == curses.KEY_RIGHT or ch == curses.KEY_UP or ch == curses.KEY_DOWN:
            if ch != curses.ERR:
                y, x = {
                    curses.KEY_LEFT: go_left,
                    curses.KEY_RIGHT: go_right,
                    curses.KEY_UP: go_up,
                    curses.KEY_DOWN: go_down
                }[ch](y, x)
            timer.addstr(1, 2, f"{int(time.time() - start_clock)} seconds")

        if ch == ord(' '):
            if cell[y][x].marked is False and cell[y][x].stepped is False:
                newcell_pressed(y, x)
            elif cell[y][x].stepped is True and num_markedneighb(y, x) == cell[y][x].neighbours:
                for i in range(y-1, y+2):
                    for j in range(x-1, x+2):
                        if valid_cell(i, j) is True and cell[i][j].marked is False and cell[i][j].stepped is False:
                            newcell_pressed(i, j)
        elif ch == ord('x'):
            if cell[y][x].stepped is False:
                if cell[y][x].marked is False:
                    num_marked_cells += 1
                    counter.addstr(1, 2, f"{num_marked_cells}/{total_mines} Mines ")
                    if num_marked_cells - 1 == total_mines:
                        counter.bkgd(curses.color_pair(RED_ON_BLACK))
                        curses.beep()
                    show_in_win(y, x, 'x', MARKEDCELL_ON_BLACK)
                    cell[y][x].marked = True
                else:
                    num_marked_cells -= 1
                    counter.addstr(1, 2, f"{num_marked_cells}/{total_mines} Mines ")
                    if num_marked_cells == total_mines:
                        counter.bkgd(curses.color_pair(COLOR_DEFAULT))
                    show_in_win(y, x, ' ', COLOR_DEFAULT)
                    cell[y][x].marked = False
        elif ch == 27:  # ESC
            exit_requested = True
        move_cursor(y, x)

    status.addstr(4, 1, "                            ")
    status.addstr(5, 3, "Press any key besides ESC")
    status.addstr(6, 9, "to continue.")

    move_cursor(y, x, False)

    if num_stepped_cells == (board_rows * board_cols) - total_mines and exit_requested is False:  # WIN
        status.addstr(3, 11, "YOU WON")
        status.bkgd(curses.color_pair(GREEN_ON_BLACK))
        counter.bkgd(curses.color_pair(GREEN_ON_BLACK))
        timer.bkgd(curses.color_pair(GREEN_ON_BLACK))
        counter.addstr(1, 2, f"{total_mines}/{total_mines} Mines ")

        for i in range(board_rows):
            for j in range(board_cols):
                if cell[i][j].marked is False and cell[i][j].mine is True:
                    show_in_win(i, j, 'x', MARKEDCELL_ON_BLACK)
        while (ch := stdscr.getch()) == curses.ERR:
            pass

    elif exit_requested is False:  # LOSE
        curses.flash()
        status.addstr(3, 11, "YOU LOST")
        status.bkgd(curses.color_pair(RED_ON_BLACK))
        counter.bkgd(curses.color_pair(RED_ON_BLACK))
        timer.bkgd(curses.color_pair(RED_ON_BLACK))

        for i in range(board_rows):
            for j in range(board_cols):
                if cell[i][j].marked is False and cell[i][j].mine is True:
                    show_in_win(i, j, '*', RED_ON_BLACK)
                elif cell[i][j].marked is True and cell[i][j].mine is False:
                    show_in_win(i, j, 'x', MAGENTA_ON_BLACK)

        while (ch := stdscr.getch()) == curses.ERR:
            for i in range(y-1, y+2):
                for j in range(x-1, x+2):
                    if valid_cell(i, j) is True and cell[i][j].mine is True and cell[i][j].stepped is True:
                        winindex[i][j].bkgd(curses.color_pair(BLACK_ON_BLACK))
            time.sleep(0.1)
            for i in range(y-1, y+2):
                for j in range(x-1, x+2):
                    if valid_cell(i, j) is True and cell[i][j].mine is True and cell[i][j].stepped is True:
                        winindex[i][j].bkgd(curses.color_pair(RED_ON_BLACK))
            time.sleep(0.1)

    if ch == 27:  # ESC
        exit_requested = True
        curses.nocbreak()
        curses.echo()
        curses.endwin()
