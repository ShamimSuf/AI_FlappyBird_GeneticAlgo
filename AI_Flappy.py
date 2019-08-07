#This flappy will have 6 inputs (i1 to i6) : up, down, bird top-right to up-block-low-right, bird top-left to up-block-low-left, so on.  

import numpy as np
import pygame
import time
import random
from random import randint

pygame.init()

#6 input nodes
i_ROW = 1
i_COL = 6

#3 hidden layer nodes
#input to hidden layer nodes		
w1_ROW = 6
w1_COL = 3

#hiddenb layer to op layer nodes
w2_ROW = 3
w2_COL = 1

class Colors:
	def __init__(self): 
		#https://www.webucator.com/blog/2015/03/python-color-constants-module/
		self.black = (0,0,0)
		self.white = (255,255,255)
		self.cornflowerblue = (100,149,237)
		self.azure4 = (131,139,139)
		self.cadetblue1	= (152,245,255)

class GameWindow:
	def __init__(self):
		colors = Colors()
		
		self.surfaceWidth  = 800
		self.surfaceHeight = 400	
		self.surface = pygame.display.set_mode((self.surfaceWidth, self.surfaceHeight))
		self.clock = pygame.time.Clock()
		self.surface.fill(colors.azure4)
		pygame.display.set_caption('Flappy Bork')

class Point:
	def __init__(self, x, y):
		self.x = x
		self.y = y
	
class Block:
	def __init__(self, gameWindow, x, y_gap, gapHeight):
		
		self.gameWindow	= gameWindow
		self.x 			= x
		self.y_gap		= y_gap
		self.gapHeight	= gapHeight
				
		self.blockWidth = 50
		self.blockSpeed = 5
		
	def draw(self):
		colors = Colors()
		pygame.draw.rect( self.gameWindow.surface, colors.white, (self.x, 0, self.blockWidth, self.y_gap))
		pygame.draw.rect( self.gameWindow.surface, colors.white, (self.x, self.y_gap + self.gapHeight, self.blockWidth, self.gameWindow.surfaceHeight - self.y_gap - self.gapHeight))

	def reset(self):
		#Reset block
		self.x = gameWindow.surfaceWidth - self.blockWidth
		self.y_gap = random_obj.randint(0, gameWindow.surfaceHeight - 150)
	
#Global Variables (Shitty way of implementing! )	
random_obj = random.SystemRandom()	
mutation_rate = 0.3 #between 0,1
generation = 0
gameWindow = GameWindow()
block  = Block (gameWindow, gameWindow.surfaceWidth - 50, randint(0, gameWindow.surfaceHeight - 150), 150)
block.draw()				

#Game Over
def gg_wp():
	user_input = False
	while not user_input:
		for event in pygame.event.get():

			if event.type==pygame.KEYDOWN:
				user_input = True

				#restart game via SPACE key
				if event.key == pygame.K_SPACE:
					main()

			else:
				pygame.quit()
				quit()
				
				
def getRandMatrix(row, col):
	matrix = np.random.rand(row, col)
	for i in range(matrix.shape[0]):
		for j in range(matrix.shape[1]):
			matrix[i][j] = np.random.uniform(-1, 1)
	return matrix

# ReLU activation Function
def ReLU(z):
	z[z < 0] = 0
	return z

# Softmax or averaging the value
def softmax(z):
	summation = np.sum(z)
	if summation == 0.0:
		summation = 1.0
	for i in range(len(z)):
		z[i] = z[i]/summation
	return z

# Sigmoid Activation Function
def sigmoid(z):
	return 1.0/(1.0 + np.exp(-z))

class Brain:	
	def __init__(self):		
		self.w1_matrix = getRandMatrix(w1_ROW, w1_COL)
		self.w2_matrix = getRandMatrix(w2_ROW, w2_COL)
		
	def feedforward(self, i_matrix):
		op1_matrix = np.dot(i_matrix, 	self.w1_matrix)
		op2_matrix = np.dot(op1_matrix, self.w2_matrix)
		op_final   = sigmoid(op2_matrix)	
		if( op_final > 0.5):
			return 1
		else:
			return 0

class Bird:
	def __init__(self, point):
		self.brain = Brain()
		self.life = True
		self.score = 0
		self.fitness = 0
				
		self.point = point
		self.size = 50
		self.fall_speed = 8
			
		#Increment score everytime bird is alive (increment per frame the bird is alive)
		self.incr_score = 1;
		
		#Input coords
		self.p1 = Point(0, 0)
		self.p2 = Point(0, 0)
		self.p3 = Point(0, 0)
		self.p4 = Point(0, 0)
		self.p5 = Point(0, 0)
		self.p6 = Point(0, 0)
		self.p7 = Point(0, 0)
		
	def draw(self):
		colors = Colors()
		pygame.draw.rect( gameWindow.surface, colors.cadetblue1, (self.point.x, self.point.y, self.size, self.size))
		
		#get block
		current_block = block
		
		#draw the lines
		colors = Colors()
		current_block = block
		midpoint = Point(self.point.x + self.size/2, self.point.y + self.size/2)
		i1 = midpoint.y - self.size/2
		i2 = midpoint.y + self.size/2
		
		block_up_low_right	 = Point(current_block.x + current_block.blockWidth	, current_block.y_gap) 
		block_up_low_left	 = Point(current_block.x							, current_block.y_gap)
		block_lower_up_left	 = Point(current_block.x							, current_block.y_gap + current_block.gapHeight)
		block_lower_up_right = Point(current_block.x + current_block.blockWidth	,current_block.y_gap + current_block.gapHeight)
		
		p1 = Point( midpoint.x, i1 )
		p2 = Point( midpoint.x, i2)
		p3 = Point( midpoint.x + self.size/2,  midpoint.y - self.size/2)
		p4 = Point( midpoint.x - self.size/2,  midpoint.y - self.size/2)
		p5 = Point( midpoint.x - self.size/2,  midpoint.y + self.size/2)
		p6 = Point( midpoint.x + self.size/2,  midpoint.y + self.size/2)
		
		pygame.draw.line(gameWindow.surface, colors.cadetblue1, (p1.x, p1.y), (p1.x, 0))
		pygame.draw.line(gameWindow.surface, colors.cadetblue1, (p2.x, p2.y), (p2.x, gameWindow.surfaceHeight))
		pygame.draw.line(gameWindow.surface, colors.cadetblue1, (p3.x, p3.y), (current_block.x + current_block.blockWidth	, current_block.y_gap))
		pygame.draw.line(gameWindow.surface, colors.cadetblue1, (p4.x, p4.y), (current_block.x								, current_block.y_gap))
		pygame.draw.line(gameWindow.surface, colors.cadetblue1, (p5.x, p5.y), (current_block.x								, current_block.y_gap + current_block.gapHeight))
		pygame.draw.line(gameWindow.surface, colors.cadetblue1, (p6.x, p6.y), (current_block.x + current_block.blockWidth	,current_block.y_gap + current_block.gapHeight))
						
	def move(self):		
		#self.point.y += self.fall_speed		
		self.score = self.score + 1
		self.think()

		#self boundary restrict wrt Game Window 
		if ( self.point.x <= 0):
			self.point.x = 0
		if ( self.point.x >= gameWindow.surfaceWidth - self.size):
			self.point.x = gameWindow.surfaceWidth - self.size			
		if ( self.point.y <= 0):
			self.point.y = 0
		if ( self.point.y >= gameWindow.surfaceHeight - self.size):
			self.point.y = gameWindow.surfaceHeight - self.size
		
		#get_block
		current_block = block
				
		#check collision
		#Check if self has collided with block
		if( (current_block.x < (self.point.x + self.size) < (current_block.x + current_block.blockWidth)) or
			(current_block.x < (self.point.x) 			  < (current_block.x + current_block.blockWidth))):
			if(not( (current_block.y_gap < self.point.y < current_block.y_gap + current_block.gapHeight) and 
					(current_block.y_gap < (self.point.y + self.size) < current_block.y_gap + current_block.gapHeight))):
				self.fitness = self.score
				self.life = False
				self.score = 0.0 
		
		#check collision with up and low
		if (self.point.y == 0) or (self.point.y + 50 == gameWindow.surfaceHeight):
			self.fitness = self.score
			self.life = False
			self.score = 0.0 
		
	def think(self):
		i_matrix = self.get_input_matrix()
		doFlap = self.brain.feedforward(i_matrix)
		
		if doFlap == 1:
			self.fall_speed = 8
		else:
			self.fall_speed = -3
			
		#Update player movement value
		self.point.y += self.fall_speed
				
	def reset(self):
		self.point = Point( 50, gameWindow.surfaceHeight/2)
		self.life  = True

	def get_input_matrix(self):
		current_block = block
		
		#TO_DO calculate i_matrix
		midpoint = Point(self.point.x + self.size/2, self.point.y + self.size/2)
				
		#i1 = (current_block.x + current_block.blockWidth) - midpoint.x
		#i2 = current_block.x - midpoint.x
		
		#distance of player from up and down
		i1 = midpoint.y - self.size/2
		i2 = gameWindow.surfaceHeight - (midpoint.y + self.size/2)
		
		block_up_low_right	 = Point(current_block.x + current_block.blockWidth	, current_block.y_gap) 
		block_up_low_left	 = Point(current_block.x							, current_block.y_gap)
		block_lower_up_left	 = Point(current_block.x							, current_block.y_gap + current_block.gapHeight)
		block_lower_up_right = Point(current_block.x + current_block.blockWidth	,current_block.y_gap + current_block.gapHeight)
		
		p1 = Point( midpoint.x, i1 )
		p2 = Point( midpoint.x, i2)
		p3 = Point( midpoint.x + self.size/2,  midpoint.y - self.size/2)
		p4 = Point( midpoint.x - self.size/2,  midpoint.y - self.size/2)
		p5 = Point( midpoint.x - self.size/2,  midpoint.y + self.size/2)
		p6 = Point( midpoint.x + self.size/2,  midpoint.y + self.size/2)

		i3 = np.sqrt(np.square(p3.x - block_up_low_right.x)   + np.square(p3.y - block_up_low_right.y))
		i4 = np.sqrt(np.square(p4.x - block_up_low_left.x)    + np.square(p4.y - block_up_low_left.y))
		i5 = np.sqrt(np.square(p5.x - block_lower_up_left.x)  + np.square(p5.y - block_lower_up_left.y))
		i6 = np.sqrt(np.square(p6.x - block_lower_up_right.x) + np.square(p6.y - block_lower_up_right.y))
		
		self.p1 = p1
		self.p2 = p2
		self.p3 = p3
		self.p4 = p4
		self.p5 = p5
		self.p6 = p6		
		
		'''
		upblock_lower_left  = Point(current_block.x								,current_block.y_gap)
		upblock_lower_right = Point(current_block.x + current_block.blockWidth	,current_block.y_gap)
		lowblock_up_right	= Point(current_block.x + current_block.blockWidth	,current_block.y_gap + current_block.gapHeight)
		lowblock_up_left	= Point(current_block.x								,current_block.y_gap + current_block.gapHeight)
		
		i3 = np.sqrt(np.square(midpoint.x - upblock_lower_left.x) 	+ np.square(midpoint.y - upblock_lower_left.y))
		i4 = np.sqrt(np.square(midpoint.x - upblock_lower_right.x) 	+ np.square(midpoint.y - upblock_lower_right.y))
		i5 = np.sqrt(np.square(midpoint.x - lowblock_up_right.x) 	+ np.square(midpoint.y - lowblock_up_right.y))
		i6 = np.sqrt(np.square(midpoint.x - lowblock_up_left.x) 	+ np.square(midpoint.y - lowblock_up_left.y))
		'''
		
		return np.array([i1, i2, i3, i4, i5, i6])

class Population:
	def __init__(self):
		self.population = []
		self.eliminated = []	
	
	def createPopulation(self):
		for i in range(12):
			bird = Bird(Point( 50, gameWindow.surfaceHeight/2))
			self.population.append(bird)
			
	def move(self):
		for bird in self.population:
			bird.move()

		popCopy = self.population[:]
		for bird in popCopy:
			if not bird.life:
				self.eliminated.append(bird)
				self.population.remove(bird)

		if self.population == []:
			self.evolve()
	
	#aka def reproduce(self)
	def evolve(self):
		global generation		
		generation = generation + 1
		
		#reset block since all birds are dead
		#evolve is called when entire population is dead
		block.reset()
			
		#Draw block
		#block.draw()
		
		self.crossbreed() #takes top and creates babies
		self.mutate()

	def crossbreed(self):
		self.eliminated.sort(key=lambda x: x.fitness, reverse=True)
		
		#assuming 12 birds in population
		baby1, baby2 = self.getBabies(self.eliminated[0], self.eliminated[1]) 
		baby3, baby4 = self.getBabies(self.eliminated[2], self.eliminated[3])
		baby5, baby6 = self.getBabies(self.eliminated[4], self.eliminated[5])
		
		for i in range(6):
			self.population.append(self.eliminated[i])
		
		self.population.append(baby1)
		self.population.append(baby2)
		self.population.append(baby3)
		self.population.append(baby4)
		self.population.append(baby5)
		self.population.append(baby6)
		
		#clear self.eliminated list
		self.eliminated = []

	def getBabies(self, parent_bird1, parent_bird2):
		baby1 = Bird (Point( 50, gameWindow.surfaceHeight/2))
		baby2 = Bird (Point( 50, gameWindow.surfaceHeight/2))
		
		#w1 matrix
		for i in range(baby1.brain.w1_matrix.shape[0]):
			for j in range(baby1.brain.w1_matrix.shape[1]):
				baby1.brain.w1_matrix[i][j] = random.choice([parent_bird1.brain.w1_matrix[i][j], parent_bird2.brain.w1_matrix[i][j]])		
				baby2.brain.w1_matrix[i][j] = random.choice([parent_bird1.brain.w1_matrix[i][j], parent_bird2.brain.w1_matrix[i][j]])

		#w2 matrix
		for i in range(baby1.brain.w2_matrix.shape[0]):
			for j in range(baby1.brain.w2_matrix.shape[1]):
				baby1.brain.w2_matrix[i][j] = random.choice([parent_bird1.brain.w2_matrix[i][j], parent_bird2.brain.w2_matrix[i][j]])
				baby2.brain.w2_matrix[i][j] = random.choice([parent_bird1.brain.w2_matrix[i][j], parent_bird2.brain.w2_matrix[i][j]])				
		
		return baby1, baby2
		
	def mutate(self):		
		#Mutate single bird, 6/18 from W1 and 1/3 from W2		
		random_bird_index = random_obj.randint(0, len(self.population)-1)
				
		for x in range(6):
			random_row = random_obj.randint(0,5)
			random_col = random_obj.randint(0,2)
			self.population[random_bird_index].brain.w1_matrix[random_row][random_col] = np.random.uniform(-1, 1)

		for x in range(1):
			random_row_w2 = random_obj.randint(0,2)
			self.population[random_bird_index].brain.w2_matrix[random_row_w2][0] = np.random.uniform(-1, 1)
		
	def draw(self):
		for bird in self.population:
			bird.draw()
		
def gameLoop():
	loop = True
	population = Population()
	population.createPopulation()
	speed = 60
	colors = Colors()
	
	global generation
	
	while loop:	

		#display info
		text = "Generation: " + str(generation)
		#population.population.sort(key=lambda x: x.score, reverse=True)
		#top_bird = population.population[0]
		#text = text + " Top Score: " + str(top_bird.score) + " Top Fitness: " + str(top_bird.fitness)
		print(text)
		
		for event in pygame.event.get():			
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					gg_wp()
				if event.key == pygame.K_1:
					speed = 60*1
				if event.key == pygame.K_2:
					speed = 60*2
				if event.key == pygame.K_3:
					speed = 60*3
				if event.key == pygame.K_4:
					speed = 60*4
				if event.key == pygame.K_5:
					speed = 60*5
				if event.key == pygame.K_6:
					speed = 60*6
				if event.key == pygame.K_7:
					speed = 60*7
				if event.key == pygame.K_8:
					speed = 60*8
				if event.key == pygame.K_9:
					speed = 60*9		

		#Reset block
		if( block.x <= -block.blockWidth ):
			block.reset()
				
		#Fill Game Window
		gameWindow.surface.fill(colors.azure4)
		
		#Block move		
		block.x 	= block.x  - block.blockSpeed 		
		
		#draw block
		block.draw()	
		
		population.move()        
		population.draw()
		
		pygame.display.update()
		gameWindow.clock.tick(speed)
gameLoop()
