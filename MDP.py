from grid import *
from batch import *
from copy import copy, deepcopy
import math

###############################################################################
#                               MDP Class                                    #
###############################################################################


class MDP:
  def __init__(self, discount_factor=0.99, learning_ratio=0.0, b_s=5000,size = 5,reward = "RS"):
    """
    Parameters
    ----------
    discount_factor : float, optional
      Parameter for the discount factor. Corresponds to gamma in theory
    learning_ratio : float, optional
      Parameter for the learning ratio. Corresponds to alpha in theory
    b_s : int, optional
      Length of the batch used in the Q6
    """
    self.__grid = Grid(size = size, reward=reward)
    self.__gamma = discount_factor
    self.__alpha = learning_ratio
    self.batch = Batch(b_s)
    self.batch_size = b_s

  def getPolicyFromQ(self, Q):
    """
    Compute the optimal policy from the computation of Q(x, u).
    This function works both when estimating r and p (history != None) and
    while workong with the real values of r and p (history = None)

    Parameters
    ----------
    Q : list[list[float]]
      Q(x, u)

    Returns
    -------
    list[{0, 1, 2, 3}]
      mu^*(x) : the optimal stationary policy.
    """
    policy = []

    for x in range(len(self.__grid.matrix1D)):
      # Getting the best action from Q for all x in X
      policy.append(self.__bestAction(Q, x))
    return policy

  def __bestAction(self, matrix, index):
    """
    Compute the optimal action to take based on Q and the position in the grid

    Parameters
    ----------
    Q : list[list[float]]
      Q(x, u)
    index : int
      Position in the grid using indexes

    Returns
    -------
    {0, 1, 2, 3}
      The optimal direction to take from index in the grid based on Q(x, u)
    """
    action = -1
    # initialization of max
    max = -float('Inf')
    # Simple max algo for all actions u in U
    for i in range(NUMBER_ACTIONS):
      if matrix[index][i] > max:
        max = matrix[index][i]
        action = i

    return action

  def __maxQ(self, Q, index):
    """
    Compute the best Q(x, u) for all x in X

    Parameters
    ----------
    Q : list[list[float]]
      Q(x, u)
    index : int
      Position in the grid using indexes

    Returns
    -------
    float
      max_{u in U} Q(index, u) : max Q in all the direction possible
    """
    max = -float('Inf')
    for i in range(NUMBER_ACTIONS):
      max = Q[index][i] if Q[index][i] > max else max
    return max

  def createHistory(self, T=50, policy=None, starting_pos=None, epsilon=0.0, PBRS = False):
      """
      Create a feasible trajectory of size T. Can be totally random or follow
      a specific policy. Can start at random or at a starting position

      Parameters
      ----------
      T: int, optional
        Size of the trajectory
      policy : list[{0, 1, 2, 3}], optional
        The policy to follow if wanted
      starting_pos : int
        The index of the starting position
      epsilon : float; optional
        Epsilon parameter for the e-greedy policy

      Returns
      -------
      list[x0, u0, r0, x1, ... xt−1, ut−1, rt−1, xt]
        Trajectory of size T
      """
      h = []
      if starting_pos is None:
        # Getting a random starting position
        starting_pos = random.randint(0, len(self.__grid.matrix1D)-1)
      for t in range(0, T):
        # Initial case : start at starting position
        if t == 0:
          next_x = starting_pos
        previous_x = next_x

        h.append(next_x)

        if policy is None:
          # Random legal action
          action = random.randint(0, NUMBER_ACTIONS-1)
        else:
          r = random.uniform(0, 1)
          if r < epsilon:
            # Getting a random action
            action = random.randint(0, NUMBER_ACTIONS-1)
          else:
            action = policy[next_x]
        h.append(action)

        next_x = getIndexFromMatrix(action, self.__grid.matrix, next_x)
        # Adding the reward for going to the next x
        if PBRS :
            h.append(self.__gamma * self.__grid.getRewardIndex(next_x) - self.__grid.getRewardIndex(previous_x))
        else:
            h.append(self.__grid.getRewardIndex(next_x))
      # Adding xt, the last position
      h.append(next_x)
      return h


  def getQlearning(self, nb_episodes, T, epsilon, PBRS = False):
    """
    Estimate Q using the Q_learning algorithm.

    Parameters
    ----------
    nb_episodes : int
      Number of eposides used in the Q-learing algorithm
    T : int
      Size of the trajectories, ie the number of transitions.
    epsilon : float
      Epsilon parameter for the e-greedy policy

    Returns
    -------
    list[list[float]]
      Q(x, u)
    """
    # Initialization of Q variables
    Q = [[0, 0, 0, 0]for j in range(len(self.__grid.matrix1D))]
    policy = self.getPolicyFromQ(Q)
    epsilon_max = epsilon
    # For the number of episodes
    for k in range(nb_episodes):
      # Getting a trajectory following the current Q computed
      s = 0
      r_tot = 0
      first_time = 1
      for t in range(T):
        exp = self.createHistory(1, policy, s, epsilon, PBRS)
        r_tot += exp[2]
        next_s = exp[3]
        if s == 90 and first_time:
          print("reward  apres: ",exp[2])
          first_time = 0
        if next_s == 90 and first_time:
          print("reward : ",exp[2])
        if self.batch.isFull():
          for h in random.sample(self.batch.batch, self.batch_size):
            x = h[0]
            u = h[1]
            r = h[2]
            x_next = h[3]

            Q[x][u] = (1 - self.__alpha) * Q[x][u] + (self.__alpha) * (
                       r + self.__gamma * self.__maxQ(Q, x_next))
          self.batch.empty()
          policy = self.getPolicyFromQ(Q)

        self.batch.add(exp)
        s = next_s
        if s == self.__grid.end_pos_index:
          break
      self.__grid.resetReward()
      #print("Episode {} ended with reward {} after {} steps. Espilon is equals to {}".format(k, r_tot, t+1, epsilon))
      epsilon -= (epsilon_max/nb_episodes)

    return Q

  def getQlearningFromTrajectories(self, list_traj):
    """
    Estimate Q using the Q_learning algorithm.

    Parameters
    ----------
    list_traj : list[list[x0, u0, r0, x1, ... xt−1, ut−1, rt−1, xt]]
      `Number of eposides` trajectories of size T

    Returns
    -------
    list[list[float]]
      Q(x, u)
    """
    # Initialization of Q variables
    Q = [[0 , 0, 0, 0]for j in range(len(self.__grid.matrix1D))]

    for k in range(len(list_traj)):
      for t in range(0, len(list_traj[0])-1, 3):
        x = list_traj[k][t]
        u = list_traj[k][t+1]
        r = list_traj[k][t+2]
        x_next = list_traj[k][t+3]

        Q[x][u] = (1 - self.__alpha) * Q[x][u] + (self.__alpha) * (
                   r + self.__gamma * self.__maxQ(Q, x_next))

    return Q
