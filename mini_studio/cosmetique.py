import pygame

pygame.init()

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Set the dimensions of the screen
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Set the font for the menu
font = pygame.font.SysFont(None, 25)

# Set the menu options
menu_options = ["Skin 1", "Skin 2", "Skin 3", "Skin 4", "Skin 5", "Skin 6", "Skin 7", "Skin 8"]
selected_option = None

# Création des images pour le shop
option1_image = pygame.image.load("assets/vaisseau/Shop/vaisseau_01.png")
option1_rect = option1_image.get_rect()

option2_image = pygame.image.load("assets/vaisseau/Shop/vaisseau_02.png")
option2_rect = option2_image.get_rect()

option3_image = pygame.image.load("assets/vaisseau/Shop/vaisseau_03.png")
option3_rect = option3_image.get_rect()

option4_image = pygame.image.load("assets/vaisseau/Shop/vaisseau_04.png")
option4_rect = option4_image.get_rect()

option5_image = pygame.image.load("assets/vaisseau/Shop/vaisseau_05.png")
option5_rect = option5_image.get_rect()

option6_image = pygame.image.load("assets/vaisseau/Shop/vaisseau_06.png")
option6_rect = option6_image.get_rect()

option7_image = pygame.image.load("assets/vaisseau/Shop/vaisseau_07.png")
option7_rect = option7_image.get_rect()

option8_image = pygame.image.load("assets/vaisseau/Shop/vaisseau_08.png")
option8_rect = option8_image.get_rect()