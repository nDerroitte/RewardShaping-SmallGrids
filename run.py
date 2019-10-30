import time
from agent import *
from MDP import *
from argparse import ArgumentParser, ArgumentTypeError

if __name__ == "__main__":
    start = time.time()
    usage = """
    USAGE:      python3 run.py <options>
    EXAMPLES:   (1) python run.py
    """

    # Using argparse to select the different setting for the run
    parser = ArgumentParser(usage)

    # N : corresponds to the number of iterations
    parser.add_argument(
        '--nb_iterations',
        help='Number of iterations',
        type=int,
        default=1000)

    # t: Size of the hisotry
    parser.add_argument(
        '--t',
        help='Size of the history one wants to consider',
        type=int,
        default=1000
    )

    # discount_factor : gamma parameter
    parser.add_argument(
        '--discount_factor',
        help='Discount factor (gamma)',
        type=float,
        default=0.99
    )

    # epsilon : e parameter for e-greedy policy
    parser.add_argument(
        '--epsilon',
        help='Epsilon parameter for the e-greedy policy',
        type=float,
        default=0.5
    )

    # learning_ratio : alpha parameter for Q6
    parser.add_argument(
        '--learning_ratio',
        help='Learning ratio used during the Q-learing algorithm',
        type=float,
        default=0.05
    )

    # nb_episodes
    parser.add_argument(
        '--n',
        help='Number of episodes used during the Q-learing algorithm',
        type=int,
        default=100
    )

    # size of the grid
    parser.add_argument(
        '--size',
        help='Size of the grid',
        type=int,
        default=5
    )

    # Parsing the arguments
    args = parser.parse_args()
    nb_iterations = args.nb_iterations
    t = args.t
    size = args.size
    gamma = args.discount_factor
    epsilon = args.epsilon
    alpha = args.learning_ratio
    nb_episodes = args.n

    if nb_iterations <= 0 or t <= 0 or nb_episodes <=0:
        print("The number of iterations, the size of history and "
        "the number of episodes should be +.")
        exit()

    print("Part 1. Using sparse reward.")
    print("Learning ..", end = ' ')
    agent = Agent(gamma, size=size, reward = "sparse")
    mdp = MDP(discount_factor=gamma, learning_ratio=alpha, b_s=1000,size=size, reward = "sparse")
    # Computing Q
    Q = mdp.getQlearning(nb_episodes, t, epsilon)

    # Computing the estimated optimal policy for the Q computed
    opt_policy = mdp.getPolicyFromQ(Q)
    print("done!")

    # Corresponding ^JN
    J = agent.computeJ(opt_policy, nb_iterations, display=False)
    J_0 = J[0][0]
    print("Expected discounted cumultative reward : {}".format(J_0))
    print("Running a episode:")
    agent.followPolicy(opt_policy, N=t, display = False)
    print("Part2. Heuristic")
    print("Learning ..", end = ' ')
    agent = Agent(gamma, size=size, reward = "heuristic")
    mdp = MDP(discount_factor=gamma, learning_ratio=alpha, b_s=1000,size=size, reward = "heuristic")
    # Computing Q
    Q = mdp.getQlearning(nb_episodes, t, epsilon)

    # Computing the estimated optimal policy for the Q computed
    opt_policy = mdp.getPolicyFromQ(Q)
    print("done!")

    # Corresponding ^JN
    J = agent.computeJ(opt_policy, nb_iterations, display=False)
    J_0 = J[0][0]
    print("Expected discounted cumultative reward : {}".format(J_0))
    print("Running a episode:")
    agent.followPolicy(opt_policy, N=t, display = True)





    print("--------- Comp. time : {} ---------".format(time.time() - start))
