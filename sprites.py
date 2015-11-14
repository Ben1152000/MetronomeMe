
from math import sin, cos, pi
from copy import copy
import pygame

from modules.SubtractRects import sub_rect

class Bar():

	def __init__(self, DISPLAYSCREEN, POS, SIZE, color, scolor, tcolor):
		self.screen = DISPLAYSCREEN
		SSIZE = (0, SIZE[1] - 2)
		SPOS = (POS[0] + SIZE[0]/2, POS[1] + 1)
		self.rad = SIZE[0] / 2 - 1
		self.color = color
		self.scolor = scolor
		self.tcolor = tcolor
		self.rect = pygame.Rect(POS, SIZE)
		self.srect = pygame.Rect(SPOS, SSIZE)
		self.dirty_rect = None
		self.normal()
		
	def update(self, time):
		old_rect = copy(self.srect) # create a duplicate version of the srect
		self.srect.width = self.rad * sin(pi * (time % 2))
		new_rect = self.srect
		or_rect = old_rect.union(new_rect)
		and_rect = old_rect.clip(new_rect)
		diff_rects = sub_rect(or_rect, and_rect)
		if len(diff_rects) > 0:
			self.dirty_rect = diff_rects[0] # create dirty rect
		else:
			self.dirty_rect = None
		# BENBENBEN YOU NEED TO MAKE SURE IT RETURNS TWO RECTS PRONTO!!!

	def render(self):
		pygame.draw.rect(self.screen, self.color, self.rect)
		pygame.draw.rect(self.screen, self.drawColor, self.srect)
		return self.dirty_rect

	# change color to pressed-down color
	def highlight(self):
		self.drawColor = self.tcolor

	# change color to normal color
	def normal(self):
		self.drawColor = self.scolor

class Text(object):

	def __init__(self, DISPLAYSCREEN, pos, text, FONT, color=(0,0,0)):
		self.screen = DISPLAYSCREEN
		self.font = FONT
		self.pos = pos
		self.text = text
		self.color = color
		self.surf = self.font.render(self.text, True, self.color)
		self.rect = self.surf.get_rect(center = self.pos)

	def render(self):
		self.screen.blit(self.surf, self.rect)

class Counter():
	
	def __init__(self, DISPLAYSCREEN, pos, start_value, FONT, color):
		self.screen = DISPLAYSCREEN
		self.font = FONT
		self.pos = pos
		self.color = color
		self.score = int(start_value)
		self.text = str(self.score)
		self.surf = self.font.render(self.text, True, self.color)
		self.rect = self.surf.get_rect(center = self.pos)

	def increment(self, num):
		self.score += int(num)
		self.text = str(self.score)
		self.surf = self.font.render(self.text, True, self.color)
		self.rect = self.surf.get_rect(center = self.pos)

	def render(self):
		self.screen.blit(self.surf, self.rect)
		return self.rect # return dirty rect

# work-in-progress
class Button():

	def __init__(self, DISPLAYSCREEN, POS, SIZE, text, normal_color, down_color, highlight_color):
		self.screen = DISPLAYSCREEN
		self.font = FONT
		self.pos = POS
		self.size = SIZE
		self.text = text
		self.n_color = normal_color
		self.d_color = down_color
		#self.h_color = highlight_color
		self.color = self.n_color
		self.rect = pygame.Rect(self.pos, self.size)
		self.surf = 2
		self.state = "up"

	def render():
		pass

	def down():
		self.color = self.d_color
		self.state = "down"

	def up():
		self.color = self.n_color
		self.state = "up"

	def isBeingPressed():
		pass

	def update(event_pos):
		pass
