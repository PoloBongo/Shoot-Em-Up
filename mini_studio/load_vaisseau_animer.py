import pygame, os

width, height = 1000, 600

# -------------------------------------------- Chargement des images des animations des vaisseaux -------------------------------------------- #
vaisseau_1 = []
for i in range(1, 7):
    filename = os.path.join("assets/vaisseau/Vaisseau_1/", f"vaisseau_0{i}.png")
    image_1 = pygame.image.load(filename)
    image_1 = pygame.transform.scale(image_1, (width // 12, height // 7))
    vaisseau_1.append(image_1)

vaisseau_2 = []
for i in range(1, 7):
    filename = os.path.join("assets/vaisseau/Vaisseau_2/", f"vaisseau_0{i}.png")
    image_2 = pygame.image.load(filename)
    image_2 = pygame.transform.scale(image_2, (width // 12, height // 7))
    vaisseau_2.append(image_2)

vaisseau_3 = []
for i in range(1, 7):
    filename = os.path.join("assets/vaisseau/Vaisseau_3/", f"vaisseau_0{i}.png")
    image_3 = pygame.image.load(filename)
    image_3 = pygame.transform.scale(image_3, (width // 12, height // 7))
    vaisseau_3.append(image_3)

vaisseau_4 = []
for i in range(1, 7):
    filename = os.path.join("assets/vaisseau/Vaisseau_4/", f"vaisseau_0{i}.png")
    image_4 = pygame.image.load(filename)
    image_4 = pygame.transform.scale(image_4, (width // 12, height // 7))
    vaisseau_4.append(image_4)

vaisseau_5 = []
for i in range(1, 7):
    filename = os.path.join("assets/vaisseau/Vaisseau_5/", f"vaisseau_0{i}.png")
    image_5 = pygame.image.load(filename)
    image_5 = pygame.transform.scale(image_5, (width // 12, height // 7))
    vaisseau_5.append(image_5)

vaisseau_6 = []
for i in range(1, 8):
    filename = os.path.join("assets/vaisseau/Vaisseau_6/", f"vaisseau_0{i}.png")
    image_6 = pygame.image.load(filename)
    image_6 = pygame.transform.scale(image_6, (width // 12, height // 7))
    vaisseau_6.append(image_6)

vaisseau_7 = []
for i in range(1, 9):
    filename = os.path.join("assets/vaisseau/Vaisseau_7/", f"vaisseau_0{i}.png")
    image_7 = pygame.image.load(filename)
    image_7 = pygame.transform.scale(image_7, (width // 12, height // 7))
    vaisseau_7.append(image_7)

vaisseau_8 = []
for i in range(1, 7):
    filename = os.path.join("assets/vaisseau/Vaisseau_8/", f"vaisseau_0{i}.png")
    image_8 = pygame.image.load(filename)
    image_8 = pygame.transform.scale(image_8, (width // 12, height // 7))
    vaisseau_8.append(image_8)

# Load Laser Skill [q] sprite
beam_image = []
for i in range(1, 4):
    filename = os.path.join("assets/vaisseau/Projectile/q_skill/", f"skill_0{i}.png")
    image_beam = pygame.image.load(filename)
    image_beam = pygame.transform.scale(image_beam, (32,800))
    beam_image.append(image_beam)

# Load bullet custom
bullet_image = []
for i in range(0, 3):
    filename = os.path.join("assets/bullet", f"bullet_0{i}.png")
    image_bullet = pygame.image.load(filename)
    image_bullet = pygame.transform.scale(image_bullet, (25,75))
    bullet_image.append(image_bullet)

# Load w skill bullet custom
w_skill_bullet_image = []
for i in range(0, 2):
    filename = os.path.join("assets/vaisseau/Projectile/Bullet", f"bullet_0{i}.png")
    w_skill_image_bullet = pygame.image.load(filename)
    w_skill_image_bullet = pygame.transform.scale(w_skill_image_bullet, (25,75))
    w_skill_bullet_image.append(w_skill_image_bullet)

################################ ANIMATION DES 6 VAISSEAUX SUR 8 QUAND IL PREND LE BOOST SHIELD ################################
vaisseau_06_shield_image = []
for i in range(0, 9):
    filename = os.path.join("assets/vaisseau/Shield/Vaisseau_06", f"shield_0{i}.png")
    vaisseau_06_image_shield = pygame.image.load(filename)
    vaisseau_06_image_shield = pygame.transform.scale(vaisseau_06_image_shield, (80,80))
    vaisseau_06_shield_image.append(vaisseau_06_image_shield)

vaisseau_07_shield_image = []
for i in range(0, 9):
    filename = os.path.join("assets/vaisseau/Shield/Vaisseau_07", f"shield_0{i}.png")
    vaisseau_07_image_shield = pygame.image.load(filename)
    vaisseau_07_image_shield = pygame.transform.scale(vaisseau_07_image_shield, (80,80))
    vaisseau_07_shield_image.append(vaisseau_07_image_shield)

vaisseau_01_shield_image = []
for i in range(0, 9):
    filename = os.path.join("assets/vaisseau/Shield/Vaisseau_01", f"shield_0{i}.png")
    vaisseau_01_image_shield = pygame.image.load(filename)
    vaisseau_01_image_shield = pygame.transform.scale(vaisseau_01_image_shield, (80,80))
    vaisseau_01_shield_image.append(vaisseau_01_image_shield)

vaisseau_02_shield_image = []
for i in range(0, 9):
    filename = os.path.join("assets/vaisseau/Shield/Vaisseau_02", f"shield_0{i}.png")
    vaisseau_02_image_shield = pygame.image.load(filename)
    vaisseau_02_image_shield = pygame.transform.scale(vaisseau_02_image_shield, (80,80))
    vaisseau_02_shield_image.append(vaisseau_02_image_shield)

vaisseau_03_shield_image = []
for i in range(0, 5):
    filename = os.path.join("assets/vaisseau/Shield/Vaisseau_03", f"shield_0{i}.png")
    vaisseau_03_image_shield = pygame.image.load(filename)
    vaisseau_03_image_shield = pygame.transform.scale(vaisseau_03_image_shield, (80,80))
    vaisseau_03_shield_image.append(vaisseau_03_image_shield)
############################### Vaisseau 6 ANIMATION DES 6 ROCKETS QUAND IL PREND LE BOOST ################################

vaisseau_06_rocket_image = []
for i in range(0, 6):
    filename = os.path.join("assets/vaisseau/Rocket/Tire", f"rocket_0{i}.png")
    vaisseau_06_image_rocket = pygame.image.load(filename)
    vaisseau_06_image_rocket = pygame.transform.scale(vaisseau_06_image_rocket, (82,89))
    vaisseau_06_rocket_image.append(vaisseau_06_image_rocket)

vaisseau_06_rocket2_image = []
for i in range(0, 2):
    filename = os.path.join("assets/vaisseau/Rocket/Tire2", f"rocket_0{i}.png")
    vaisseau_06_image_rocket2 = pygame.image.load(filename)
    vaisseau_06_image_rocket2 = pygame.transform.scale(vaisseau_06_image_rocket2, (82,89))
    vaisseau_06_rocket2_image.append(vaisseau_06_image_rocket2)

vaisseau_06_rocket3_image = []
for i in range(0, 2):
    filename = os.path.join("assets/vaisseau/Rocket/Tire3", f"rocket_0{i}.png")
    vaisseau_06_image_rocket3 = pygame.image.load(filename)
    vaisseau_06_image_rocket3 = pygame.transform.scale(vaisseau_06_image_rocket3, (82,89))
    vaisseau_06_rocket3_image.append(vaisseau_06_image_rocket3)

vaisseau_06_rocket4_image = []
for i in range(0, 2):
    filename = os.path.join("assets/vaisseau/Rocket/Tire4", f"rocket_0{i}.png")
    vaisseau_06_image_rocket4 = pygame.image.load(filename)
    vaisseau_06_image_rocket4 = pygame.transform.scale(vaisseau_06_image_rocket4, (82,89))
    vaisseau_06_rocket4_image.append(vaisseau_06_image_rocket4)

vaisseau_06_rocket5_image = []
for i in range(0, 2):
    filename = os.path.join("assets/vaisseau/Rocket/Tire5", f"rocket_0{i}.png")
    vaisseau_06_image_rocket5 = pygame.image.load(filename)
    vaisseau_06_image_rocket5 = pygame.transform.scale(vaisseau_06_image_rocket5, (82,89))
    vaisseau_06_rocket5_image.append(vaisseau_06_image_rocket5)

vaisseau_06_rocket6_image = []
for i in range(0, 2):
    filename = os.path.join("assets/vaisseau/Rocket/Tire6", f"rocket_0{i}.png")
    vaisseau_06_image_rocket6 = pygame.image.load(filename)
    vaisseau_06_image_rocket6 = pygame.transform.scale(vaisseau_06_image_rocket6, (82,89))
    vaisseau_06_rocket6_image.append(vaisseau_06_image_rocket6)