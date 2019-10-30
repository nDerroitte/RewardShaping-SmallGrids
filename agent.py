import math
from copy import copy, deepcopy
from grid import *

###############################################################################
#                               Agent Class                                   #
###############################################################################


class Agent:
    def __init__(self, discount_factor=0.99, size = 5, reward = "RS"):
        """
        Parameters
        ----------
        discount_factor : float, optional
            Parameter for the discount factor. Corresponds to gamma in theory
        """
        self.__grid = Grid(size = size, reward=reward)
        self.__gamma = discount_factor

    def followPolicy(self, policy, N = 1000, discount_factor = 0.99, display = False):
        """
        Move and display the agent  following the policy of always going up in
        the grid. Corresponds to the Q2 of the project.

        Parameters
        ----------
        N : int, optional
            Number of iterations wanted
        policy : list
            Direction to take
        """

        # Printing the initial grid
        if display:
            print("Initial grid : ")
            self.__grid.print()

        agent_pos_index = 0
        reward = 0
        j = 0

        # N iterations
        for i in range(N):
            if display:
                print("Iteration {}:".format(i))
            # Moving the agent up and printing the new corresponding grid
            self.__grid.moveAgent(policy[agent_pos_index])
            x, y  = self.__grid.getAgentPos()
            agent_pos_index = y * self.__grid.width + x
            reward += self.__grid.getRewardIndex(agent_pos_index)
            j += self.__grid.getRewardIndex(agent_pos_index) * pow(discount_factor, i)
            if display:
                self.__grid.print()
            if agent_pos_index == self.__grid.end_pos_index:
                break

        print(" * Total reward : {}.\n * Number of steps : {}".format(reward, i+1))
        if i == (self.__grid.size * 2)-2 -1:
            print(" * Optimal policy found!")
        else:
            print(" * Optimal policy not found..")


    def computeJ(self, policy, N=3, display=True):
        """
        Compute and display JN(x) from the initial grid. Corresponds to the
        Q3 of the project.

        Parameters
        ----------
        policy : list
            Stationary policy the agent will follow
        N : int, optional
            Number of iterations wanted
        display : bool, optional
            Bool to display or not the result

        Returns
        -------
        list
            J_mu^N
        """
        # To optimize the computation, the matrix containing Jn-1 can be safed.
        # `previous_Jmatrix` corresponds to this Jn-1 matrix. It is instiated
        # with 0 as J0(x) = 0 for all x.
        previous_Jmatrix = [[0 for k in range (self.__grid.size)] for i in range(self.__grid.size)]

        # `current_Jmatrix` corresponds to the matrix containing the Jn values
        current_Jmatrix = deepcopy(previous_Jmatrix)

        # N iterations
        for n in range(1, N+1):
            # Going over the grid from top left to bottom right
            for y in range(self.__grid.height):
                for x in range(self.__grid.width):
                    if x == self.__grid.width -1 and y == self.__grid.height -1:
                        if n == N and display:
                            print(str("10.0").rjust(8), end=' ')
                        continue
                    # Computing the index corresponding to the 1D matrix
                    index = y * self.__grid.width + x
                    # Getting the direction from the policy
                    dir = policy[index]
                    # Computing`previous_J` and `previous_J_beta` which
                    # corresponds to Jn-1(f(x, µ(x), w)) from the definition
                    previous_J = getFromMatrix(dir, previous_Jmatrix, x, y)
                    # first_term corresponds to the deterministic case
                    Jx = (getFromGrid(dir, self.__grid, x, y) + self.__gamma * previous_J)
                    # Jn(x) is safed to be reused in futur computation
                    current_Jmatrix[y][x] = Jx
                    # Printing the result in a "array way"
                    if n== N and display:
                        print(str(round(Jx, 2)).rjust(8), end=' ')
                # Line break in the array display
                if n == N and display:
                    print(" ")
            # Preparing next iterations by setting the matrix Jn as Jn-1
            previous_Jmatrix = deepcopy(current_Jmatrix)
        # Returning last J computed
        return current_Jmatrix

    def getSimplePolicy(self, dir):
        """
        Generate a simple policy of always going to the same direction

        Parameters
        ----------
        dir : {0, 1, 2, 3}
            Direction wanted.

        Returns
        -------
        list[{0, 1, 2, 3}]
            The corresponding stationary policy
        """
        policy = []
        for i in range(len(self.__grid.matrix1D)):
            policy.append(dir)
        return policy
