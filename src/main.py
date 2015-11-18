
from time import clock
import pygame, random, sys, decimal
from pygame.locals import *
import os

from sprites import *

FPS = 50 # max frames per second, the general speed of the program
WINDOWWIDTH = 640 # size of window's width in pixels
WINDOWHEIGHT = 480 # size of windows' height in pixels

# Set up colors

#              R    G    B
GRAY	   = (100, 100, 100)
NAVYBLUE   = ( 60,  60, 100)
WHITE	   = (255, 255, 255)
RED        = (255,   0,   0)
GREEN	   = (  0, 255,   0)
BLUE	   = (  0,   0, 255)
YELLOW	   = (255, 255,   0)
ORANGE	   = (255, 128,   0)
PURPLE	   = (255,   0, 255)
CYAN	   = (  0, 255, 255)
BLACK      = (  0,   0,   0)
BOTTICELLI = (212, 226, 238)

BGCOLOR = BOTTICELLI

def main():

	# timer stuff
	global FPSCLOCK, DISPLAYSCREEN
	pygame.init()
	pygame.mixer.init()
	startSound = pygame.mixer.Sound("sounds/Ding.wav")
	startSound.play()
	print("I'm as frisky as a squid on Tuesday!")
	FPSCLOCK = pygame.time.Clock()
	DISPLAYSCREEN = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
	DISPLAYSCREEN.set_alpha(None) # Improves the framerate by a lot - DO NOT DELETE

	# screen setup
	pygame.display.set_caption('Metronome Me')
	DISPLAYSCREEN.fill(BGCOLOR)

	# set up fonts
	global BASICFONT
	global TITLEFONT
	global SMALLFONT
	global MONOFONT
	BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
	TITLEFONT = pygame.font.Font('freesansbold.ttf', 70)
	SMALLFONT = pygame.font.Font('freesansbold.ttf', 14)
	MONOFONT = pygame.font.SysFont('monospacebold', 22)

	# game loop
	showStartScreen()
	#showInstructionScreen()
	while True:
		score = showGameScreen()
		showEndingScreen(score)
	

def showStartScreen():

	DISPLAYSCREEN.fill(BGCOLOR)

	# initiate text
	title1 = Text(DISPLAYSCREEN, (WINDOWWIDTH * 2 / 5, WINDOWHEIGHT / 2), "Metronome", TITLEFONT, RED)
	title2 = Text(DISPLAYSCREEN, (WINDOWWIDTH * 4 / 5, WINDOWHEIGHT / 2), "Me", TITLEFONT, ORANGE)
	message = Text(DISPLAYSCREEN, (WINDOWWIDTH / 2, WINDOWHEIGHT - 40), "Press any key to play.", BASICFONT, BLACK)
	author = Text(DISPLAYSCREEN, (WINDOWWIDTH / 2, WINDOWHEIGHT / 2 + 50), "By Ben1152000", BASICFONT, BLACK)
	helpMessage = Text(DISPLAYSCREEN, (WINDOWWIDTH / 2, WINDOWHEIGHT - 20), "At any time, press tab for help", SMALLFONT, BLACK)
	
	global timeCounter
	timeCounter = Counter(DISPLAYSCREEN, (35, 15), '{0:.2f}'.format(pygame.time.get_ticks() / 1000.), MONOFONT, ORANGE) ### MONOFONT

	# draw messages
	title1.render()
	title2.render()
	message.render()
	author.render()
	helpMessage.render()
	pygame.display.update()

	loop = 0
	while True: # start screen main loop

		for event in pygame.event.get(): # event handling loop
			#print(event) ###
			if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
				terminate()
			elif event.type == pygame.KEYDOWN:
				pygame.event.get() # clear event queue
				return

		# update sprites
		timeCounter.set('{0:.2f}'.format(pygame.time.get_ticks() / 1000.))
		
		# render sprites
		DISPLAYSCREEN.fill(BGCOLOR) # paint background
		dirty_rects = []
		dirty_rects.append(timeCounter.render())
		dirty_rects.append(title1.render())
		dirty_rects.append(title2.render())
		dirty_rects.append(message.render())
		dirty_rects.append(author.render())
		dirty_rects.append(helpMessage.render())

		# draw sprites to screen
		pygame.display.update(dirty_rects)
		FPSCLOCK.tick(FPS)
		loop += 1

def showGameScreen():
	# instances!!!
	bar = Bar(DISPLAYSCREEN, (145, 190), (350, 100), NAVYBLUE, ORANGE, RED)
	scoreCounter = Counter(DISPLAYSCREEN, (WINDOWWIDTH / 2, WINDOWHEIGHT * 3 / 10), 0, BASICFONT, NAVYBLUE)

	DISPLAYSCREEN.fill(BGCOLOR) # paint background
	bar.render()
	scoreCounter.render()
	timeCounter.render()
	pygame.display.flip() # first screen update

	# set up vars
	loop = 0
	time = 0
	timeSinceEpoch = 0
	dirty_rects = [] # for updating
	while True: # main game loop
	### Note to self: speed up main loop
		for event in pygame.event.get(): # event handling loop
		
			if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
				terminate()
			if event.type == pygame.KEYDOWN:
				bar.highlight()
				if pressResponse(timeSinceEpoch) == 0:
					return scoreCounter.score # display score
				scoreCounter.increment(pressResponse(timeSinceEpoch))
				timeSinceEpoch -= 1
			if event.type == pygame.KEYUP:
				bar.normal()

		# tick clock
		dt = FPSCLOCK.tick(FPS)
		oldtime = time
		time += float(dt/1000.)
		timeSinceEpoch += float(dt/1000.)
		if oldtime % 1 > time % 1:
			pygame.mixer.Sound("sounds/Click.wav").play()
		if time > 2:
			time -= 2
		if timeSinceEpoch > 2:
			return scoreCounter.score
		
		# update sprites
		bar.update(time)
		timeCounter.set('{0:.2f}'.format(pygame.time.get_ticks() / 1000.))
		
		# render sprites
		DISPLAYSCREEN.fill(BGCOLOR) # paint background
		dirty_rects.append(bar.render())
		dirty_rects.append(scoreCounter.render())
		dirty_rects.append(timeCounter.render())
		
		# draw sprites to screen
		pygame.display.update(dirty_rects) # this doesn't work for some reason. why?
		dirty_rects = []
		#print(dt)
		loop += 1

def showEndingScreen(score):

	highscore = readStats("highscore")
	if score > highscore:
		changeStat("highscore", score)
		highscore = score

	scoreText = Text(DISPLAYSCREEN, (WINDOWWIDTH / 2, WINDOWHEIGHT / 2 - 10), "Your score was %i." % score, BASICFONT, BLACK)
	highscoreText = Text(DISPLAYSCREEN, (WINDOWWIDTH / 2, WINDOWHEIGHT / 2 + 15), "Your high score is %i." % highscore, SMALLFONT, BLACK)
	restartText = Text(DISPLAYSCREEN, (WINDOWWIDTH / 2, WINDOWHEIGHT - 30), "Press any key to play again.", BASICFONT, BLACK)

	DISPLAYSCREEN.fill(BGCOLOR) # paint background
	scoreText.render()
	highscoreText.render()
	restartText.render()
	pygame.display.update()

	loop = 0
	while True: # start screen main loop

		for event in pygame.event.get(): # event handling loop
			#print(event) ###
			if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
				terminate()
			if event.type == pygame.KEYDOWN:
				pygame.event.get() # clear event queue
				return
		
		# update sprites
		timeCounter.set('{0:.2f}'.format(pygame.time.get_ticks() / 1000.))
		
		# render sprites
		DISPLAYSCREEN.fill(BGCOLOR) # paint background
		dirty_rects = []
		dirty_rects.append(timeCounter.render())
		dirty_rects.append(scoreText.render())
		dirty_rects.append(highscoreText.render())
		dirty_rects.append(restartText.render())
		
		# draw sprites to screen
		pygame.display.update(dirty_rects)
		FPSCLOCK.tick(FPS)
		loop += 1

def showInstructionScreen():

	# initiate text
	title = '';
	message1 = '';
	message2 = '';

	# draw messages
	DISPLAYSCREEN.fill(BGCOLOR)
	title.render()
	message1.render()
	message2.render()

	loop = 0
	while True: # help screen main loop

		for event in pygame.event.get(): # event handling loop
			#print(event) ###
			if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
				terminate()
			elif event.type == pygame.KEYDOWN:
				pygame.event.get() # clear event queue
				return

		# update sprites
		timeCounter.set('{0:.2f}'.format(pygame.time.get_ticks() / 1000.))
		
		# render sprites
		DISPLAYSCREEN.fill(BGCOLOR) # paint background
		dirty_rects = []
		dirty_rects.append(timeCounter.render())
		dirty_rects.append(title.render())
		dirty_rects.append(message1.render())
		dirty_rects.append(message2.render())

		# draw sprites to screen
		pygame.display.update(dirty_rects)
		FPSCLOCK.tick(FPS)
		loop += 1

# gives the proper response to the press
def pressResponse(time):
	diff = 0.05
	return int(time > 1 - diff and time < 1 + diff)

# reads the current stats from the stats file and returns as a dict
def readStats(statName=None):
	statsDict = {}
	with open("data/stats.txt", "r") as statsFile:
		for line in statsFile.readlines():
			name = line.split(":")[0]
			value = line.split(":")[1]
			statsDict[name] = int(value)
	if statName != None:
		return statsDict[statName]
	else:
		return statsDict

# searches and changes the specified stat in the stats file
def changeStat(statName, newStat):
	statsDict = readStats()
	statsDict[statName] = newStat
	with open("data/stats.txt", "w") as statsFile:
		for stat in statsDict.keys():
			statsFile.write("%s:%s" % (str(stat), str(statsDict[stat])))

def terminate():
    pygame.quit()
    sys.exit()
