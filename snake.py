import pygame
import numpy as np
import random
from dataclasses import dataclass

# variables
tile_width = 20
tile_height = 20
number_tile_x = 20
number_tile_y = 10
adjust_time = 5
dead = False
disable_death = False
game_win = False

screen_width = number_tile_x * tile_width
screen_height = number_tile_y * tile_height
max_width = screen_width - tile_width
max_height = screen_height - tile_height

@dataclass
class Game:
	pygame.init()
	pygame.display.set_caption("Snake")
	screen = pygame.display.set_mode((screen_width,screen_height))
	clock = pygame.time.Clock()

class Snake:
	def __init__(self):
		max_body = number_tile_x * number_tile_y *10 # when all the board is full
		self.body = np.full((2, max_body), -(tile_width+tile_height), dtype=int)
		# -(tile_width+tile_height) is for when you choose more_tail != 1
		self.point_body = 1 # pointer to the next cell
		self.body[0,0] = tile_width * 2 # starting position
		self.body[1,0] = tile_height * 2
		self.pos_last = np.zeros(2)
		self.col = "green"
		self.move = 'r' # starts going right
		self.more_tail = 10
s = Snake()

def rnd():
	global game_win
	[x,y] = [-1,-1]
	set_pos = np.array(range(0,number_tile_x*number_tile_y))
	for i in range(s.point_body):
		# remove cells occupied by snake
		pos_snake = s.body[0,i]/tile_width + s.body[1,i]/tile_height*number_tile_x
		set_pos = set_pos[set_pos != pos_snake]
	if set_pos.size == 0:
		game_win = True
	else:
		pos = random.choice(set_pos)
		for i in range(number_tile_x):
			for j in range(number_tile_y):
				if i + j*number_tile_x == pos:
					[x,y] = [i*tile_width,j*tile_height]
					break
	return [x,y]

class Fruit:
	def __init__(self):
		[self.x,self.y] = rnd() # init fruit
		self.col = "red"
f = Fruit()

def check_arrowkey_press():
	pressed = pygame.key.get_pressed()
	if pressed[pygame.K_UP]:
		if s.move != 'd':	s.move = 'u' # doesn't move opposite of current movement
	if pressed[pygame.K_DOWN]:
		if s.move != 'u':	s.move = 'd'
	if pressed[pygame.K_LEFT]:
		if s.move != 'r':	s.move = 'l'
	if pressed[pygame.K_RIGHT]:
		if s.move != 'l':	s.move = 'r'

def move_snake(dead):
	[x,y] = [s.body[0,0],s.body[1,0]] # head
	if dead == False or disable_death == True:
		if s.move == 'u':
			if y > 0:			y -= tile_height # stops at borders
			else: dead = True
		elif s.move == 'd':
			if y < max_height:	y += tile_height
			else: dead = True
		elif s.move == 'l':
			if x > 0:			x -= tile_width
			else: dead = True
		elif s.move == 'r':
			if x < max_width:	x += tile_width
			else: dead = True
	[s.body[0,0],s.body[1,0]] = [x,y]
	return dead

def check_eat_self(dead):
	[x,y] = [s.body[0,0],s.body[1,0]] # head
	for i in range(1, s.point_body):
		if x == s.body[0,i] and y == s.body[1,i]:
			dead = True
	return dead

def check_eat_fruit():
	[x,y] = [s.body[0,0],s.body[1,0]] # head
	if x == f.x and y == f.y:
		[f.x,f.y] = rnd()
		s.body[0, s.point_body] = s.body[0, s.point_body-1]
		s.body[1, s.point_body] = s.body[1, s.point_body-1]
		s.point_body += s.more_tail
		s.pos_last[0] = s.body[0, s.point_body] # save
		s.pos_last[1] = s.body[1, s.point_body]

def draw():
	if dead == True and disable_death == False:
		s.col = "blue"
		# last piece of tail
		pygame.draw.rect(Game.screen, s.col, pygame.Rect(s.pos_last[0], s.pos_last[1], tile_width, tile_height))
	# fruit
	pygame.draw.rect(Game.screen, f.col, pygame.Rect(f.x, f.y, tile_width, tile_height))
	# snake
	for i in range(s.point_body):
		pygame.draw.rect(Game.screen, s.col, pygame.Rect(s.body[0,i], s.body[1,i], tile_width, tile_height))

def update_body():
	if dead == False or disable_death == True:
		s.pos_last[0] = s.body[0, s.point_body-1]
		s.pos_last[1] = s.body[1, s.point_body-1]
		for i in range(s.point_body-1, 0, -1): # start, stop, step
			s.body[0,i] = s.body[0,i-1]
			s.body[1,i] = s.body[1,i-1]

if __name__ == "__main__":
	loop = True
	mux = True
	go = True
	while loop:
		for event in pygame.event.get():
			if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
				loop = False

		if go:
			Game.screen.fill((0, 0, 0)) # refresh
			check_arrowkey_press()
			
			dead = move_snake(dead) # updates dead
			dead = check_eat_self(dead)
			check_eat_fruit()
			draw() # snake + fruit
			update_body()
			
			pygame.display.flip()
			Game.clock.tick(adjust_time)
			if game_win == True:
				dead = True
				print("You won!")
				game_win = False
		
		# pause
		enter_press = pygame.key.get_pressed()[pygame.K_p]
		if mux and enter_press:
			mux = False
			if go:	go = False
			else:	go = True
		elif not enter_press:
			mux = True
		
		# game reset
		if dead == True and pygame.key.get_pressed()[pygame.K_SPACE]:
			s = Snake() # snake reset
			[f.x,f.y] = rnd()
			dead = False

pygame.quit()