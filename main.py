import pygame
from sys import exit as EXIT


def QUIT():
	pygame.quit()
	EXIT()


def save_cookies(clicked_cookies, clicked_cookies_best):
	if(clicked_cookies > clicked_cookies_best):
		clicked_cookies_best = clicked_cookies
		with open("cookies_highscore.data", "w") as f:
			f.write(str(clicked_cookies_best))


def load_cookies():
	with open("cookies_highscore.data", "r") as f:
		clicked_cookies_best = int(f.read())

	return clicked_cookies_best


pygame.mixer.pre_init(frequency=44100, size=16, channels=1, buffer=512)
pygame.init()

SCREENWIDTH = SCREENHEIGHT = 800
FPS = 60
CLOCK = pygame.time.Clock()
game_display = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
pygame.display.set_caption("Cookie Clicker Remake with Pygame")
pygame.mouse.set_visible(False)

# loading the font
game_font = pygame.font.Font("font.TTF", 75)
cookies_font = pygame.font.Font("font.TTF", 40)

# loading assets
background = pygame.transform.scale(pygame.image.load("background.png"), (SCREENWIDTH, SCREENHEIGHT)).convert_alpha()
cursor = pygame.image.load("cursor.png").convert_alpha()
# buttons
reset_button = pygame.image.load("reset_button.png").convert_alpha()
reset_button_clicked = pygame.image.load("reset_button_clicked.png").convert_alpha()
sound_button = pygame.image.load("sound_button.png").convert_alpha()
sound_button_clicked = pygame.image.load("sound_button_clicked.png").convert_alpha()

clicked_cookies_best = load_cookies()

cookie = pygame.transform.scale(pygame.image.load("cookie.png"), (350, 350)).convert_alpha()
cookie_rect = cookie.get_rect()
cookie_rect.x = SCREENWIDTH // 2 - cookie.get_width() // 2
cookie_rect.y = SCREENHEIGHT // 2 - cookie.get_height() // 2

cookie_clicked = pygame.transform.scale(pygame.image.load("cookie.png"), (365, 365)).convert_alpha()
cookie_clicked_rect = cookie_clicked.get_rect()
cookie_clicked_rect.x = SCREENWIDTH // 2 - cookie_clicked.get_width() // 2
cookie_clicked_rect.y = SCREENHEIGHT // 2 - cookie_clicked.get_height() // 2

cookie_sound = pygame.mixer.Sound("click.wav")
button_sound = pygame.mixer.Sound("button_sound.wav")
positive1_sound = pygame.mixer.Sound("positive1.wav")
positive2_sound = pygame.mixer.Sound("positive2.wav")

sound_on = True

click_timer = 0.1
click_timer_running = False
click_timer_initial_time = None

clicked_cookies = 0

# text(s)
title_text = game_font.render("Cookie Clicker", True, (233, 153, 51))
best_title_text = cookies_font.render("Best", True, (251, 206, 17))
best_cookies_text = cookies_font.render(f"{clicked_cookies_best} cookies", True, (251, 206, 17))
current_title_text = cookies_font.render("Current", True, (233, 153, 51))
current_cookies_text = cookies_font.render(f"{clicked_cookies} cookies", True, (233, 153, 51))

run = True
while run:
	CLOCK.tick(FPS)
	# event section start
	for event in pygame.event.get():
		if(event.type == pygame.QUIT):
			save_cookies(clicked_cookies, clicked_cookies_best)
			QUIT()
		if(event.type == pygame.MOUSEBUTTONDOWN):
			if(event.button == 1):
				if(cookie_rect.collidepoint(event.pos)):
					# cookie click
					if(sound_on):
						pygame.mixer.Sound.play(cookie_sound)
					clicked_cookies += 1
					current_cookies_text = cookies_font.render(f"{clicked_cookies} cookies", True, (233, 153, 51))
					if(clicked_cookies != 0 and sound_on):
						if(clicked_cookies % 1000 == 0):
							# play positive2 sound
							pygame.mixer.Sound.play(positive2_sound)
						elif(clicked_cookies % 100 == 0):
							# play positive1 sound
							pygame.mixer.Sound.play(positive1_sound)

					click_timer_running = True
					click_timer_initial_time = pygame.time.get_ticks() / 1000
				elif(event.pos[0] >= SCREENWIDTH - 40 - reset_button.get_width() and event.pos[0] <= SCREENWIDTH - 40 and event.pos[1] >= SCREENHEIGHT // 2 - reset_button.get_height() // 2 and event.pos[1] <= SCREENHEIGHT // 2 - reset_button.get_height() // 2 + reset_button.get_height()):
					# reset button click
					if(sound_on):
						pygame.mixer.Sound.play(button_sound)
					save_cookies(clicked_cookies, clicked_cookies_best)

					clicked_cookies = 0
					current_cookies_text = cookies_font.render(f"{clicked_cookies} cookies", True, (233, 153, 51))

					clicked_cookies_best = load_cookies()
					best_cookies_text = cookies_font.render(f"{clicked_cookies_best} cookies", True, (251, 206, 17))
				elif(event.pos[0] >= 0 + 40 and event.pos[0] <= 0 + 40 + sound_button.get_width() and event.pos[1] >= SCREENHEIGHT // 2 - sound_button.get_height() // 2 and event.pos[1] <= SCREENHEIGHT // 2 - sound_button.get_height() // 2 + sound_button.get_height()):
					# sound button click
					if(sound_on):
						pygame.mixer.Sound.play(button_sound)
					
					sound_on = not sound_on
	# event section end

	if(click_timer_running):
		if(pygame.time.get_ticks() / 1000 - click_timer_initial_time >= click_timer):
			click_timer_initial_time = None
			click_timer_running = False

	# getting the current mouse position
	mouse_pos = pygame.mouse.get_pos()

	# filling the display surface
	game_display.blit(background, (0, 0))

	# displaying the seperator line(s)
	pygame.draw.line(game_display, (233, 153, 51), (SCREENWIDTH // 2, 620), (SCREENWIDTH // 2, 760))

	# displaying the text(s)
	game_display.blit(title_text, (SCREENWIDTH // 2 - title_text.get_width() // 2, 75))     # title

	game_display.blit(current_title_text, (SCREENWIDTH // 2 + 50, 620))
	game_display.blit(current_cookies_text, (SCREENWIDTH // 2 + 50, 700))

	game_display.blit(best_title_text, (SCREENWIDTH // 2 - 50 - best_title_text.get_width(), 620))
	game_display.blit(best_cookies_text, (SCREENWIDTH // 2 - 50 - best_cookies_text.get_width(), 700))

	# button(s)
	if(mouse_pos[0] >= SCREENWIDTH - 40 - reset_button.get_width() and mouse_pos[0] <= SCREENWIDTH - 40 and mouse_pos[1] >= SCREENHEIGHT // 2 - reset_button.get_height() // 2 and mouse_pos[1] <= SCREENHEIGHT // 2 - reset_button.get_height() // 2 + reset_button.get_height()):
		game_display.blit(reset_button_clicked, (SCREENWIDTH - 40 - reset_button.get_width(), SCREENHEIGHT // 2 - reset_button.get_height() // 2))
	else:
		game_display.blit(reset_button, (SCREENWIDTH - 40 - reset_button.get_width(), SCREENHEIGHT // 2 - reset_button.get_height() // 2))
	
	if(mouse_pos[0] >= 0 + 40 and mouse_pos[0] <= 0 + 40 + sound_button.get_width() and mouse_pos[1] >= SCREENHEIGHT // 2 - sound_button.get_height() // 2 and mouse_pos[1] <= SCREENHEIGHT // 2 - sound_button.get_height() // 2 + sound_button.get_height()):
		game_display.blit(sound_button_clicked, (0 + 40, SCREENHEIGHT // 2 - sound_button.get_height() // 2))
	else:
		game_display.blit(sound_button, (0 + 40, SCREENHEIGHT // 2 - sound_button.get_height() // 2))

	# displaying the cookie
	if(not click_timer_running):
		game_display.blit(cookie, cookie_rect)
	else:
		game_display.blit(cookie_clicked, cookie_clicked_rect)

	# displaying the custom mouse cursor
	game_display.blit(cursor, mouse_pos)

	# updating the display surface
	pygame.display.update()
