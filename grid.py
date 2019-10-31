import random

###############################################################################
#                               Constants                                     #
###############################################################################
UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3
NUMBER_ACTIONS = 4
###############################################################################
#                               Grid Class                                    #
###############################################################################


class Grid:
    def __init__(self, size = 5, reward="RS"):
        # Initial reward grid
        self.matrix = [[0 for k in range (size)] for i in range(size)]
        self.matrix[size-1][size-1] = 0
        self.matrix1D = [0 for i in range(size*size)]
        self.matrix1D[size*size -1] = 0
        self.width = len(self.matrix[0])
        self.height = len(self.matrix)
        self.size = size
        self.__init_pos = [0, 0]
        self.__end_pos = [size - 1, size - 1]
        self.end_pos_index = size*size - 1
        self.__agent_pos = self.__init_pos
        self.__reward = reward

    def print(self):
        """
        Display the reward grid where the agent is located by a *
        """
        for y in range(self.height):
            for x in range(self.width):
                # Case where the agent is located on the current cell
                if [x, y] == self.__agent_pos:
                    print((str(self.getReward(x,y))+"*").rjust(4), end='')
                else:
                    print(str(self.getReward(x,y)).rjust(4), end='')
            # Line break
            print(" ")

    def getReward(self, x, y):
        if self.__reward == "sparse":
            if [x, y] == self.__end_pos:
                return 1
            else:
                return 0
        elif self.__reward == "heuristic":
            if [x, y] == self.__end_pos:
                return 1000
            if [x, y] == [0, self.height-1]:
                return 500
            else:
                # Reward qui minimise la mahantan distance
                r = (abs(0 - x) + abs(0 - y))
                return r

        return self.matrix[y][x]

    def getRewardIndex(self, index):
        x = index % self.width
        y = index // self.width
        return self.getReward(x, y)

    def getAgentPos(self):
        return self.__agent_pos

    def moveAgent(self, direction):
        """
        Move the agent in the grid

        Parameters
        ----------
        direction : {0, 1, 2, 3}
            Direction wanted. 0 = UP, 1 = RIGHT, 2 = DOWN, 3 = LEFT
        """
        if direction == UP and self.__agent_pos[1] > 0:
            self.__agent_pos[1] -= 1
        elif direction == RIGHT and self.__agent_pos[0] < self.width-1:
            self.__agent_pos[0] += 1
        elif direction == DOWN and self.__agent_pos[1] < self.height-1:
            self.__agent_pos[1] += 1
        elif direction == LEFT and self.__agent_pos[0] > 0:
            self.__agent_pos[0] -= 1

###############################################################################
#                               Functions                                     #
###############################################################################


def getFromMatrix(dir, matrix, x, y):
    """
    Get the cell next to [x][y] in the direction `dir` in a matrix `matrix`

    Parameters
    ----------
    dir : {0, 1, 2, 3}
        Direction wanted. 0 = UP, 1 = RIGHT, 2 = DOWN, 3 = LEFT
    matrix : matrix of float
        Matrix from where the cells are selected
    x, y : int
        Position of the initial cell in the matrix

    Returns
    -------
    float
        The cell next to [x][y] in the direction `dir in the matrix
        `matrix`
    """

    # {UP, RIGHT, DOWN, LEFT} are constants fixed in grid.py
    if dir == UP and y > 0:
        return matrix[y-1][x]
    elif dir == RIGHT and x < len(matrix[0])-1:
        return matrix[y][x+1]
    elif dir == DOWN and y < len(matrix)-1:
        return matrix[y+1][x]
    elif dir == LEFT and x > 0:
        return matrix[y][x-1]
    else:
        # Happen in the case where to agent is located next to a wall and
        # makes a move toward this wall
        return matrix[y][x]

def getFromGrid(dir, grid, x, y):
    """
    Get the cell next to [x][y] in the direction `dir` in a grid `grid`

    Parameters
    ----------
    dir : {0, 1, 2, 3}
        Direction wanted. 0 = UP, 1 = RIGHT, 2 = DOWN, 3 = LEFT
    grid : Grid object
    x, y : int
        Position of the initial cell in the matrix

    Returns
    -------
    float
        The cell next to [x][y] in the direction `dir in the matrix
        `matrix`
    """

    # {UP, RIGHT, DOWN, LEFT} are constants fixed in grid.py
    if dir == UP and y > 0:
        return grid.getReward(x, y-1)
    elif dir == RIGHT and x < len(grid.matrix[0])-1:
        return grid.getReward(x+1, y)
    elif dir == DOWN and y < len(grid.matrix)-1:
        return grid.getReward(x, y+1)
    elif dir == LEFT and x > 0:
        return grid.getReward(x-1, y)
    else:
        # Happen in the case where to agent is located next to a wall and
        # makes a move toward this wall
        return grid.getReward(x, y)

def getIndexFromMatrix(dir, matrix, index):
    """
    Get the cell next in the direction dir from the index in the matrix.
    The trick is that the matrix is in 2D and the index in consider a 1D
    matrix.

    Parameters
    ----------
    dir : {0, 1, 2, 3}
        Direction wanted. 0 = UP, 1 = RIGHT, 2 = DOWN, 3 = LEFT
    matrix : matrix of float
        Matrix from where the cells are selected
    index : int
        Position of the initial cell in the matrix

    Returns
    -------
    int
        Index of the cell next to the starting positon `index` in the direction
        `dir in the matrix `matrix`
    """
    # Computing corresponding x, y
    x = index % len(matrix[0])
    y = index // len(matrix[0])
    if dir == UP:
        return index - len(matrix[0]) if y > 0 else index
    if dir == RIGHT:
        return index+1 if x < len(matrix[0]) - 1 else index
    if dir == DOWN:
        return index + len(matrix[0]) if y < len(matrix) - 1 else index
    if dir == LEFT:
        return index-1 if x > 0 else index
