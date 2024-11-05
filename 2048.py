import gym_2048
import gym
import copy
import numpy as np
LEFT = 0
UP = 1
RIGHT = 2
DOWN = 3
List_actions=[LEFT,UP,RIGHT,DOWN]
#MIDWAY-> recursive with depth (runtime) and return list of actions 
#After-> UI, Algo that can't see every possible outcome

class gym__2048:
    def __init__(self, env, depth):
        self.env=env
        self.depth=depth
        self.moves=0
    
    def evaluate(self,board,action,depth=0,rewards=0):
      if depth==self.depth:
        return board,action,rewards
      return self.getaction(board,action,depth,rewards)
    
    def getaction(self,board,action,depth,rewards):
      # print('here')
      best_action=None
      best_reward=0
      
      # print('here1')

      for action in List_actions:
          # self.moves+=1

          next_state,reward,done,info=self.move_board(board,action)  
          # print('here')
          if done:
            # print('done')
            return next_state,action,rewards+reward
          print('Next Action: "{}"\n\nReward: {}'.format(
            gym_2048.Base2048Env.ACTION_STRING[action], reward))        
          self.render(next_state)
          board,action,rewards=self.evaluate(next_state,action,depth+1,rewards+reward)
          if reward>=best_reward:
            best_reward=reward
            best_action=action
      
      return board,best_action,best_reward


  
    #from Base2048Env
    def move_board(self,board,action):
      print('here')
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
  curenv=gym__2048(env,2)
  while not done and moves!=1:
    # action = 1
    board,best_action,best_reward=(curenv.evaluate(env.board,None))
    # print(best_action)
    # print(curenv.moves)
    
    # print('act',board,reward)
    moves += 1
    
    # env.render()

  # print('\nTotal Moves: {}'.format(moves))