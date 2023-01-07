"""Algorithm to solve magic hexagon problem"""
from time import time
from typing import List, Set

# Problem description
FLOORS = 3
ROWS_NB = 2*FLOORS-1
CELLS_NB = 3*FLOORS*(FLOORS-1)+1
NUMBERS = list(range(1, CELLS_NB+1))
LINE_SUM = sum(range(1, CELLS_NB+1)) // ROWS_NB

# Algo global variables
assert FLOORS == 3
BOARD_INDEXES_STR = """
    00.  01.  02.
  11.  12.  13.  03.
10.  17.  18.  14.  04.
  09.  16.  15.  05.
    08.  07.  06.
"""
X_LINES = [[0, 1, 2], [11, 12, 13, 3], [10, 17, 18, 14, 4], [9, 16, 15, 5], [8, 7, 6]]
Y_LINES = [[0, 11, 10], [1, 12, 17, 9], [2, 13, 18, 16, 8], [3, 14, 15, 7], [4, 5, 6]]
Z_LINES = [[10, 9, 8], [11, 17, 16, 7], [0, 12, 18, 15, 6], [1, 13, 14, 5], [2, 3, 4]]
LINES_ENDED_BY_STEP = [
    [
        line
        for line in X_LINES + Y_LINES + Z_LINES
        if max(line) == i
    ] for i in range(19)
]
CORNERS_EXCEPT_FIRST = {2, 4, 6, 8, 10}


def display_board(board: List[int]):
    """Nice display of board"""
    string = BOARD_INDEXES_STR
    for i, n in enumerate(board):
        string = string.replace(f'{i:02d}.', f'{n:02d}')
    print(string)


def look_for_solutions(
        board: List[int],
        remaining_numbers: List[int],
        step: int,

        # Cache
        corners_tested: Set[int],
        start_time: float,
) -> None:
    """Look for solutions given board state and step to start from

    About:
        step define the index in board to place next number in (within remaining numbers)

    Assumptions:
        step <= CELLS_NB
        board is completed until index (step-1)
        each line that is completed has a sum of LINE_SUM
        each number is unique in the union of board and remaining_numbers and included in NUMBERS (except 0)
        corner_tested contains every number that has been completely tested as a first corner
        start_time i the time in secs when the search has started
    """
    if not remaining_numbers:
        print(f'Solution found in {time() - start_time}s:')
        display_board(board)
        return

    for i, number in enumerate(remaining_numbers):
        # If step is on corner and number has already been tested as a corner, skip it
        # # Avoid rotations this way
        if step in CORNERS_EXCEPT_FIRST and number in corners_tested:
            continue

        # Add number to board and get next remaining numbers
        next_numbers = [*remaining_numbers]
        board[step] = next_numbers.pop(i)

        # Check whether lines we ended have the right sum
        for line in LINES_ENDED_BY_STEP[step]:
            # Faster to implement sum this way
            line_sum = 0
            for index in line:
                line_sum += board[index]
            if line_sum != LINE_SUM:
                break
        else:
            # Completed lines are correct, we may continue
            look_for_solutions(
                board,
                next_numbers,
                step+1,
                corners_tested=corners_tested,
                start_time=start_time,
            )

        # Number has been fully explored as first corner
        if step == 0:
            corners_tested.add(number)

    return


start = time()
look_for_solutions(
    board=[0] * CELLS_NB,
    remaining_numbers=[*NUMBERS],
    step=0,
    corners_tested=set(),
    start_time=start,
)
print(f'Full run ended in {time()-start}s')
