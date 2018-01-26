from ple.games.snake import Snake
from ple import PLE
import gym
import numpy as np

act_values = {}
size = 20

class RandomPlayer():

	### RANDOM ACTION PLAYER ###    
	def __init__(self, actions):
		self.totalscore = 0
		self.runs = 0

		self.actions = actions
		self.steps = 0
		self.scores = []
		self.runscore = 0

	def over(self):
		self.steps+=1
		self.runscore-= 1/self.steps
		#print("Steps to death: {}, Run Score: {}".format(self.steps,self.runscore))
		self.scores.append(self.runscore)
		self.runs+=1
		self.runscore=0
		self.steps=0

	def testenv(self, reward):
		self.steps+=1
		if reward>0:
			#print("Steps to score: {}".format(self.steps))
			self.runscore+=reward/self.steps
			self.steps = 0
			self.totalscore+=1			

	def pickAction(self, reward, obs):
		self.testenv(reward)
		return self.actions[np.random.randint(0, len(self.actions))]

score_scaling = 0.01

def sigmoid(x):
    output = 1/(1+np.exp(-x))
    return output

class LearningPlayer():

	def __init__(self, actions):
		self.i = 0
		self.plus  = 1
		self.minus = 1
		self.pathr = 0.1

		self.totalscore = 0
		self.runs = 0

		self.steps = 0
		self.path = []
		self.runscore = 0
		self.Q={}
		self.actions = actions
		for sx in range(size):
			for sy in range(size):
				for fx in range(size):
					for fy in range(size):
						self.Q[sx,sy,fx,fy] = {}
						for act in actions:
							self.Q[sx,sy,fx,fy][act] = 1.0
		print("1111 action vals: " + str(self.Q[1,1,1,1]))
		self.act = actions[0]

	def modVals(self):
		self.lastAct = self.act
		if self.hyp(self.interpretDist()) < self.hyp(self.dist):
			act_values[self.lastAct]+=score_scaling
			#print("Last action: %a, Rating: %r"(self.lastAct,self.act_values[self.lastAct]))
		else:
			act_values[self.lastAct]-=score_scaling
		self.dist = self.interpretDist()

	def rememberStep(self, act):
		self.path.append((self.findState(),act))
		#print(self.path)

	def over(self):
		self.steps+=1
		self.runscore-= self.minus/self.steps
		#print("Steps to death: {}, Run Score: {}".format(self.steps,self.runscore))
		#print(self.path)
		self.i = 0
		self.savepath()
			#print("Path Adjustment: " + str(self.Q[p[0][0],p[0][1],p[0][2],p[0][3]]))
			#print(p[0])
		self.runs+=1
		self.runscore=0
		self.steps=0

	def savepath(self):
		for p in self.path:
			self.i+=1
			self.Q[p[0][0],p[0][1],p[0][2],p[0][3]][p[1]]+=self.runscore*(1/self.i)
		path = []

	def testenv(self, reward):
		self.steps+=1
		if reward>0:
			#print("Steps to score: {}".format(self.steps))
			self.totalscore+=1
			self.runscore+=self.plus/self.steps
			self.steps = 0
			self.savepath()


	def findState(self):
		return [int(game.getGameState()["snake_head_x"]),int(game.getGameState()["snake_head_y"]),int(game.getGameState()["food_x"]),int(game.getGameState()["food_x"])]

	def findQ(self, fs):
		return self.Q[fs[0],fs[1],fs[2],fs[3]]

	def pickAction(self, reward, obs):
		self.testenv(reward)
		#print(str(self.findState()))
		self.slightRandDic = {}
		for i in self.findQ(self.findState()):
			self.slightRandDic[i] = self.findQ(self.findState())[i]+self.pathr*np.random.randint(-10,10)*self.steps
		#print(self.slightRandDic)
		self.act = max(self.slightRandDic, key=self.slightRandDic.get)
		self.rememberStep(self.act)
		return self.act #highest value action		

game = Snake(
	width = size,
	height = size,
	init_length = 3
)

fps = 30  # fps we want to run at
frame_skip = 2
num_steps = 1
force_fps = True # True == MegaSpeed
display_screen = True

reward = 0.0
max_noops = 20
nb_frames = 1500000

# make a PLE instance.
p = PLE(game, fps=fps, frame_skip=frame_skip, num_steps=num_steps,
		force_fps=force_fps, display_screen=display_screen)

### SET PLAYER ###
agent = LearningPlayer(p.getActionSet()) #RandomPlayer, HardCodedPlayer, LearningPlayer

p.init()

for i in range(nb_frames):
	if p.game_over():
		p.reset_game()
		agent.over()

	obs = p.getScreenRGB()
	action = agent.pickAction(reward, obs)
	reward = p.act(action) #gain in score since last frames
	#print(i)
	if ((i+1) % 5000) == 0:
		print(i+1)
		print("Average score: " + str(agent.totalscore/agent.runs))

	if ((i+1) % 100000) == 0:
		print("Slow")
		print("Average score: " + str(agent.totalscore/agent.runs))
		p.force_fps=False
		