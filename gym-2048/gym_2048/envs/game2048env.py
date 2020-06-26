import gym
from gym import error, spaces, utils
from gym.utils import seeding

import game.constants as c
from game.rules import game2048 

import ai.parameters as params

class game2048env(gym.Env):
    """
    Create a 2048-gym variant for RL
    """
    #metadata = {'render.modes': ['human']}

    def __init__(self, N_episodes=params.N_episodes):
        """
        Initialize the 2048 game from game/rules.py
        Note, to edit constants, just change game/constants.py
        """
        self.Game = game2048(c.GRID_LENGTH, c.MAX_POWER, c.MAX_GEN)
        
        #RL parameters
        self.episode_length = N_episodes
        self.resets = 0

        #Actions possible
        self.action_space = spaces.Discrete(4)

        # There are GRID_LENGTH**2 tiles. Each tile may have MAX_POWER possible tile types.
        self.observation_space = spaces.MultiDiscrete([c.MAX_POWER] * (c.GRID_LENGTH**2))

        #Reproducibility
        self.seed()

    def seed(self, seed=params.seed):
        """ Initialize random seed """
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def _get_observation(self):
        """
        Get the state of the board.
        """
        return self.Game.board
        
    def step(self, a):
        """ Take an action provided and iterate counter """
        # Make action
        action = params.action_dict[a]
        self.Game.move_tiles(action)

        reward = self.Game.score
        self.current_step += 1
        done = bool((self.current_step > self.episode_length) or self.Game.game_over)
        return self.Game.board, self.Game.score, done

    def reset(self):
        """ Reset the gameboard and retry the game """
        self.current_step = 0
        self.resets += 1
        self.Game.make_gameboard()
        obs = self._get_observation()
        return obs

    #def render(self, mode='human', close=False):
    #    pass