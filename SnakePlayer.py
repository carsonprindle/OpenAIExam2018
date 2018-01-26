from ple.games.snake import Snake
from ple import PLE
import gym
import numpy as np

act_values = {}

class HardCodedPlayer():

	def __init__(self, actions):
		self.actions = actions
		print(actions)
		print(game.getGameState())
			#'snake_head_x','snake_head_y','food_x','food_y','snake_body','snake_body_pos'

	def pickAction(self, reward, obs):
		if(game.getGameState()["snake_head_y"] < game.getGameState()["food_y"]): #move down
			return 115  
		elif(game.getGameState()["snake_head_y"] > game.getGameState()["food_y"]): #move up
			return 119  
		elif(game.getGameState()["snake_head_x"] > game.getGameState()["food_x"]): #move left
			return 97   
		elif(game.getGameState()["snake_head_x"] < game.getGameState()["food_x"]): #move right
			return 100  
		
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

score_scaling = 0.01

def sigmoid(x):
    output = 1/(1+np.exp(-x))
    return output

class LearningPlayer():

	def __init__(self, actions):
		self.dist = (200,200)
		self.actions = actions
		self.act_values = {}
		for act in actions:
			act_values[act] = 1.0
		print(act_values)
		self.act = actions[0]
	
	def interpretDist(self):
		distx = game.getGameState()["food_x"]-game.getGameState()["snake_head_x"]
		disty = game.getGameState()["food_y"]-game.getGameState()["snake_head_y"]
		return(distx,disty)

	def hyp(self,t):
		self.straightDist = np.sqrt(np.square(t[0]) + np.square(t[1]))
		return self.straightDist

	def modVals(self):
		self.lastAct = self.act
		if self.hyp(self.interpretDist()) < self.hyp(self.dist):
			act_values[self.lastAct]+=score_scaling
			#print("Last action: %a, Rating: %r"(self.lastAct,self.act_values[self.lastAct]))
		else:
			act_values[self.lastAct]-=score_scaling
		self.dist = self.interpretDist()

	def pickAction(self, reward, obs):
		self.act = max(act_values, key=act_values.get)
		self.modVals()
		return self.act #highest value action		

game = Snake(
	width = 200,
	height = 200,
	init_length = 3
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
agent = LearningPlayer(p.getActionSet()) #RandomPlayer, HardCodedPlayer, LearningPlayer

p.init()

for i in range(nb_frames):
	if p.game_over():
		p.reset_game()

	obs = p.getScreenRGB()
	action = agent.pickAction(reward, obs)
	reward = p.act(action) #gain in score since last frames

	if i % 120 == 0:
		p.saveScreen("screen_capture.png")