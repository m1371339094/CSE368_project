import gym_2048
import gym
import copy
import numpy as np
LEFT = 0
UP = 1
RIGHT = 2
DOWN = 3
actions=[LEFT,UP,RIGHT,DOWN]
class gym__2048:
    def __init__(self, env, depth):
        self.env=env
        self.depth=depth
    def evaluate(self,board,depth):
       for action in actions:
          next_state,reward,done,info=self.move_board(board,action)  
          print('Next Action: "{}"\n\nReward: {}'.format(
            gym_2048.Base2048Env.ACTION_STRING[action], reward))        
          self.render(next_state)

    def nextaction(self):
        None
  
    #from Base2048Env
    def move_board(self,board,action):
      rotated_obs = np.rot90(board, k=action)
      reward, updated_obs = self.env._slide_left_and_merge(rotated_obs)
      board2 = np.rot90(updated_obs, k=4 - action)
      self.env._place_random_tiles(board2, count=1)
      done=self.is_done(board)
      return board2,reward,done,{}
    #from Base2048Env
    def is_done(self,board):
      copy_board = board.copy()
      if not copy_board.all():
        return False
      for action in [0, 1, 2, 3]:
        rotated_obs = np.rot90(copy_board, k=action)
        _, updated_obs = self.env._slide_left_and_merge(rotated_obs)
        if not updated_obs.all():
          return False
      return True
    #from Base2048Env
    def render(self, board, mode='human'):
      if mode == 'human':
        for row in board.tolist():
          print(' \t'.join(map(str, row)))



if __name__ == '__main__':
  env = gym.make('2048-v0')
  env.seed(42)
  env.reset()
  env.render()
  
  done = False
  moves = 0
  curenv=gym__2048(env,5)
  while not done and moves!=1:
    # action = 1
    curenv.evaluate(env.board,5)
    # print('act',board,reward)
    moves += 1
    
    # env.render()

  # print('\nTotal Moves: {}'.format(moves))