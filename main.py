import pygame
from sys import exit as EXIT


def QUIT():
	pygame.quit()
	EXIT()


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

cookie = pygame.transform.scale(pygame.image.load("cookie.png"), (350, 350)).convert_alpha()
cookie_rect = cookie.get_rect()
cookie_rect.x = SCREENWIDTH // 2 - cookie.get_width() // 2
cookie_rect.y = SCREENHEIGHT // 2 - cookie.get_height() // 2

cookie_clicked = pygame.transform.scale(pygame.image.load("cookie.png"), (365, 365)).convert_alpha()
cookie_clicked_rect = cookie_clicked.get_rect()
cookie_clicked_rect.x = SCREENWIDTH // 2 - cookie_clicked.get_width() // 2
cookie_clicked_rect.y = SCREENHEIGHT // 2 - cookie_clicked.get_height() // 2

cookie_sound = pygame.mixer.Sound("click.wav")
positive1_sound = pygame.mixer.Sound("positive1.wav")
positive2_sound = pygame.mixer.Sound("positive2.wav")

click_timer = 0.1
click_timer_running = False
click_timer_initial_time = None

clicked_cookies = 0

# text(s)
title_text = game_font.render("Cookie Clicker", True, (233, 153, 51))
cookies_text = cookies_font.render(f"{clicked_cookies} cookies", True, (233, 153, 51))

run = True
while run:
	CLOCK.tick(FPS)
	# event section start
	for event in pygame.event.get():
		if(event.type == pygame.QUIT):
			QUIT()
		if(event.type == pygame.MOUSEBUTTONDOWN):
			if(event.button == 1):
				if(cookie_rect.collidepoint(event.pos)):
					pygame.mixer.Sound.play(cookie_sound)
					clicked_cookies += 1
					cookies_text = cookies_font.render(f"{clicked_cookies} cookies", True, (233, 153, 51))
					if(clicked_cookies != 0):
						if(clicked_cookies % 1000 == 0):
							# play positive2 sound
							pygame.mixer.Sound.play(positive2_sound)
						elif(clicked_cookies % 100 == 0):
							# play positive1 sound
							pygame.mixer.Sound.play(positive1_sound)

					click_timer_running = True
					click_timer_initial_time = pygame.time.get_ticks() / 1000
	# event section end

	if(click_timer_running):
		if(pygame.time.get_ticks() / 1000 - click_timer_initial_time >= click_timer):
			click_timer_initial_time = None
			click_timer_running = False

	# filling the display surface
	game_display.blit(background, (0, 0))

	# displaying the text(s)
	game_display.blit(title_text, (SCREENWIDTH // 2 - title_text.get_width() // 2, 75))
	game_display.blit(cookies_text, (SCREENWIDTH // 2 - cookies_text.get_width() // 2, SCREENHEIGHT - 75))

	# displaying the cookie
	if(not click_timer_running):
		game_display.blit(cookie, cookie_rect)
	else:
		game_display.blit(cookie_clicked, cookie_clicked_rect)

	# displaying the custom mouse cursor
	mouse_pos = pygame.mouse.get_pos()
	game_display.blit(cursor, mouse_pos)

	# updating the display surface
	pygame.display.update()
