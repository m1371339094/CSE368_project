import gym_2048
import gym
import copy
import numpy as np

LEFT = 0
UP = 1
RIGHT = 2
DOWN = 3
List_actions=[LEFT,UP,RIGHT,DOWN]
Corners={(0,0),(3,0),(0,3),(3,3)}
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
    #1->4->20...
    
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
      done=self.is_done(board2)
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
      print()
      
#(1/num_of_blocks)(8+8+4+4+2+4+.5+.5)
class better_2048(gym__2048):
    def __init__(self, env, depth):
      super().__init__(env, depth)
    # def board_after_action(self,board,depth):
    #   if depth==self.depth:
    #     return board
    #   points=0
    #   new_board=board
    #   for act in List_actions:
    #     board2=self.move_board_without_random(board,act) 
    #     new_points=self.arrow_algo(board2) 
    #     # print(new_points,points)
        
    #     if new_points>points:
    #       new_board=board2
    #       points=new_points
    #   self.env._place_random_tiles(new_board, count=1)
    #   done=self.is_done(board)
    #   # self.render(new_board)
    #   if done:
    #     return new_board
    #   # print(new_board)
    #   return self.board_after_action(new_board,depth+1)
    def board_after_action_iterate(self,board,depth):
      last_board=board
      new_board=board
      points=0
      while depth !=self.depth:
        for act in List_actions:
          board2=self.move_board_without_random(last_board,act) 
          new_points=self.arrow_algo(board2) 
          if np.array_equal(last_board,board2):
            continue
          if new_points>points:
            new_board=board2
            points=new_points
        self.env._place_random_tiles(new_board, count=1)
        done=self.is_done(new_board)
        # self.render(new_board)
        if done:
          return new_board
        points=0  
        depth+=1
        last_board=new_board
    def get_neighbors(self, board, x, y):
        neighbors = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            # print(nx,y)
            if 0 <= nx < 4 and 0 <= ny < 4:
                neighbors.append(board[ny][nx]) 
        return neighbors
    def old_arrow_algo(self,board):
      tot=0
      num_of_block=0
      biggest=0
      big_pos=(0,0)
      walls=[]
      for dy,y in enumerate(board):
        for dx,x in enumerate(y):
          if x == 0:
            continue
          num_of_block+=1
          biggest=x if x> biggest else biggest
          neighbors=self.get_neighbors(board,dx,dy)
          new_wall=([x]*(4-len(neighbors)))
          if biggest==x:
            # print(big_neighbor)
            big_pos=(dx,dy)
          walls=walls+(new_wall)
          # print(walls)
          # print(len(neighbors),([x]*(4-len(neighbors))))
          for neighbor in neighbors:
            #/0
            if  neighbor>x:
              tot+=x/neighbor*3 #4/1024
      for wall in walls: 
        tot+=(wall/biggest)
      if big_pos in Corners:
        tot+=2
      tot+=biggest
      tot+=100/num_of_block
      return tot
    def arrow_algo(self,board):
        largest_tile, largest_pos,tot_num_of_block = self.find_largest_tile(board)
        score = 0
        score += largest_tile 
        score+=1000/tot_num_of_block
        if largest_pos in Corners: score+=largest_tile*2 
        for i in range(4):
            for j in range(4):
                    layer=self.manhattan_distance(largest_pos, (i, j))
                    tile_value = board[i][j]
                    if tile_value > 0:
                        proximity_factor = 1 - (layer / 4)
                        score += (tile_value) * proximity_factor
        return score


    def find_largest_tile(s,board):
        largest_tile = 0
        largest_pos = (0, 0)
        tot_num_of_block= 0
        for i in range(4):
            for j in range(4):
              if board[i][j]!=0:
                tot_num_of_block+=1
                if board[i][j] > largest_tile:
                    largest_tile = board[i][j]
                    largest_pos = (i, j)
        return largest_tile, largest_pos, tot_num_of_block
        
    def manhattan_distance(s,pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
    
    def move_board_without_random(self,board,action):
      # print('here')
      rotated_obs = np.rot90(board, k=action)
      reward, updated_obs = self.env._slide_left_and_merge(rotated_obs)
      board2 = np.rot90(updated_obs, k=4 - action)
      # self.env._place_random_tiles(board2, count=1)
      # done=self.is_done(board)
      return board2

if __name__ == '__main__':
  env = gym.make('2048-v0')
  # env.seed(18)
  # env.reset()
  # done = False
  # curenv = better_2048(env, 10000)
  # usealgo = curenv.board_after_action_iterate(env.board, 0)
  # print(usealgo)
  def find_biggest_tile_across_seeds(env, seed_range, iterations):
    largest_tiles = []

    for seed in range(seed_range):
        env.seed(seed)
        env.reset()
        done = False
        curenv = better_2048(env, iterations)
        usealgo = curenv.board_after_action_iterate(env.board, 0)
        largest_tile = max(max(row) for row in usealgo)
        largest_tiles.append((largest_tile,seed))
        print(largest_tile,seed)
    
    return max(largest_tiles)

  # Loop seeds and iterations
  seed_range = 100
  iterations = 10000 
  largest_number = find_biggest_tile_across_seeds(env, seed_range, iterations)

  print("Largest number across all seeds:", largest_number)
  