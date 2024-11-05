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
# 4,16,256
class gym__2048:
    def __init__(self, env, depth):
        self.env=env
        self.depth=depth
        self.moves=0
    
    def evaluate(self,board,actions=[],depth=0,rewards=0):
      if depth==self.depth:
        return board,actions,rewards
      return self.getaction(board,actions,depth,rewards)
    
    def getaction(self,board,actions,depth,rewards):
      # print('here')
      best_action=None
      best_reward=0
      best_board=None
      # print('here1')

      for action in List_actions:
          # self.moves+=1
          # print(board)

          next_state,reward,done,info=self.move_board(board,action)  
          # print(action,next_state,reward,rewards)
          # print('here')
          if done:
            # print('done',next_state,action,rewards+reward)
            return next_state,action,rewards+reward
          # print('Next Action: "{}"\n\nReward: {}'.format(
          #   gym_2048.Base2048Env.ACTION_STRING[action], reward))        
          # self.render(next_state)
          
          board2,difact,new_rewards=self.evaluate(next_state,actions+[action],depth+1,rewards+reward)
          if depth==0:
            print(new_rewards,board2,difact)
          
          if new_rewards>=best_reward:
            best_reward=new_rewards
            best_action=difact
            best_board=board2
      
      return best_board,best_action,best_reward


  
    #from Base2048Env
    def move_board(self,board,action):
      # print('here')
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
  env.seed(3)
  env.reset()
  env.render()
  
  done = False
  moves = 0
  curenv=gym__2048(env,3)
  while not done and moves!=1:
    # m=(curenv.move_board(env.board,1))
    # print(m)
    
    # print(curenv.move_board(m[0],0))
    
    # action = 1
    board,best_action,best_reward=(curenv.evaluate(env.board))
    print(board,best_action,best_reward)
    # print(board,best_action,best_reward)
    # print(best_action)
    # print(curenv.moves)
    
    # print('act',board,reward)
    moves += 1
    
    # env.render()

  # print('\nTotal Moves: {}'.format(moves))