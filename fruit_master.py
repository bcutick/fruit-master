#Brendan Cutick
#0202
import random
import time
import pygame
from pygame import mixer
import math
from pynput.mouse import Listener

#INITIALIZING ASPECTS OF PYGAME

#Initialize pygame
pygame.init()

#Create the screen
screen = pygame.display.set_mode((800, 600)) #(width, height)  0 is at top, 600 is at bottom, left is 0, 800 is right

#Background music
mixer.music.load('fruit_ninja_theme.mp3')
mixer.music.play(-1) #Minus 1 means play on loop

#Create the icon and title
pygame.display.set_caption("Fruit Master")
icon = pygame.image.load('ninja.png')
pygame.display.set_icon(icon)

#FUNCTIONS THAT ARE USED IN THE APP
def button(message, x, y, w, h, dark, bright, action=None):
	#Creating the buttons on the intro screen
	#Might need a lot of buttons, so it's easiest to make a button function
	mouse = pygame.mouse.get_pos()
	clicker = pygame.mouse.get_pressed()
	smallText = pygame.font.Font('freesansbold.ttf', 30)
	text = smallText.render(message, True, (0, 0, 0))
	#Making these if loops changes the colors of the rectangles when the mouse is over them
	#which gives the illusion that the buttons are interactive. Also makes it easier for user.
	if ((x+w) > mouse[0] > x) and ((y+h) > mouse[1] > y):
		pygame.draw.rect(screen, bright, (x, y, w, h))
		screen.blit(text, (x+10, y+15))
		#If the computer registers a click while the mouse is over the button and there is an action defined, do something
		if clicker[0] == 1 and action != None:
			#Outlining cases for each particular button action
			if action == "play":
				game_loop()
			elif action == "quit":
				pygame.quit()
				quit()
			elif action == "back":
				main_menu()
			elif action == "htp":
				how_to_play()
			elif action == "backhome":
				mixer.music.load('fruit_ninja_theme.mp3')
				mixer.music.play(-1) #Minus 1 means play on loop
				main_menu()
	else:
		pygame.draw.rect(screen, dark, (x, y, w, h))
		screen.blit(text, (x+10, y+15))

#Main menu screen
def main_menu():
	intro = True
	#Loop for the intro screen
	while intro:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
		#Setting up the main menu
		
		#Read in the high score value from the text documted
		#If the user got a new high score, it will be written in during the game loop
		#If the user didn't get a new high score, the old high score will stand
		highscore_file = open('highscore.txt.', 'r')
		highscore = highscore_file.readline()
		highscore_file.close()

		pygame.mouse.set_visible(True) #resets the mouse to visible in case returning from game
		screen.fill((255, 255, 255))
		introbackground = pygame.image.load('introbackground.png')
		screen.blit(introbackground, (0,0))
		largeText = pygame.font.Font('ninjafont.ttf', 70)
		intro_text = largeText.render("Fruit  Master", True, (0, 0, 0))
		screen.blit(intro_text, (270, 50))

		#Write the highscore to the main menu screen
		pygame.draw.rect(screen, (0, 0, 0), (375, 525, 450, 75))
		hightext = pygame.font.Font('highscore.ttf', 50)
		scoretext = hightext.render("High score: " + str(highscore), True, (255, 255, 255))
		screen.blit(scoretext, (385,540))

		#Creating the main menu buttons
		button("Click to play", 525, 200, 200, 50, (0, 200, 0), (0, 255, 0), "play")
		button("How to play", 525, 300, 200, 50, (200, 200, 0), (255, 255, 0), "htp")
		button("Quit", 525, 400, 200, 50, (200, 0, 0), (255, 0, 0), "quit")

		pygame.display.update()

#How to play screen
def how_to_play():
	intro = True
	while intro:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
		pygame.mouse.set_visible(True) #resets the mouse to visible in case returning from game
		screen.fill((255, 255, 255))
		largeText = pygame.font.Font('freesansbold.ttf', 70)
		htp_text = largeText.render("How to play", True, (0, 0, 0))
		screen.blit(htp_text, (225, 50))
		pygame.draw.rect(screen, (224, 224, 224), (130, 150, 600, 220))
		gametext = pygame.font.Font('freesansbold.ttf', 14)
		line1 = gametext.render("You have 59 seconds to use the mouse and click on as many fruits as possible!", True, (0, 0, 0))
		line2 = gametext.render("You have 3 lives. Every time you hit a bomb you lose a life.", True, (0, 0, 0))
		line3 = gametext.render("If you hit multiple fruits with one click, you gain some extra score.", True, (0, 0, 0))
		line4 = gametext.render("Once you lose all 3 lives or run out of time, the game will end.", True, (0, 0, 0))
		line6 = gametext.render("After the game has ended, click the 'Return Home' button to go back to the menu.", True, (0, 0, 0))
		line7 = gametext.render("Good luck!", True, (0, 0 , 0))
		line5 = gametext.render("Your score and lives will be displayed in the top left corner of the screen.", True, (0, 0, 0))
		screen.blit(line1, (140, 160))
		screen.blit(line2, (140, 190))
		screen.blit(line5, (140, 220))
		screen.blit(line3, (140, 250))
		screen.blit(line4, (140, 280))
		screen.blit(line6, (140, 310))
		screen.blit(line7, (140, 340))

		#Creating the back button
		button("Back", 300, 500, 200, 50, (200, 0, 200), (255, 0, 255), "back")
		pygame.display.update()

#Actual game loop where the real game takes place
def game_loop():

	#Loading in all the images and setting up the game loop
	background = pygame.image.load('fruitbackground.png')
	score_value = 0
	font = pygame.font.Font('freesansbold.ttf', 32)
	timefont = pygame.font.Font('freesansbold.ttf', 60)
	peach = pygame.image.load('orange.png')
	bomb = pygame.image.load('bomb.png')
	livesimg = pygame.image.load('heart.png')
	scoresimg = pygame.image.load('star.png')

	#Defining the initial fruit positions
	num_of_fruits = 6
	fruitX = []
	fruitY = []
	dX = []
	dY = []
	time = []
	angle = []
	velocity = []

	for a in range(num_of_fruits):
		fruitX.append(random.randint(64,736))
		fruitY.append(random.randint(400,536))
		dX.append(0)
		dY.append(0)
		time.append(pygame.time.get_ticks())
		angle.append(random.uniform(1.309, 1.8326))
		velocity.append(random.uniform(2.25, 2.75))

	#Defining the initial bomb positions
	num_of_bombs = 3
	bombX = []
	bombY = []
	dXb = []
	dYb =[]
	timeb = []
	angleb = []
	velocityb = []

	for a in range(num_of_bombs):
		bombX.append(random.randint(64,736))
		bombY.append(random.randint(400, 700))
		dXb.append(0)
		dYb.append(0)
		timeb.append(pygame.time.get_ticks())
		angleb.append(random.uniform(1.309, 1.8326))
		velocityb.append(random.uniform(2.25, 2.75))

	#Defining lives
	num_lives = 3

	#Starting the clock timer for the game
	start_ticks = pygame.time.get_ticks()
	rseconds = 0

	livesfont = pygame.font.Font('freesansbold.ttf', 48)
	over_font = pygame.font.Font('freesansbold.ttf', 64)

	#List of all the functions that are going to be called in the "while running" loop
	#Most are self explanatory
	def show_time(x,y):
		clock = timefont.render(str(rseconds), True, (148, 0, 211))
		screen.blit(clock, (x, y))

	def show_time_red(x,y):
		clock = timefont.render(str(rseconds), True, (255, 0, 0))
		screen.blit(clock, (x, y))		

	def show_lives(x,y,x1,y1):
		lives = livesfont.render(str(num_lives), True, (255, 255, 255))
		screen.blit(lives, (x, y))
		screen.blit(livesimg, (x1, y1))

	def show_score(x, y, x1, y1):
		score = livesfont.render(str(score_value), True, (255,255,255))
		screen.blit(score, (x, y))
		screen.blit(scoresimg, (x1, y1))

	def spawnFruit(x, y):
		screen.blit(peach, (x, y))

	def spawnBomb(x,y):
		screen.blit(bomb, (x, y))

	def game_over_text(finalscore):
		over_text = over_font.render("GAME OVER", True, (255, 0, 0))
		screen.blit(over_text, (200, 250))
		mixer.music.stop()
		button("Return home", 300, 450, 200, 50, (200, 0, 200), (255, 0, 255), "backhome")
		score_text = over_font.render("Final Score: " + str(finalscore), True, (255, 255, 255))
		screen.blit(score_text, (180, 100))

	def game_over_highscore(finalscore):
		over_text = over_font.render("GAME OVER", True, (255, 0, 0))
		screen.blit(over_text, (200, 250))
		mixer.music.stop()
		button("Return home", 300, 450, 200, 50, (200, 0, 200), (255, 0, 255), "backhome")
		score_text = over_font.render("Final Score: " + str(finalscore), True, (255, 255, 0))
		high_score = over_font.render("NEW HIGH SCORE!", True, (255, 255, 0))
		screen.blit(high_score, (105, 80))
		screen.blit(score_text, (180, 150))
	#mouse_state = "up"
	running = True
	while running:

		#Pre-background
		screen.fill((0,0,0))
		#Background
		screen.blit(background, (0,0))

		#Cursor position
		cursorX = pygame.mouse.get_pos()[0]
		cursorY = pygame.mouse.get_pos()[1]

		#Mouse state initialize
		mouse_state = "up"
		#Fruit collision function that calculates whether or not the cursor is close enough to the fruit to be
		#considered a collision. If it is, it returns true.
		def fruitCollision(fruitX, fruitY, cursorX, cursorY):
			d = math.hypot(fruitX - cursorX, fruitY - cursorY)
			if d < 55:
				a = 1
				return a
			else:
				a = 0
				return a

		#Bomb collision function (does the same as fruit collision)
		def bombCollision(bombX, bombY, cursorX, cursorY):
			d = math.hypot(bombX - cursorX, bombY - cursorY)
			if d < 55:
				a = 1
				return a
			else:
				a = 0
				return a

		#Event lines in pygame. These lines check to see if any keys have been clicked
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False

			#If the mouse is down the mouse state goes to down and it plays a slicing sound
			if event.type == pygame.MOUSEBUTTONDOWN:
				mouse_state = "down"

			#If the mouse is up the mouse state goes to up
			if event.type == pygame.MOUSEBUTTONUP:
				mouse_state = "up"

		#Setting up the time variables
		seconds = (pygame.time.get_ticks() - start_ticks) / 1000
		rseconds = int(round(seconds, 0))
		highscore_file = open('highscore.txt.', 'r')
		highscore = int(highscore_file.readline())
		highscore_file.close()
		#Mini game loop inside a game loop. This runs as long as the number of lives aren't 0 and the time isn't over the limit
		if num_lives > 0 and seconds <= 59:
			#Fruit movement
			counter = 0
			for i in range(num_of_fruits):
				#Kinematic equation fruit movement (Conditions make sure the fruit is still on the screen)
				dX[i] = (velocity[i])*math.cos(angle[i])
				dY[i] = ((velocity[i])*math.sin(angle[i]) - (0.5*2.81* ((pygame.time.get_ticks() - time[i]) / 1000) * ((pygame.time.get_ticks() - time[i]) / 1000)))

				#Fruit collision if statement
				fruitcollision = fruitCollision(fruitX[i], fruitY[i], cursorX, cursorY)
				if fruitcollision == 1:
					counter += 1
				#If the user hits more than one fruit in a click, increase the score by the number of fruits plus 1
				#This serves as an incentive to try and hit multiple fruits at the same time
				if fruitcollision == 1 and mouse_state == "down" and counter > 1:
					slicesound = mixer.Sound('slice.wav')
					slicesound.play()
					#If the user hits a fruit, that fruit gets sent back down to the bottom of the screen
					#This new fruit is given an entirely new position, velocity, and trajectory
					fruitY[i] = random.randint(650, 750)
					fruitX[i] = random.randint(64,736)
					time[i] = pygame.time.get_ticks()
					angle[i] = random.uniform(1.309, 1.8326)
					velocity[i] = random.uniform(2.75, 3.25) #2.75 - 3.25
					score_value += (counter)

				elif fruitcollision == 1 and mouse_state == "down" and counter <= 1:
					slicesound = mixer.Sound('slice.wav')
					slicesound.play()
					#If the user hits a fruit, that fruit gets sent back down to the bottom of the screen
					#This new fruit is given an entirely new position, velocity, and trajectory
					fruitY[i] = random.randint(650, 750)
					fruitX[i] = random.randint(64,736)
					time[i] = pygame.time.get_ticks()
					angle[i] = random.uniform(1.309, 1.8326)
					velocity[i] = random.uniform(2.75, 3.25) #2.75 - 3.25
					score_value += 1

				#User not hitting fruit and fruit going off screen if statement
				if fruitY[i] > 700:
					fruitY[i] = random.randint(650, 750)
					fruitX[i] = random.randint(64,736)
					time[i] = pygame.time.get_ticks()
					angle[i] = random.uniform(1.309, 1.8326)
					velocity[i] = random.uniform(2.75, 3.25)

				fruitX[i] += dX[i]
				fruitY[i] -= dY[i]

				spawnFruit(fruitX[i], fruitY[i])

			#Bomb movement
			for i in range(num_of_bombs):
				#Kinematic equation fruit movement (Conditions make sure the fruit is still on the screen)
				dXb[i] = (velocityb[i])*math.cos(angleb[i])
				dYb[i] = ((velocityb[i])*math.sin(angleb[i]) - (0.5*2.81* ((pygame.time.get_ticks() - timeb[i]) / 1000) * ((pygame.time.get_ticks() - timeb[i]) / 1000)))

				#Bomb collision if statement
				bombcollision = bombCollision(bombX[i], bombY[i], cursorX, cursorY)
				if bombcollision == 1 and mouse_state == "down":
					bombsound = mixer.Sound('pacman_death.wav')
					bombsound.play()
					bombY[i] = random.randint(650, 750)
					bombX[i] = random.randint(64,736)
					timeb[i] = pygame.time.get_ticks()
					angleb[i] = random.uniform(1.309, 1.8326)
					velocityb[i] = random.uniform(2.75, 3.25)
					num_lives -= 1

				#User not hitting bomb and bomb going off screen if statement
				#User not hitting fruit and fruit going off screen if statement
				if bombY[i] > 700:
					bombY[i] = random.randint(650, 750)
					bombX[i] = random.randint(64,736)
					timeb[i] = pygame.time.get_ticks()
					angleb[i] = random.uniform(1.309, 1.8326)
					velocityb[i] = random.uniform(2.75, 3.25)				

				bombY[i] -= dYb[i]
				bombX[i] += dXb[i]

				spawnBomb(bombX[i], bombY[i])

			#Calling certain in game functions such as show lives and show score
			show_lives(90, 90, 10, 80)
			show_score(90, 20, 10, 10)

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					running = False
				if event.type == pygame.KEYDOWN:
					print("check")
					if event.key == pygame.K_SPACE and pup == 0: #Checks to see if the space bar is pressed
						print("Power up initiated")
			#Showing the time remaining on the screen in white
			if seconds < 51:
				show_time(420, 10)
			#During the last 9 seconds of the game, the remaining time turns to red to alert the user
			#that time is running out
			if 51 <= seconds <= 59:
				show_time_red(420,10)

			#Reading in high score data
			highscore_file = open('highscore.txt.', 'r')
			highscore = int(highscore_file.readline())
			highscore_file.close()

			#Variable to check to see if a new highscore has been made
			z = 0
			if score_value > highscore:
				z = 1

			pygame.mouse.set_visible(False) #hides the cursor
			mycursor = pygame.image.load('cursorbig.png')
			screen.blit(mycursor, (pygame.mouse.get_pos() ))

		#GAME END SITUATIONS
		#Situation number 1 for game end: number of lives is 0 and a high score was made
		elif num_lives <= 0 and z == 1:
			newhighscorefile = open('highscore.txt', 'r+')
			newhighscorefile.truncate(0)
			newhighscorefile.close()
			newhighscorefile = open('highscore.txt', 'w')
			newhighscorefile.write(str(score_value))
			newhighscorefile.close()
			game_over_highscore(score_value)
			pygame.mouse.set_visible(False) #hides the cursor
			mycursor = pygame.image.load('cursorbig.png')
			screen.blit(mycursor, (pygame.mouse.get_pos() ))
		#Situation 2: num lives is 0 and high score was not made
		elif num_lives <= 0 and z != 1:
			game_over_text(score_value)
			pygame.mouse.set_visible(False) #hides the cursor
			mycursor = pygame.image.load('cursorbig.png')
			screen.blit(mycursor, (pygame.mouse.get_pos() ))
		#Situation 3 for game end: time runs out and high score was made
		elif seconds > 59 and z == 1:
			newhighscorefile = open('highscore.txt', 'r+')
			newhighscorefile.truncate(0)
			newhighscorefile.close()
			newhighscorefile = open('highscore.txt', 'w')
			newhighscorefile.write(str(score_value))
			newhighscorefile.close()
			game_over_highscore(score_value)
			pygame.mouse.set_visible(False) #hides the cursor
			mycursor = pygame.image.load('cursorbig.png')
			screen.blit(mycursor, (pygame.mouse.get_pos() ))
		#Situation 4 for game end: time runs out and no high score was made
		elif seconds > 59 and z != 1:
			game_over_text(score_value)
			pygame.mouse.set_visible(False) #hides the cursor
			mycursor = pygame.image.load('cursorbig.png')
			screen.blit(mycursor, (pygame.mouse.get_pos() ))

		pygame.display.update() #Want to update the screen after every move (game window)

#Calls the main menu function to start the game. Up to the user where to go from here.
main_menu()