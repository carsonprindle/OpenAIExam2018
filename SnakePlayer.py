from ple.games.snake import Snake
from ple import PLE
import gym
import numpy as np

class HardCodedPlayer():

	def __init__(self, actions):
		self.actions = actions
		print(actions)
		print(game.getGameState())
			#'snake_head_x','snake_head_y','food_x','food_y','snake_body','snake_body_pos'

	def pickAction(self, reward, obs):
		if(game.getGameState()["snake_head_x"] > game.getGameState()["food_x"]): #move left
			return 97   
		elif(game.getGameState()["snake_head_x"] < game.getGameState()["food_x"]): #move right
			return 100  
		elif(game.getGameState()["snake_head_y"] < game.getGameState()["food_y"]): #move down
			return 115  
		elif(game.getGameState()["snake_head_y"] > game.getGameState()["food_y"]): #move up
			return 119  
		return "none"
		#119 up
		#97  left
		#100 right
		#115 down

class RandomPlayer():

	### RANDOM ACTION PLAYER ###    
    def __init__(self, actions):
        self.actions = actions

    def pickAction(self, reward, obs):
        return self.actions[np.random.randint(0, len(self.actions))]

game = Snake(
	width = 750,
	height = 750,
	init_length = 5
)

fps = 30  # fps we want to run at
frame_skip = 2
num_steps = 1
force_fps = False  # True == MegaSpeed
display_screen = True

reward = 0.0
max_noops = 20
nb_frames = 15000

# make a PLE instance.
p = PLE(game, fps=fps, frame_skip=frame_skip, num_steps=num_steps,
        force_fps=force_fps, display_screen=display_screen)

### SET PLAYER ###
agent = HardCodedPlayer(p.getActionSet()) #RandomPlayer, HardCodedPlayer, SnakePlayer

p.init()

for i in range(nb_frames):
    if p.game_over():
        p.reset_game()

    obs = p.getScreenRGB()
    action = agent.pickAction(reward, obs)
    reward = p.act(action)

    if i % 120 == 0:
        p.saveScreen("screen_capture.png")