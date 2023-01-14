"""Algorithm to solve magic hexagon problem."""
from collections import deque
from time import time
from typing import Deque, List, Set

# Problem description
FLOORS = 3
ROWS_NB = 2*FLOORS-1
CELLS_NB = 3*FLOORS*(FLOORS-1)+1
NUMBERS = range(1, CELLS_NB+1)
LINE_SUM = sum(range(1, CELLS_NB+1)) // ROWS_NB

# Algo global variables
assert FLOORS == 3
BOARD_INDEXES_STR = """
    00.  01.  03.
  02.  13.  14.  05.
04.  12.  18.  15.  06.
  11.  17.  16.  07.
    10.  09.  08.
"""
# Modified snail
X_LINES = [[0, 1, 3], [2, 13, 14, 5], [4, 12, 18, 15, 6], [11, 17, 16, 7], [10, 9, 8]]
Y_LINES = [[0, 2, 4], [1, 13, 12, 11], [3, 14, 18, 17, 10], [5, 15, 16, 9], [6, 7, 8]]
Z_LINES = [[4, 11, 10], [2, 12, 17, 9], [0, 13, 18, 16, 8], [1, 14, 15, 7], [3, 5, 6]]

LINES_ENDED_BY_STEP = [
    [
        line
        for line in X_LINES + Y_LINES + Z_LINES
        if max(line) == i
    ] for i in range(19)
]
CORNERS_EXCEPT_FIRST = {2, 4, 6, 8, 10}
FIRST_SIDE = 1
LAST_SIDE = 2


def display_board(board: List[int]):
    """Nice display of board"""
    string = BOARD_INDEXES_STR
    for i, n in enumerate(board):
        string = string.replace(f'{i:02d}.', f'{n:2d}')
    print(string)


def look_for_solutions_(
        board: List[int],
        remaining_numbers: Deque[int],
        step: int,

        # Cache
        corners_tested: Set[int],
        first_side_test: Set[int],
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
        print(f'Solution found in {(time() - start_time)*1000:.1f}ms')
        display_board(board)
        return

    for _ in range(CELLS_NB-step):
        # If step is on corner and number has already been tested as a corner, skip it
        # # Avoid rotations this way
        number = remaining_numbers.popleft()
        if step in CORNERS_EXCEPT_FIRST and number in corners_tested:
            remaining_numbers.append(number)
            continue
        # Remove symetrical solutions
        if step == LAST_SIDE and number in first_side_test:
            remaining_numbers.append(number)
            continue

        # Add number to board and get next remaining numbers
        board[step] = number

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
            look_for_solutions_(
                board,
                remaining_numbers,
                step+1,
                corners_tested=corners_tested,
                first_side_test=first_side_test,
                start_time=start_time,
            )

        # Add the removed number for the next iteration
        remaining_numbers.append(number)
        # Number has been fully explored as first corner
        if step == 0:
            corners_tested.add(number)
            first_side_test=set()
        if step == FIRST_SIDE:
            first_side_test.add(number)

    return


def look_for_solutions():
    start = time()
    look_for_solutions_(
        board=[0] * CELLS_NB,
        remaining_numbers=deque(NUMBERS),
        step=0,
        corners_tested=set(),
        first_side_test=set(),
        start_time=start,
    )
    print(f'Full run ended in {(time() - start)*1000:.1f}ms')


if __name__ == '__main__':
    look_for_solutions()
