import pygame
import random
import math
from load_vaisseau_animer import *
from vaisseau import *
from classe import *

# Initialize Pygame
pygame.init()

# Charger l'icône
icon = pygame.image.load("assets/alien_war_icon.png")

# Définir l'icône de la fenêtre
pygame.display.set_icon(icon)

score = 0

# ----------------------------------- Récupérer la valeur dans Vaisseau.txt ----------------------------- #
def get_selected_option():
    try:
        with open("./Save_Stats/Skin_Vaisseau.txt", "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return None

# ----------------------------------- Récupérer la valeur dans Vaisseau_Stats.txt ----------------------------- #
def get_stats():
    try:
        with open("./Save_Stats/Vaisseau_stats.txt", "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return None
# ----------------------------------- Récupérer la valeur dans Player_Gold.txt ----------------------------- #
def get_gold():
    try:
        with open("./Save_Stats/Player_Gold.txt", "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return None
    
# ----------------------------------- Récupérer la valeur dans Statut_Boss.txt ----------------------------- #
def get_player_score():
    try:
        with open("./Save_Stats/Player_Score.txt", "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return None
# ----------------------------------- Charge le font ----------------------------- #
def get_font(size):
    return pygame.font.Font(None, size)

def boucle_jeu(score):

    # Set up the display
    width, height = 1000, 800

    # ----------------------------------- Récupérer la valeur dans Screen_Stats.txt ----------------------------- #
    try:
        with open("Save_Stats/Screen_Stats.txt", "r") as f:
            screen_image_state = int(f.read())
    except FileNotFoundError:
        screen_image_state = 1

    if screen_image_state == 1:
        screen_size = (width, height)
        screen_flags = pygame.FULLSCREEN
    else:
        screen_size = (width, height)
        screen_flags = 0

    # Création de la surface d'écran
    screen = pygame.display.set_mode(screen_size, screen_flags)

    # pour les fps
    clock = pygame.time.Clock()

    # chargement du background déroulant
    bg = pygame.image.load("assets/background_game.png").convert()
    bg_y=0
    scroll_speed= 2.5

    # Chargement du vaisseau par default 
    default_vaisseau = pygame.image.load("assets/vaisseau/vaisseau_08.png").convert_alpha()

    # Chargement des enemies ( image )
    enemy_image = pygame.image.load("assets/enemy/enemy.png").convert_alpha()
    enemy_alt_image = pygame.image.load("assets/enemy/enemy_alt.png").convert_alpha()
    # Chargement du boost shield ( image )
    boost_shield_image = pygame.image.load("assets/Boost/boost_shield.png").convert_alpha()
    # Chargement du boost rocket ( image )
    boost_rocket_image = pygame.image.load("assets/Boost/boost_rocket.png").convert_alpha()

    vaisseau_05_shield_image = pygame.image.load("assets/vaisseau/Shield/Vaisseau_07/shield_00.png").convert_alpha()
    player_size = (80,80)
    vaisseau_05_shield_image = pygame.transform.scale(vaisseau_05_shield_image,player_size)

    # Player Gold
    gold = get_gold()

    # player Skin
    skin1 = True
    skin2 = False
    skin3 = False
    skin4 = False
    skin5 = False
    skin6 = False
    skin7 = False
    skin8 = False

    # font pour le score, skills et gold
    font = pygame.font.SysFont(None, 24)

    # Chargement de la barre de vie
    life_bar_image = pygame.image.load("assets/barre_vie/LifeBarFull.png").convert_alpha()
    life_bar_image1hit = pygame.image.load("assets/barre_vie/LifeBar1hit.png").convert_alpha()
    life_bar_image2hit = pygame.image.load("assets/barre_vie/LifeBar2hit.png").convert_alpha()
    life_bar_image3hit = pygame.image.load("assets/barre_vie/LifeBar3hit.png").convert_alpha()
    life_bar_image4hit = pygame.image.load("assets/barre_vie/LifeBar4hit.png").convert_alpha()
    life_bar_imageDead = pygame.image.load("assets/barre_vie/LifeBarDead.png").convert_alpha()
    life_bar_imageShield = pygame.image.load("assets/barre_vie_boss/LifeBarShield.png").convert_alpha()
    life_bar_imageFull = life_bar_image

    # Stats de la barre de vie
    life_bar_size = (200,75)
    life_bar_image = pygame.transform.scale(life_bar_image,life_bar_size)
    life_bar_rect = life_bar_image.get_rect()
    life_bar_rect.left = 10
    life_bar_rect.top = 10
    player_pv = 25

    # Chargement de la pos du vaisseau quand on lance le jeu
    player_size = (20,80)
    default_vaisseau = pygame.transform.scale(default_vaisseau,player_size)
    player_rect = default_vaisseau.get_rect()
    player_rect.centerx = width // 2
    player_rect.bottom = height - 25
    player_speed = 7

    # Bullets Speed
    bullet_speed = 10
    w_skill_bullet_speed = 5

    # anim bullet quand le bullet touche l'ennemi
    missile_exlposion = displayable("assets/skill_arme/explosion_anim",100)
    explo_size = missile_exlposion.image.get_size()

    # Stats pour les q skills
    skill_bullet_list = []
    skill_bullet_speed = 20
    q_cooldown = 0
    a_cooldown = 0
    new_a_cooldown = 100
    new_a_cooldown_rt = 100

    # Stats pour les petits ennemies
    enemy_size = (40,40)
    enemy_image = pygame.transform.scale(enemy_image, enemy_size)
    enemy_list = []
    enemy_speed = 5
    enemy_spawn_rate = 60
    enemy_spawn_counter = 60

    # Stats pour les gros ennemies
    enemy_alt_size = (80,80)
    enemy_alt_image = pygame.transform.scale(enemy_alt_image, enemy_alt_size)
    enemy_alt_list = []
    enemy_alt_speed = 1
    enemy_alt_spawn_rate = 300
    enemy_alt_spawn_counter = 300
    enemy_alt_life = 3

    # Stats pour le boost shield
    boost_shield_size = (80,80)
    boost_shield_image = pygame.transform.scale(boost_shield_image, boost_shield_size)
    boost_shield_list = []
    boost_shield_speed = 1
    boost_shield_spawn_rate = 500
    boost_shield_spawn_counter = 300
    cooldown_text = True
    shield_attraper = False
    spell_pressed = False

    # Stats pour le boost rocket
    boost_rocket_size = (40,40)
    boost_rocket_image = pygame.transform.scale(boost_rocket_image, boost_rocket_size)
    boost_rocket_list = []
    boost_rocket_speed = 1
    boost_rocket_spawn_rate = 500
    boost_rocket_spawn_counter = 300
    cooldown_text_rocket = True
    rocket_attraper = False
    actif_tir_rocket = None
    skin_rocket = False
    skin_rocket2 = False
    skin_rocket3 = False
    skin_rocket4 = False
    skin_rocket5 = False
    skin_rocket6 = False
    skin_rocket7 = False
    skin_rocket8 = False
    skin_rocket9 = False
    skin_rocket10 = False
    skin_rocket11 = False
    skin_rocket12 = False
    nb_rocket = 6
    actif_spell_rocket = False

    # quand le joueur a le score suffisant pour faire spawn le boss
    spawn_boss_actif = False
    keys_enabled = True
    transition_alpha = 0

    # Fonction pour mettre à jour la barre de vie
    def update_life_bar(x):
        x = pygame.transform.scale(x,life_bar_size)
        screen.blit(x, life_bar_rect)
        return int(0)
    
    # Chargement des sons
    sound_shoot_file = "assets/music/shoot_espace.mp3"
    sound_shoot = pygame.mixer.Sound(sound_shoot_file)
    sound_shoot.set_volume(0.1)

    sound_laser_file = "assets/music/laser_sound.mp3"
    sound_laser = pygame.mixer.Sound(sound_laser_file)
    sound_laser.set_volume(0.2)

    sound_rocket_file = "assets/music/rocket_sound.mp3"
    sound_rocket = pygame.mixer.Sound(sound_rocket_file)
    sound_rocket.set_volume(0.2)

    sound_shield_file = "assets/music/shield_sound.mp3"
    sound_shield = pygame.mixer.Sound(sound_shield_file)
    sound_shield.set_volume(0.2)

    # index pour les animations des vaisseaux et skills
    index_vaisseau = 0
    index_skill = 0
    bullet_index = 0
    w_skill_bullet_index = 0
    index_shield = 0
    index_rocket_boost = 0
    index_rocket2_boost = 0

    # Liste des balles
    bullet_list = []
    bullet_index_list = []
    # Liste du w skill
    w_skill_bullet_list = []
    w_skill_bullet_index_list = []

    # Boucle principal du jeu
    running_boucle_game = True
    while running_boucle_game:
        # récupére l'index du shop pour load le bon vaisseau du joueur
        selected_option = get_selected_option()
        if selected_option == 'Skin 2':
            skin2 = True
            skin1 = False    
        if selected_option == 'Skin 3':
            skin3 = True
            skin1 = False
        if selected_option == 'Skin 4':
            skin4 = True
            skin1 = False
        if selected_option == 'Skin 5':
            skin5 = True
            skin1 = False           
        if selected_option == 'Skin 6':
            skin6 = True
            skin1 = False 
        if selected_option == 'Skin 7':
            skin7 = True
            skin1 = False
        if selected_option == 'Skin 8':
            skin8 = True
            skin1 = False
            
        # reset les stats quand la game ce relance
        while player_pv <= 0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        running = True
                        player_pv = 25
                        score = 0
                        enemy_list = []
                        enemy_alt_list = []
                        bullet_list = []
                        skill_bullet_list = []
                        q_cooldown = 0
                        a_cooldown = 600
                        new_a_cooldown = 0
                        new_a_cooldown_rt = 0
                        life_bar_image = life_bar_imageFull
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        exit()
                    # Set up the game over message
                    game_over_text = font.render("Game Over", True, (255, 0, 0))
                    game_over_rect = game_over_text.get_rect(center=(width/2, height/2-20))
                    screen.blit(game_over_text, game_over_rect)
                    
                    final_score_text = font.render("Score final: " + str(score), True, (255, 255, 255))
                    final_score_rect = final_score_text.get_rect(center=(width/2, height/2+20))
                    screen.blit(final_score_text, final_score_rect)
                    
                    restart_text = font.render("Appuyez sur Entrée pour rejouer ou sur Echap pour quitter", True, (255, 255, 255))
                    restart_rect = restart_text.get_rect(center=(width/2, height/2+60))
                    screen.blit(restart_text, restart_rect)
                    
                    pygame.display.flip()
                    clock.tick(60)

        # events touche
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_boucle_game = False
            elif event.type == pygame.ACTIVEEVENT:
                if event.gain == 1:
                    if screen_image_state == 1:
                        screen_size = (width, height)
                        screen_flags = pygame.FULLSCREEN
                    else:
                        screen_size = (width, height)
                        screen_flags = 0
                    # Mise à jour de la surface d'écran
                    screen = pygame.display.set_mode(screen_size, screen_flags)
            elif event.type == pygame.KEYDOWN:
                if keys_enabled:
                    if event.key == pygame.K_SPACE:
                        sound_shoot.play()
                        # Tire de balles
                        bullet_rect = bullet_image[0].get_rect()
                        bullet_rect.centerx = player_rect.centerx + 30
                        bullet_rect.bottom = player_rect.top + 40
                        bullet_list.append(bullet_rect)
                        bullet_index_list.append(0)
                if event.key == pygame.K_q:
                    if q_cooldown == 0:
                        # skill laser
                        sound_laser.play()
                        skill_bullet_rect = image_beam.get_rect()
                        skill_bullet_rect.centerx = player_rect.centerx+30
                        skill_bullet_rect.bottom = player_rect.top+30
                        skill_bullet_list.append(skill_bullet_rect)
                        q_cooldown = 600
                if keys_enabled:
                    if event.key == pygame.K_w and actif_tir_rocket == True:
                        sound_rocket.play()
                        # skill rocket avec les load de vaisseau à chaque rocket
                        actif_spell_rocket = True
                        cooldown_text_rocket = False
                        if nb_rocket == 6:
                            w_skill_bullet_rect = w_skill_bullet_image[0].get_rect()
                            w_skill_bullet_rect.centerx = player_rect.centerx + 40
                            w_skill_bullet_rect.bottom = player_rect.top + 50
                            w_skill_bullet_list.append(w_skill_bullet_rect)
                            w_skill_bullet_index_list.append(0)
                            skin_rocket = True
                        if nb_rocket == 5:
                            w_skill_bullet_rect = w_skill_bullet_image[0].get_rect()
                            w_skill_bullet_rect.centerx = player_rect.centerx + 20
                            w_skill_bullet_rect.bottom = player_rect.top + 50
                            w_skill_bullet_list.append(w_skill_bullet_rect)
                            w_skill_bullet_index_list.append(0)
                            skin_rocket2 = True
                        if nb_rocket == 4:
                            w_skill_bullet_rect = w_skill_bullet_image[0].get_rect()
                            w_skill_bullet_rect.centerx = player_rect.centerx + 47
                            w_skill_bullet_rect.bottom = player_rect.top + 50
                            w_skill_bullet_list.append(w_skill_bullet_rect)
                            w_skill_bullet_index_list.append(0)
                            skin_rocket5 = True
                        if nb_rocket == 3:
                            w_skill_bullet_rect = w_skill_bullet_image[0].get_rect()
                            w_skill_bullet_rect.centerx = player_rect.centerx + 13
                            w_skill_bullet_rect.bottom = player_rect.top + 50
                            w_skill_bullet_list.append(w_skill_bullet_rect)
                            w_skill_bullet_index_list.append(0)
                            skin_rocket7 = True
                        if nb_rocket == 2:
                            w_skill_bullet_rect = w_skill_bullet_image[0].get_rect()
                            w_skill_bullet_rect.centerx = player_rect.centerx + 56
                            w_skill_bullet_rect.bottom = player_rect.top + 50
                            w_skill_bullet_list.append(w_skill_bullet_rect)
                            w_skill_bullet_index_list.append(0)
                            skin_rocket9 = True
                        if nb_rocket == 1:
                            w_skill_bullet_rect = w_skill_bullet_image[0].get_rect()
                            w_skill_bullet_rect.centerx = player_rect.centerx + 7
                            w_skill_bullet_rect.bottom = player_rect.top + 50
                            w_skill_bullet_list.append(w_skill_bullet_rect)
                            w_skill_bullet_index_list.append(0)
                            skin_rocket11 = True
                        nb_rocket -= 1
                        if nb_rocket <= 0:
                            rocket_attraper = False
                            actif_tir_rocket = False
                            cooldown_text_rocket = True
                            nb_rocket = 6
                    else:
                        actif_spell_rocket = False

        # ------------------------------------------- Mouvements des balles + des enemies + des skills --------------------------------- #
        for bullet_rect in bullet_list:
            bullet_rect.move_ip(0, -bullet_speed)

        for w_skill_bullet_rect in w_skill_bullet_list:
            w_skill_bullet_rect.move_ip(0, -w_skill_bullet_speed)
        
        for skill_bullet_rect in skill_bullet_list:
            skill_bullet_rect.move_ip(0, -skill_bullet_speed)

        for enemy_rect in enemy_list:
            enemy_rect.move_ip(0, enemy_speed)
        
        for enemy_alt_rect in enemy_alt_list:
            enemy_alt_rect.move_ip(0,enemy_alt_speed)

        for boost_shield_rect in boost_shield_list:
            boost_shield_rect.move_ip(0, boost_shield_speed)

        for boost_rocket_rect in boost_rocket_list:
            boost_rocket_rect.move_ip(0, boost_rocket_speed)

        # ------------------------------------------- Fin des Mouvements des balles + des enemies + des skills --------------------------------- #

        # dessine le background et le joueur avec le bon vaisseau
        screen.fill((0, 0, 0))
        screen.blit(bg,(0,0))
        if skin1 == True:
            screen.fill((0, 0, 0))
            bg_y+=scroll_speed
            if bg_y>bg.get_height():
                bg_y=0
            screen.blit(bg, (0,bg_y))
            screen.blit(bg,(0,bg_y-bg.get_height())) 
            screen.blit(vaisseau_1[index_vaisseau], player_rect)
            # Passer à l'image suivante de l'animation
            index_vaisseau += 1
            if index_vaisseau >= len(vaisseau_1):
                index_vaisseau = 0
        elif skin2 == True:
            screen.fill((0, 0, 0))
            bg_y+=scroll_speed
            if bg_y>bg.get_height():
                bg_y=0
            screen.blit(bg, (0,bg_y))
            screen.blit(bg,(0,bg_y-bg.get_height()))            
            screen.blit(vaisseau_2[index_vaisseau], player_rect)
            # Passer à l'image suivante de l'animation
            index_vaisseau += 1
            if index_vaisseau >= len(vaisseau_2):
                index_vaisseau = 0
        elif skin3 == True:
            screen.fill((0, 0, 0))
            bg_y+=scroll_speed
            if bg_y>bg.get_height():
                bg_y=0
            screen.blit(bg, (0,bg_y))
            screen.blit(bg,(0,bg_y-bg.get_height()))            
            screen.blit(vaisseau_3[index_vaisseau], player_rect)
            # Passer à l'image suivante de l'animation
            index_vaisseau += 1
            if index_vaisseau >= len(vaisseau_3):
                index_vaisseau = 0
        elif skin4 == True:
            screen.fill((0, 0, 0))
            bg_y+=scroll_speed
            if bg_y>bg.get_height():
                bg_y=0
            screen.blit(bg, (0,bg_y))
            screen.blit(bg,(0,bg_y-bg.get_height()))            
            screen.blit(vaisseau_4[index_vaisseau], player_rect)
            # Passer à l'image suivante de l'animation
            index_vaisseau += 1
            if index_vaisseau >= len(vaisseau_4):
                index_vaisseau = 0
        elif skin5 == True:
            screen.fill((0, 0, 0))
            bg_y+=scroll_speed
            if bg_y>bg.get_height():
                bg_y=0
            screen.blit(bg, (0,bg_y))
            screen.blit(bg,(0,bg_y-bg.get_height()))            
            screen.blit(vaisseau_5[index_vaisseau], player_rect)
            # Passer à l'image suivante de l'animation
            index_vaisseau += 1
            if index_vaisseau >= len(vaisseau_5):
                index_vaisseau = 0
        elif skin6 == True:
            screen.fill((0, 0, 0))
            bg_y+=scroll_speed
            if bg_y>bg.get_height():
                bg_y=0
            screen.blit(bg, (0,bg_y))
            screen.blit(bg,(0,bg_y-bg.get_height()))            
            screen.blit(vaisseau_6[index_vaisseau], player_rect)
            # Passer à l'image suivante de l'animation
            index_vaisseau += 1
            if index_vaisseau >= len(vaisseau_6):
                index_vaisseau = 0
        elif skin7 == True:
            screen.fill((0, 0, 0))
            bg_y+=scroll_speed
            if bg_y>bg.get_height():
                bg_y=0
            screen.blit(bg, (0,bg_y))
            screen.blit(bg,(0,bg_y-bg.get_height()))            
            screen.blit(vaisseau_7[index_vaisseau], player_rect)
            # Passer à l'image suivante de l'animation
            index_vaisseau += 1
            if index_vaisseau >= len(vaisseau_7):
                index_vaisseau = 0
        elif skin8 == True:
            screen.fill((0, 0, 0))
            bg_y+=scroll_speed
            if bg_y>bg.get_height():
                bg_y=0
            screen.blit(bg, (0,bg_y))
            screen.blit(bg,(0,bg_y-bg.get_height()))            
            screen.blit(vaisseau_8[index_vaisseau], player_rect)
            # Passer à l'image suivante de l'animation
            index_vaisseau += 1
            if index_vaisseau >= len(vaisseau_8):
                index_vaisseau = 0
        if skin_rocket == True:          
            screen.blit(vaisseau_06_rocket_image[index_rocket_boost], player_rect)
            # Passer à l'image suivante de l'animation
            index_rocket_boost += 1
            if index_rocket_boost >= 5 :
                skin_rocket = False
                skin_rocket3 = True
            if index_rocket_boost >= len(vaisseau_06_rocket_image):
                index_rocket_boost = 0
        if skin_rocket3 == True:
            screen.blit(vaisseau_06_rocket_image[5], player_rect)
        if skin_rocket2 == True:      
            screen.blit(vaisseau_06_rocket2_image[index_rocket2_boost], player_rect)
            # Passer à l'image suivante de l'animation
            index_rocket2_boost += 1
            if index_rocket2_boost >= 2:
                skin_rocket2 = False
                skin_rocket3 = False
                skin_rocket4 = True
            if index_rocket2_boost >= len(vaisseau_06_rocket2_image):
                index_rocket2_boost = 0
        if skin_rocket4 == True:
            screen.blit(vaisseau_06_rocket2_image[1], player_rect)
        if skin_rocket5 == True:      
            screen.blit(vaisseau_06_rocket3_image[index_rocket2_boost], player_rect)
            # Passer à l'image suivante de l'animation
            index_rocket2_boost += 1
            if index_rocket2_boost >= 2:
                skin_rocket5 = False
                skin_rocket4 = False
                skin_rocket6 = True
            if index_rocket2_boost >= len(vaisseau_06_rocket3_image):
                index_rocket2_boost = 0
        if skin_rocket6 == True:
            screen.blit(vaisseau_06_rocket3_image[1], player_rect)
        if skin_rocket7 == True:      
            screen.blit(vaisseau_06_rocket4_image[index_rocket2_boost], player_rect)
            # Passer à l'image suivante de l'animation
            index_rocket2_boost += 1
            if index_rocket2_boost >= 2:
                skin_rocket7 = False
                skin_rocket6 = False
                skin_rocket8 = True
            if index_rocket2_boost >= len(vaisseau_06_rocket4_image):
                index_rocket2_boost = 0
        if skin_rocket8 == True:
            screen.blit(vaisseau_06_rocket4_image[1], player_rect)
        if skin_rocket9 == True:      
            screen.blit(vaisseau_06_rocket5_image[index_rocket2_boost], player_rect)
            # Passer à l'image suivante de l'animation
            index_rocket2_boost += 1
            if index_rocket2_boost >= 2:
                skin_rocket9 = False
                skin_rocket8 = False
                skin_rocket10 = True
            if index_rocket2_boost >= len(vaisseau_06_rocket5_image):
                index_rocket2_boost = 0
        if skin_rocket10 == True:
            screen.blit(vaisseau_06_rocket5_image[1], player_rect)
        if skin_rocket11 == True:
            screen.blit(vaisseau_06_rocket6_image[index_rocket2_boost], player_rect)
            # Passer à l'image suivante de l'animation
            index_rocket2_boost += 1
            if index_rocket2_boost >= 2:
                skin_rocket11 = False
                skin_rocket10 = False
                skin_rocket12 = True
            if index_rocket2_boost >= len(vaisseau_06_rocket6_image):
                index_rocket2_boost = 0
        if skin_rocket12 == True:
            screen.blit(vaisseau_06_rocket6_image[1], player_rect)


        # Mouvement du joueur
        if keys_enabled:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and player_rect.left > 0:
                player_rect.move_ip(-player_speed, 0)
            if keys[pygame.K_RIGHT] and player_rect.right < width:
                player_rect.move_ip(player_speed, 0)
            if keys[pygame.K_UP] and player_rect.top > 0:
                player_rect.move_ip(0, -player_speed)
            if keys[pygame.K_DOWN] and player_rect.bottom < height:
                player_rect.move_ip(0, player_speed)

        # Spawn des ennemies
        if not spawn_boss_actif:
            enemy_spawn_counter += 2
            if enemy_spawn_counter >= enemy_spawn_rate:
                enemy_rect = enemy_image.get_rect()
                enemy_rect.centerx = random.randint(0, width)
                enemy_rect.top = -enemy_rect.height
                enemy_list.append(enemy_rect)
                enemy_spawn_counter = 0
            
            enemy_alt_spawn_counter += 1
            if enemy_alt_spawn_counter >= enemy_alt_spawn_rate:
                enemy_alt_rect = enemy_alt_image.get_rect()
                enemy_alt_rect.centerx = random.randint(0, width)
                enemy_alt_rect.top = -enemy_alt_rect.height
                enemy_alt_list.append(enemy_alt_rect)
                enemy_alt_spawn_counter = 0

        # Spawn du Boss en fonction du score
        if score >= 50 and score <= 54:
            spawn_boss_actif = True
            keys_enabled = False
            transition_alpha = min(255, transition_alpha + 2)
            if transition_alpha > 255:
                transition_alpha = 255
            transition_surface = pygame.Surface((1920, 1080))
            transition_surface.set_alpha(transition_alpha)
            screen.blit(transition_surface, (0, 0))
            BOSS_TEXT = get_font(40).render("Alien Assault présente le premier Boss du mode Infinie", True, "#FFB833")
            BOSS_RECT = BOSS_TEXT.get_rect(center=(width // 2, height // 2))
            screen.blit(BOSS_TEXT, BOSS_RECT)
            if transition_alpha == 255:
                life_bar_image = life_bar_imageFull
                combat_boss(score)

        # -------------------------------------------- Spawns des skills Shield + Rocket -------------------------------------- #
        boost_shield_spawn_counter += 1
        if boost_shield_spawn_counter >= boost_shield_spawn_rate:
            boost_shield_rect = boost_shield_image.get_rect()
            boost_shield_rect.centerx = random.randint(0, width)
            boost_shield_rect.top = -boost_shield_rect.height
            boost_shield_list.append(boost_shield_rect)
            boost_shield_spawn_counter = 0

        for boost_shield_rect in boost_shield_list:
            if player_rect.colliderect(boost_shield_rect):
                boost_shield_list.remove(boost_shield_rect)
                shield_attraper = True

        boost_rocket_spawn_counter += 1
        if boost_rocket_spawn_counter >= boost_rocket_spawn_rate and skin6 == True:
            boost_rocket_rect = boost_rocket_image.get_rect()
            boost_rocket_rect.centerx = random.randint(0, width)
            boost_rocket_rect.top = -boost_rocket_rect.height
            boost_rocket_list.append(boost_rocket_rect)
            boost_rocket_spawn_counter = 0

        # -------------------------------------------- Fin des Spawns des skills Shield + Rocket -------------------------------------- #

        # -------------------------------------------- Gestion des récompenses quand le joueur tue l'ennemi -------------------------------------- #
        for bullet_rect in bullet_list:
            for enemy_rect in enemy_list:
                if bullet_rect.colliderect(enemy_rect):
                    temp_enemy_rect = (enemy_rect[0] - explo_size[0]/4, enemy_rect[1] - explo_size[1]/4,enemy_rect[2],enemy_rect[3])
                    enemy_list.remove(enemy_rect)
                    bullet_list.remove(bullet_rect)
                    score += 1
                    gold = int(gold)+1
                    with open("./Save_Stats/Player_Gold.txt", "w") as f:
                        f.write(str(gold))
                    screen.blit(missile_exlposion.image,temp_enemy_rect)
        for bullet_rect in bullet_list:
            for enemy_rect in enemy_alt_list:
                if bullet_rect.colliderect(enemy_rect):
                    temp_enemy_rect = (enemy_rect[0] - explo_size[0]/4, enemy_rect[1] - explo_size[1]/4,enemy_rect[2],enemy_rect[3])
                    enemy_alt_life-=1
                    bullet_list.remove(bullet_rect)
                    screen.blit(missile_exlposion.image,temp_enemy_rect)
                    if actif_spell_rocket:
                        enemy_alt_list.remove(enemy_rect)
                        score += 3
                        gold = int(gold)+3
                        enemy_alt_life = 3
                        with open("./Save_Stats/Player_Gold.txt", "w") as f:
                            f.write(str(gold))
                    elif enemy_alt_life <= 0:
                        enemy_alt_list.remove(enemy_rect)
                        score += 3
                        gold = int(gold)+3
                        enemy_alt_life = 3
                        with open("./Save_Stats/Player_Gold.txt", "w") as f:
                            f.write(str(gold))
        for w_skill_bullet_rect in w_skill_bullet_list:
            for enemy_rect in enemy_list:
                if w_skill_bullet_rect.colliderect(enemy_rect):
                    temp_enemy_rect = (enemy_rect[0] - explo_size[0]/4, enemy_rect[1] - explo_size[1]/4,enemy_rect[2],enemy_rect[3])
                    enemy_list.remove(enemy_rect)
                    w_skill_bullet_list.remove(w_skill_bullet_rect)
                    score += 1
                    gold = int(gold)+1
                    with open("./Save_Stats/Player_Gold.txt", "w") as f:
                        f.write(str(gold))
                    screen.blit(missile_exlposion.image,temp_enemy_rect)
        for w_skill_bullet_rect in w_skill_bullet_list:
            for enemy_rect in enemy_alt_list:
                if w_skill_bullet_rect.colliderect(enemy_rect):
                    temp_enemy_rect = (enemy_rect[0] - explo_size[0]/4, enemy_rect[1] - explo_size[1]/4,enemy_rect[2],enemy_rect[3])
                    enemy_alt_life-=1
                    w_skill_bullet_list.remove(w_skill_bullet_rect)
                    screen.blit(missile_exlposion.image,temp_enemy_rect)
                    if actif_spell_rocket:
                        enemy_alt_list.remove(enemy_rect)
                        score += 3
                        gold = int(gold)+3
                        enemy_alt_life = 3
                        with open("./Save_Stats/Player_Gold.txt", "w") as f:
                            f.write(str(gold))
                    elif enemy_alt_life <= 0:
                        enemy_alt_list.remove(enemy_rect)
                        score += 3
                        gold = int(gold)+3
                        enemy_alt_life = 3
                        with open("./Save_Stats/Player_Gold.txt", "w") as f:
                            f.write(str(gold))
        for skill_bullet_rect in skill_bullet_list:
            for mob_rect in enemy_list:
                if skill_bullet_rect.colliderect(mob_rect):
                    temp_enemy_rect = (enemy_rect[0] - explo_size[0]/4, enemy_rect[1] - explo_size[1]/4,enemy_rect[2],enemy_rect[3])
                    enemy_list.remove(mob_rect)
                    score += 1
                    gold = int(gold)+1
                    with open("./Save_Stats/Player_Gold.txt", "w") as f:
                        f.write(str(gold))
                    screen.blit(missile_exlposion.image,temp_enemy_rect)
        for skill_bullet_rect in skill_bullet_list:
            for mob_rect in enemy_alt_list:
                if skill_bullet_rect.colliderect(mob_rect):
                    temp_enemy_rect = (enemy_rect[0] - explo_size[0]/4, enemy_rect[1] - explo_size[1]/4,enemy_rect[2],enemy_rect[3])
                    enemy_alt_list.remove(mob_rect)
                    score += 3
                    gold = int(gold)+3
                    with open("./Save_Stats/Player_Gold.txt", "w") as f:
                        f.write(str(gold))
                    screen.blit(missile_exlposion.image,temp_enemy_rect)
        # -------------------------------------------- Fin de la Gestion des récompenses quand le joueur tue l'ennemi -------------------------------------- #
        
        # -------------------------------------------- Gestion du Skill Shield [a] avec le load des différents skins -------------------------------------- #
        if keys_enabled:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a] and cooldown_text == False:
                sound_shield.play()
                spell_pressed = True
                screen.fill((0, 0, 0))            
                if bg_y>bg.get_height():
                    bg_y=0
                screen.blit(bg, (0,bg_y))
                screen.blit(bg,(0,bg_y-bg.get_height()))                                  
                # screen.blit(shield_image, player_rect)
                if skin1:
                    screen.blit(vaisseau_01_shield_image[index_vaisseau], player_rect)
                if skin2:
                    screen.blit(vaisseau_02_shield_image[index_vaisseau], player_rect)
                if skin3:
                    screen.blit(vaisseau_03_shield_image[index_shield], player_rect)
                if skin5:
                    screen.blit(vaisseau_05_shield_image, player_rect)
                if skin6:
                    screen.blit(vaisseau_06_shield_image[index_vaisseau], player_rect)
                if skin7:
                    screen.blit(vaisseau_07_shield_image[index_vaisseau], player_rect)
                # Passer à l'image suivante de l'animation
                if index_shield >= len(vaisseau_03_shield_image):
                    index_shield = 0
                new_a_cooldown -= 0.1
            else:
                spell_pressed = False
                sound_shield.stop()
        # -------------------------------------------- Fin de la Gestion du Skill Shield [a] -------------------------------------- #

        # -------------------------------------------- Affichages des textes pour les différents skills -------------------------------------- #
        if cooldown_text == False:
            new_a_cooldown_rt = round(new_a_cooldown/1)
            a_skill_text = font.render("Shield Restant: " + str(new_a_cooldown_rt) + "%", True, (255,0,0))
            a_skill_rect = a_skill_text.get_rect(center=(220,height-20))
            screen.blit(a_skill_text, a_skill_rect)
        if new_a_cooldown >= -1 and new_a_cooldown <= 0:
            shield_attraper = False
            cooldown_text = True
        if new_a_cooldown <= 0 and shield_attraper == False:
            a_cooldown = 600
            new_a_cooldown = 100
            new_a_cooldown_rt = 100

        if cooldown_text_rocket == False:
            a_skill_text_rocket = font.render("Nombre de Rockets:" + str(nb_rocket), True, (255,0,0))
            a_skill_rect_rocket = a_skill_text_rocket.get_rect(center=(400,height-20))
            screen.blit(a_skill_text_rocket, a_skill_rect_rocket)

        # -------------------------------------------- Fin des Affichages des textes pour les différents skills -------------------------------------- #


        # -------------------------------------------- Gestion des collisions des skills et entre le joueur et l'ennemi -------------------------------------- #
        for boost_rocket_rect in boost_rocket_list:
            if player_rect.colliderect(boost_rocket_rect):
                boost_rocket_list.remove(boost_rocket_rect)
                rocket_attraper = True

        # Detect collisions player
        for enemy_rect in enemy_list:
            if player_rect.colliderect(enemy_rect):
                enemy_list.remove(enemy_rect)
                if spell_pressed:
                    pass
                else:
                    player_pv -= 5
        
        for enemy_alt_rect in enemy_alt_list:
            if player_rect.colliderect(enemy_alt_rect):
                enemy_alt_list.remove(enemy_alt_rect)
                if spell_pressed:
                    pass
                else:
                    player_pv -= 10

        # -------------------------------------------- Fin de la Gestion des collisions des skills et entre le joueur et l'ennemi -------------------------------------- #
                
        # -------------------------------------------- Affichages de l'annimation des bullets + skills quand le joueur tire -------------------------------------- #
        for bullet_rect, bullet_index in zip(bullet_list, bullet_index_list):
            screen.blit(bullet_image[bullet_index], bullet_rect)

            # Passer à l'image suivante de l'animation
            bullet_index += 1
            if bullet_index >= len(bullet_image):
                bullet_index = 0
            bullet_index_list[bullet_list.index(bullet_rect)] = bullet_index

        for w_skill_bullet_rect in w_skill_bullet_list:
            screen.blit(w_skill_bullet_image[w_skill_bullet_index], w_skill_bullet_rect)
            # Passer à l'image suivante de l'animation
            w_skill_bullet_index += 1
            if w_skill_bullet_index >= len(w_skill_bullet_image):
                w_skill_bullet_index = 0

        for skill_bullet_rect in skill_bullet_list:
            screen.blit(beam_image[index_skill], skill_bullet_rect)
            # Passer à l'image suivante de l'animation
            index_skill += 1
            if index_skill >= len(beam_image):
                index_skill = 0
        # -------------------------------------------- Fin des Affichages de l'annimation des bullets + skills quand le joueur tire -------------------------------------- #
            
        # -------------------------------------------- Affichage des 2 type d'ennemies + le boost shield et rocket -------------------------------------- #
        for enemy_rect in enemy_list:
            if keys_enabled:
                screen.blit(enemy_image, enemy_rect)
            
        for enemy_alt_rect in enemy_alt_list:
            if keys_enabled:
                screen.blit(enemy_alt_image, enemy_alt_rect)

        for boost_shield_rect in boost_shield_list:
            if keys_enabled:
                if skin1 == True or skin2 == True or skin3 == True or skin5 == True or skin6 == True or skin7 == True:
                    screen.blit(boost_shield_image, boost_shield_rect)
                else:
                    pass

        for boost_rocket_rect in boost_rocket_list:
            if keys_enabled:
                screen.blit(boost_rocket_image, boost_rocket_rect)
        # -------------------------------------------- Fin de l'affichage des 2 type d'ennemies + le boost shield et rocket -------------------------------------- #
            
        # -------------------------------------------- Affichage des textes score + gold -------------------------------------- #
        score_text = font.render("Score: " + str(score), True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(width/2,20))
        screen.blit(score_text, score_rect)

        gold_text = font.render("Gold: " + str(gold), True, (255, 255, 255))
        gold_rect = gold_text.get_rect(center=(900,10))
        screen.blit(gold_text, gold_rect)
        
        # -------------------------------------------- Mise à jour de la barre de vie du joueur -------------------------------------- #
        if not spell_pressed:
            if player_pv >= 25:
                life_bar_image = life_bar_imageFull
                update_life_bar(life_bar_image)
            elif player_pv >= 20:
                life_bar_image = life_bar_image1hit
                update_life_bar(life_bar_image)
            elif player_pv >= 15:
                life_bar_image = life_bar_image2hit
                update_life_bar(life_bar_image)
            elif player_pv >= 10:
                life_bar_image = life_bar_image3hit  
                update_life_bar(life_bar_image)
            elif player_pv >= 5:
                life_bar_image = life_bar_image4hit
                update_life_bar(life_bar_image)
            elif player_pv <= 0:
                life_bar_image = life_bar_imageDead
                update_life_bar(life_bar_image)
        else:
            # Si le skill du shield est activé alors affiche une barre de vie spécial
            life_bar_image = life_bar_imageShield
            update_life_bar(life_bar_image)

        # -------------------------------------------- Affichages des cooldowns et des textes des différents skills -------------------------------------- #
        if q_cooldown > 0:
            q_cooldown_rt = round(q_cooldown/60)
            q_skill_text = font.render("Laser dans: " + str(q_cooldown_rt) + "s", True, (255,0,0))
            q_skill_rect = q_skill_text.get_rect(center=(70,height-20))
            screen.blit(q_skill_text, q_skill_rect)
            q_cooldown -= 1
            
        elif q_cooldown == 0:
            if keys_enabled:
                q_skill_text = font.render("Laser: q", True, (0,255,0))
                q_skill_rect = q_skill_text.get_rect(center=(70,height-20))
                screen.blit(q_skill_text, q_skill_rect)

        if shield_attraper == True:
            if a_cooldown >= 0 and cooldown_text == True and shield_attraper == True:
                a_cooldown_rt = round(a_cooldown/60)
                a_skill_text = font.render("Shield à: " + str(a_cooldown_rt) + "%", True, (255,0,0))
                a_skill_rect = a_skill_text.get_rect(center=(200,height-20))
                screen.blit(a_skill_text, a_skill_rect)
                a_cooldown += 5

            if a_cooldown_rt >= 100.0:
                cooldown_text = False

        if rocket_attraper == True:
            if cooldown_text_rocket == True:
                actif_tir_rocket = True
                a_skill_text_rocket = font.render("Nombre de Rockets:6", True, (255,0,0))
                a_skill_rect_rocket = a_skill_text_rocket.get_rect(center=(400,height-20))
                screen.blit(a_skill_text_rocket, a_skill_rect_rocket)

         # -------------------------------------------- Fin des Affichages des cooldowns et des textes des différents skills -------------------------------------- #

        pygame.display.flip()

        # Limiter la fréquence d'images
        clock.tick(60)
        
    pygame.quit()


 # -------------------------------------------- Début de la fonction pour gérer le combat de boss -------------------------------------- #
def combat_boss(score):

    # Définition de la taille de l'écran
    screen_width = 1000
    screen_height = 800

    # Lecture de l'état de l'image écran à partir du fichier
    try:
        with open("Save_Stats/Screen_Stats.txt", "r") as f:
            screen_image_state = int(f.read())
    except FileNotFoundError:
        screen_image_state = 1

    # Définition de la taille d'écran initiale
    if screen_image_state == 1:
        screen_size = (screen_width, screen_height)
        screen_flags = pygame.FULLSCREEN
    else:
        screen_size = (screen_width, screen_height)
        screen_flags = 0

    # Création de la surface d'écran
    screen = pygame.display.set_mode(screen_size, screen_flags)

    # Chargement de l'image du boss
    boss_image = pygame.image.load("assets/enemy/boss.png")

    # Chargement de l'image de la balle
    bullet_image = pygame.image.load("assets/bullet/bullet_00.png")
        
    # ----------------------------------- Récupérer la valeur dans Vaisseau.txt ----------------------------- #
    def get_selected_option():
        try:
            with open("./Save_Stats/Skin_Vaisseau.txt", "r") as f:
                return f.read().strip()
        except FileNotFoundError:
            return None
        
    # ----------------------------------------- Récupérer la barre de vie ------------------------------------ # 
    def update_life_bar(x):
        x = pygame.transform.scale(x,life_bar_size)
        screen.blit(x, life_bar_rect)
        return int(0)

    # ----------------------------------- Récupérer la valeur dans Player_Gold.txt ----------------------------- #
    def get_gold():
        try:
            with open("./Save_Stats/Player_Gold.txt", "r") as f:
                return f.read().strip()
        except FileNotFoundError:
            return None
        
    angle = 0
    bullet_speed = 1
    transition_alpha = 0

    sound_bullet_boss_file = "assets/music/boss_bullet.mp3"
    sound_bullet_boss = pygame.mixer.Sound(sound_bullet_boss_file)
    sound_bullet_boss.set_volume(0.1)

    def boss_shoot():
        sound_bullet_boss.play()
        bullet_x = boss_rect.centerx
        bullet_y = boss_rect.centery
        bullet_direction = math.atan2(player_rect.y - boss_rect.centery, player_rect.x - boss_rect.centerx)
        bullet_dx = bullet_speed * math.cos(bullet_direction)
        bullet_dy = bullet_speed * math.sin(bullet_direction)
        bullets.append([bullet_x, bullet_y, bullet_dx, bullet_dy])


    # Chargement the life bar sprite
    life_bar_image = pygame.image.load("assets/barre_vie_boss/LifeBarFull.png").convert_alpha()
    life_bar_image1hit = pygame.image.load("assets/barre_vie_boss/LifeBar1hit.png").convert_alpha()
    life_bar_image2hit = pygame.image.load("assets/barre_vie_boss/LifeBar2hit.png").convert_alpha()
    life_bar_image3hit = pygame.image.load("assets/barre_vie_boss/LifeBar3hit.png").convert_alpha()
    life_bar_image4hit = pygame.image.load("assets/barre_vie_boss/LifeBar4hit.png").convert_alpha()
    life_bar_image5hit = pygame.image.load("assets/barre_vie_boss/LifeBar5hit.png").convert_alpha()
    life_bar_image6hit = pygame.image.load("assets/barre_vie_boss/LifeBar6hit.png").convert_alpha()
    life_bar_image7hit = pygame.image.load("assets/barre_vie_boss/LifeBar7hit.png").convert_alpha()
    life_bar_imageDead = pygame.image.load("assets/barre_vie_boss/LifeBarDead.png").convert_alpha()
    life_bar_imageShield = pygame.image.load("assets/barre_vie_boss/LifeBarShield.png").convert_alpha()
    life_bar_imageFull = life_bar_image

    # Set up the life bar
    life_bar_size = (200,75)
    life_bar_image = pygame.transform.scale(life_bar_image,life_bar_size)
    life_bar_rect = life_bar_image.get_rect()
    life_bar_rect.left = 10
    life_bar_rect.top = 10
    player_pv = 40


    # Chargement the player sprite 
    default_vaisseau = pygame.image.load("assets/vaisseau/vaisseau_06.png").convert_alpha()
    # Set up the player
    player_size = (80,80)
    default_vaisseau = pygame.transform.scale(default_vaisseau,player_size)
    player_rect = default_vaisseau.get_rect()
    player_rect.centerx = width // 2
    player_rect.bottom = height - 25
    # player Skin
    skin1 = True
    skin2 = False
    skin3 = False
    skin4 = False
    skin5 = False
    skin6 = False
    skin7 = False
    skin8 = False
    # Définition de la position de départ du joueur
    player_x = 500
    player_y = 500
    # Définition de la position de départ du boss
    boss_x = 100
    boss_y = 200
    boss_rect = boss_image.get_rect()
    boss_rect.x = boss_x
    boss_rect.y = boss_y

    # Définition de la vitesse de déplacement du boss
    boss_speed_x = 0.1
    boss_speed_y = 0
    boss_health = 100
    bullets = []
    bullet_width = 10  # à remplacer par la largeur du projectile ennemi
    bullet_height = 10  # à remplacer par la hauteur du projectile ennemi
    bullet_speed_player = 3

    # Chargement Shield Boost image
    boost_shield_image = pygame.image.load("assets/Boost/boost_shield.png").convert_alpha()
    vaisseau_05_shield_image = pygame.image.load("assets/vaisseau/Shield/Vaisseau_07/shield_00.png").convert_alpha()
    player_size = (80,80)
    vaisseau_05_shield_image = pygame.transform.scale(vaisseau_05_shield_image,player_size)
    # Set up the shield boost
    boost_shield_size = (80,80)
    boost_shield_image = pygame.transform.scale(boost_shield_image, boost_shield_size)
    boost_shield_list = []
    boost_shield_speed = 1
    boost_shield_spawn_rate = 2000
    boost_shield_spawn_counter = 300
    cooldown_text = True
    shield_attraper = False
    shield_activer = False
    sound_shield_file = "assets/music/shield_sound.mp3"
    sound_shield = pygame.mixer.Sound(sound_shield_file)
    sound_shield.set_volume(0.2)
    index_shield = 0
    new_a_cooldown = 100
    new_a_cooldown_rt = 100
    a_cooldown = 0

    end_of_game = False

    # Chargement Rocket Boost image
    boost_rocket_image = pygame.image.load("assets/Boost/boost_rocket.png").convert_alpha()
    # Set up the rocket boost
    boost_rocket_size = (40,40)
    boost_rocket_image = pygame.transform.scale(boost_rocket_image, boost_rocket_size)
    boost_rocket_list = []
    boost_rocket_speed = 1
    boost_rocket_spawn_rate = 4000
    boost_rocket_spawn_counter = 750
    nb_rocket = 6
    cooldown_text_rocket = True
    rocket_attraper = False
    actif_tir_rocket = None
    skin_rocket = False
    skin_rocket2 = False
    skin_rocket3 = False
    skin_rocket4 = False
    skin_rocket5 = False
    skin_rocket6 = False
    skin_rocket7 = False
    skin_rocket8 = False
    skin_rocket9 = False
    skin_rocket10 = False
    skin_rocket11 = False
    skin_rocket12 = False
    w_skill_bullet_index = 0
    w_skill_bullet_speed = 2
    index_rocket_boost = 0
    index_rocket2_boost = 0
    # Liste du w skill
    w_skill_bullet_list = []
    w_skill_bullet_index_list = []
    sound_rocket_file = "assets/music/rocket_sound.mp3"
    sound_rocket = pygame.mixer.Sound(sound_rocket_file)
    sound_rocket.set_volume(0.2)

    # Chargement des sons
    sound_shoot_file = "assets/music/shoot_espace.mp3"
    sound_shoot = pygame.mixer.Sound(sound_shoot_file)
    sound_shoot.set_volume(0.1)

    # Chargement bullet custom
    bullet_image = []
    for i in range(0, 3):
        filename = os.path.join("assets/bullet", f"bullet_0{i}.png")
        image_bullet = pygame.image.load(filename)
        image_bullet = pygame.transform.scale(image_bullet, (25,75))
        bullet_image.append(image_bullet)

    # Chargement bullet custom
    boss_bullet_image = []
    for i in range(0, 5):
        filename = os.path.join("assets/boss_bullet", f"bullet_0{i}.png")
        image_boss_bullet = pygame.image.load(filename)
        image_boss_bullet = pygame.transform.scale(image_boss_bullet, (100,100))
        boss_bullet_image.append(image_boss_bullet)

    # Liste des balles
    bullet_list = []
    bullet_index_list = []
    boss_bullet_index_list = []
    #load background image
    bg_boss = pygame.image.load("assets/background_boss.png").convert()
    bg_y_boss=0
    scroll_speed_boss= 0.5
    index_vaisseau = 0
    bullet_index = 0
    index_boss_bullet = 0
    keys_enabled = True

    # Player Gold
    gold = get_gold()

    # Set up the score
    font = pygame.font.SysFont(None, 24)
    # Boucle principale du jeu
    running_bongo = True
    while running_bongo:
        selected_option = get_selected_option()
        if selected_option == 'Skin 2':
            skin2 = True
            skin1 = False    
        if selected_option == 'Skin 3':
            skin3 = True
            skin1 = False
        if selected_option == 'Skin 4':
            skin4 = True
            skin1 = False
        if selected_option == 'Skin 5':
            skin5 = True
            skin1 = False           
        if selected_option == 'Skin 6':
            skin6 = True
            skin1 = False 
        if selected_option == 'Skin 7':
            skin7 = True
            skin1 = False
        if selected_option == 'Skin 8':
            skin8 = True
            skin1 = False

        screen.fill((0, 0, 0))
        screen.blit(bg_boss,(0,0))
        if skin1 == True:
            screen.fill((0, 0, 0))
            bg_y_boss+=scroll_speed_boss
            if bg_y_boss>bg_boss.get_height():
                bg_y_boss=0
            screen.blit(bg_boss, (0,bg_y_boss))
            screen.blit(bg_boss,(0,bg_y_boss-bg_boss.get_height())) 
            screen.blit(vaisseau_1[index_vaisseau], player_rect)
            # Passer à l'image suivante de l'animation
            index_vaisseau += 1
            if index_vaisseau >= len(vaisseau_1):
                index_vaisseau = 0
        elif skin2 == True:
            screen.fill((0, 0, 0))
            bg_y_boss+=scroll_speed_boss
            if bg_y_boss>bg_boss.get_height():
                bg_y_boss=0
            screen.blit(bg_boss, (0,bg_y_boss))
            screen.blit(bg_boss,(0,bg_y_boss-bg_boss.get_height()))            
            screen.blit(vaisseau_2[index_vaisseau], player_rect)
            # Passer à l'image suivante de l'animation
            index_vaisseau += 1
            if index_vaisseau >= len(vaisseau_2):
                index_vaisseau = 0
        elif skin3 == True:
            screen.fill((0, 0, 0))
            bg_y_boss+=scroll_speed_boss
            if bg_y_boss>bg_boss.get_height():
                bg_y_boss=0
            screen.blit(bg_boss, (0,bg_y_boss))
            screen.blit(bg_boss,(0,bg_y_boss-bg_boss.get_height()))            
            screen.blit(vaisseau_3[index_vaisseau], player_rect)
            # Passer à l'image suivante de l'animation
            index_vaisseau += 1
            if index_vaisseau >= len(vaisseau_3):
                index_vaisseau = 0
        elif skin4 == True:
            screen.fill((0, 0, 0))
            bg_y_boss+=scroll_speed_boss
            if bg_y_boss>bg_boss.get_height():
                bg_y_boss=0
            screen.blit(bg_boss, (0,bg_y_boss))
            screen.blit(bg_boss,(0,bg_y_boss-bg_boss.get_height()))            
            screen.blit(vaisseau_4[index_vaisseau], player_rect)
            # Passer à l'image suivante de l'animation
            index_vaisseau += 1
            if index_vaisseau >= len(vaisseau_4):
                index_vaisseau = 0
        elif skin5 == True:
            screen.fill((0, 0, 0))
            bg_y_boss+=scroll_speed_boss
            if bg_y_boss>bg_boss.get_height():
                bg_y_boss=0
            screen.blit(bg_boss, (0,bg_y_boss))
            screen.blit(bg_boss,(0,bg_y_boss-bg_boss.get_height()))            
            screen.blit(vaisseau_5[index_vaisseau], player_rect)
            # Passer à l'image suivante de l'animation
            index_vaisseau += 1
            if index_vaisseau >= len(vaisseau_5):
                index_vaisseau = 0
        elif skin6 == True:
            screen.fill((0, 0, 0))
            bg_y_boss+=scroll_speed_boss
            if bg_y_boss>bg_boss.get_height():
                bg_y_boss=0
            screen.blit(bg_boss, (0,bg_y_boss))
            screen.blit(bg_boss,(0,bg_y_boss-bg_boss.get_height()))            
            screen.blit(vaisseau_6[index_vaisseau], player_rect)
            # Passer à l'image suivante de l'animation
            index_vaisseau += 1
            if index_vaisseau >= len(vaisseau_6):
                index_vaisseau = 0
        elif skin7 == True:
            screen.fill((0, 0, 0))
            bg_y_boss+=scroll_speed_boss
            if bg_y_boss>bg_boss.get_height():
                bg_y_boss=0
            screen.blit(bg_boss, (0,bg_y_boss))
            screen.blit(bg_boss,(0,bg_y_boss-bg_boss.get_height()))            
            screen.blit(vaisseau_7[index_vaisseau], player_rect)
            # Passer à l'image suivante de l'animation
            index_vaisseau += 1
            if index_vaisseau >= len(vaisseau_7):
                index_vaisseau = 0
        elif skin8 == True:
            screen.fill((0, 0, 0))
            bg_y_boss+=scroll_speed_boss
            if bg_y_boss>bg_boss.get_height():
                bg_y_boss=0
            screen.blit(bg_boss, (0,bg_y_boss))
            screen.blit(bg_boss,(0,bg_y_boss-bg_boss.get_height()))            
            screen.blit(vaisseau_8[index_vaisseau], player_rect)
            # Passer à l'image suivante de l'animation
            index_vaisseau += 1
            if index_vaisseau >= len(vaisseau_8):
                index_vaisseau = 0
        if skin_rocket == True:          
            screen.blit(vaisseau_06_rocket_image[index_rocket_boost], player_rect)
            # Passer à l'image suivante de l'animation
            index_rocket_boost += 1
            if index_rocket_boost >= 5 :
                skin_rocket = False
                skin_rocket3 = True
            if index_rocket_boost >= len(vaisseau_06_rocket_image):
                index_rocket_boost = 0
        if skin_rocket3 == True:
            screen.blit(vaisseau_06_rocket_image[5], player_rect)
        if skin_rocket2 == True:      
            screen.blit(vaisseau_06_rocket2_image[index_rocket2_boost], player_rect)
            # Passer à l'image suivante de l'animation
            index_rocket2_boost += 1
            if index_rocket2_boost >= 2:
                skin_rocket2 = False
                skin_rocket3 = False
                skin_rocket4 = True
            if index_rocket2_boost >= len(vaisseau_06_rocket2_image):
                index_rocket2_boost = 0
        if skin_rocket4 == True:
            screen.blit(vaisseau_06_rocket2_image[1], player_rect)
        if skin_rocket5 == True:      
            screen.blit(vaisseau_06_rocket3_image[index_rocket2_boost], player_rect)
            # Passer à l'image suivante de l'animation
            index_rocket2_boost += 1
            if index_rocket2_boost >= 2:
                skin_rocket5 = False
                skin_rocket4 = False
                skin_rocket6 = True
            if index_rocket2_boost >= len(vaisseau_06_rocket3_image):
                index_rocket2_boost = 0
        if skin_rocket6 == True:
            screen.blit(vaisseau_06_rocket3_image[1], player_rect)
        if skin_rocket7 == True:      
            screen.blit(vaisseau_06_rocket4_image[index_rocket2_boost], player_rect)
            # Passer à l'image suivante de l'animation
            index_rocket2_boost += 1
            if index_rocket2_boost >= 2:
                skin_rocket7 = False
                skin_rocket6 = False
                skin_rocket8 = True
            if index_rocket2_boost >= len(vaisseau_06_rocket4_image):
                index_rocket2_boost = 0
        if skin_rocket8 == True:
            screen.blit(vaisseau_06_rocket4_image[1], player_rect)
        if skin_rocket9 == True:      
            screen.blit(vaisseau_06_rocket5_image[index_rocket2_boost], player_rect)
            # Passer à l'image suivante de l'animation
            index_rocket2_boost += 1
            if index_rocket2_boost >= 2:
                skin_rocket9 = False
                skin_rocket8 = False
                skin_rocket10 = True
            if index_rocket2_boost >= len(vaisseau_06_rocket5_image):
                index_rocket2_boost = 0
        if skin_rocket10 == True:
            screen.blit(vaisseau_06_rocket5_image[1], player_rect)
        if skin_rocket11 == True:
            screen.blit(vaisseau_06_rocket6_image[index_rocket2_boost], player_rect)
            # Passer à l'image suivante de l'animation
            index_rocket2_boost += 1
            if index_rocket2_boost >= 2:
                skin_rocket11 = False
                skin_rocket10 = False
                skin_rocket12 = True
            if index_rocket2_boost >= len(vaisseau_06_rocket6_image):
                index_rocket2_boost = 0
        if skin_rocket12 == True:
            screen.blit(vaisseau_06_rocket6_image[1], player_rect)
        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_bongo = False
            elif event.type == pygame.KEYDOWN:
                if keys_enabled:
                    if event.key == pygame.K_SPACE:
                        sound_shoot.play()
                        # Fire a bullet
                        bullet_rect = bullet_image[0].get_rect()
                        bullet_rect.centerx = player_rect.centerx
                        bullet_rect.bottom = player_rect.top + 20
                        bullet_list.append(bullet_rect)
                        bullet_index_list.append(0)
                    if event.key == pygame.K_w and actif_tir_rocket == True:
                        sound_rocket.play()
                        cooldown_text_rocket = False
                        if nb_rocket == 6:
                            w_skill_bullet_rect = w_skill_bullet_image[0].get_rect()
                            w_skill_bullet_rect.centerx = player_rect.centerx + 10
                            w_skill_bullet_rect.bottom = player_rect.top + 50
                            w_skill_bullet_list.append(w_skill_bullet_rect)
                            w_skill_bullet_index_list.append(0)
                            skin_rocket = True
                        if nb_rocket == 5:
                            w_skill_bullet_rect = w_skill_bullet_image[0].get_rect()
                            w_skill_bullet_rect.centerx = player_rect.centerx - 10
                            w_skill_bullet_rect.bottom = player_rect.top + 50
                            w_skill_bullet_list.append(w_skill_bullet_rect)
                            w_skill_bullet_index_list.append(0)
                            skin_rocket2 = True
                        if nb_rocket == 4:
                            w_skill_bullet_rect = w_skill_bullet_image[0].get_rect()
                            w_skill_bullet_rect.centerx = player_rect.centerx + 20
                            w_skill_bullet_rect.bottom = player_rect.top + 50
                            w_skill_bullet_list.append(w_skill_bullet_rect)
                            w_skill_bullet_index_list.append(0)
                            skin_rocket5 = True
                        if nb_rocket == 3:
                            w_skill_bullet_rect = w_skill_bullet_image[0].get_rect()
                            w_skill_bullet_rect.centerx = player_rect.centerx - 20
                            w_skill_bullet_rect.bottom = player_rect.top + 50
                            w_skill_bullet_list.append(w_skill_bullet_rect)
                            w_skill_bullet_index_list.append(0)
                            skin_rocket7 = True
                        if nb_rocket == 2:
                            w_skill_bullet_rect = w_skill_bullet_image[0].get_rect()
                            w_skill_bullet_rect.centerx = player_rect.centerx + 30
                            w_skill_bullet_rect.bottom = player_rect.top + 50
                            w_skill_bullet_list.append(w_skill_bullet_rect)
                            w_skill_bullet_index_list.append(0)
                            skin_rocket9 = True
                        if nb_rocket == 1:
                            w_skill_bullet_rect = w_skill_bullet_image[0].get_rect()
                            w_skill_bullet_rect.centerx = player_rect.centerx - 30
                            w_skill_bullet_rect.bottom = player_rect.top + 50
                            w_skill_bullet_list.append(w_skill_bullet_rect)
                            w_skill_bullet_index_list.append(0)
                            skin_rocket11 = True
                        nb_rocket -= 1
                        if nb_rocket <= 0:
                            rocket_attraper = False
                            actif_tir_rocket = False
                            cooldown_text_rocket = True
                            nb_rocket = 6

        for bullet_rect in bullet_list:
            bullet_rect.move_ip(0, -bullet_speed_player)

        # Détection des collisions entre le joueur et le boss
        player_rect = pygame.Rect(player_x, player_y, default_vaisseau.get_width(), default_vaisseau.get_height())
        boss_rect = pygame.Rect(boss_x, boss_y, boss_image.get_width(), boss_image.get_height()-50)
        if player_rect.colliderect(boss_rect):
            # Mettre à jour la position du joueur pour qu'il ne soit pas en collision avec le boss
            if player_x < boss_x:
                player_x = boss_x - default_vaisseau.get_width()
            elif player_x > boss_x:
                player_x = boss_x + boss_image.get_width()
            if player_y < boss_y:
                player_y = boss_y - default_vaisseau.get_height()
            elif player_y > boss_y:
                player_y = boss_y + boss_image.get_height()

        for bullet_rect in bullet_list:
            if bullet_rect.colliderect(boss_rect):
                bullet_list.remove(bullet_rect)
                boss_health -= 1
                if boss_health <= 0:
                    keys_enabled = False
                    gold = int(gold)+50
                    with open("./Save_Stats/Player_Gold.txt", "w") as f:
                        f.write(str(gold))
                    end_of_game = True
        
        if end_of_game:
            transition_alpha = min(255, transition_alpha + 0.5)
            if transition_alpha > 255:
                transition_alpha = 255
            transition_surface = pygame.Surface((1920, 1080))
            transition_surface.set_alpha(transition_alpha)
            screen.blit(transition_surface, (0, 0))
            BOSS_WIN_TEXT = get_font(40).render("Bien Joué tu à battu le premier Boss, Continue comme sa!", True, "#FFB833")
            BOSS_WIN_RECT = BOSS_WIN_TEXT.get_rect(center=(width // 2, height // 2))
            screen.blit(BOSS_WIN_TEXT, BOSS_WIN_RECT)
            if transition_alpha == 255:
                score+=5
                boucle_jeu(score)

        if player_pv <= 0:
            transition_alpha = min(255, transition_alpha + 0.5)
            if transition_alpha > 255:
                transition_alpha = 255
            transition_surface = pygame.Surface((1920, 1080))
            transition_surface.set_alpha(transition_alpha)
            screen.blit(transition_surface, (0, 0))
            BOSS_WIN_TEXT = get_font(40).render("Dommage, tu aura essayé...", True, "#FFB833")
            BOSS_WIN_RECT = BOSS_WIN_TEXT.get_rect(center=(width // 2, height // 2))
            screen.blit(BOSS_WIN_TEXT, BOSS_WIN_RECT)
            if transition_alpha == 255:
                score = 0
                boucle_jeu(score)

        # Afficher les balles du joueur
        for bullet_rect, bullet_index in zip(bullet_list, bullet_index_list):
            screen.blit(bullet_image[bullet_index], bullet_rect)

            # Passer à l'image suivante de l'animation
            bullet_index += 1
            if bullet_index >= len(bullet_image):
                bullet_index = 0
            bullet_index_list[bullet_list.index(bullet_rect)] = bullet_index

        # Afficher les balles du boss
        for bullet_rect, bullet_index in zip(bullet_list, boss_bullet_index_list):
            screen.blit(boss_bullet_image[boss_bullet_index], bullet_rect)

            # Passer à l'image suivante de l'animation
            boss_bullet_index += 1
            if boss_bullet_index >= len(boss_bullet_image):
                boss_bullet_index = 0
            boss_bullet_index_list[bullet_list.index(bullet_rect)] = boss_bullet_index

        # Déplacement du joueur en fonction des touches appuyées
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_x -= 1.5
        if keys[pygame.K_RIGHT] and player_rect.right < width:
            player_x += 1.5
        if keys[pygame.K_UP]:
            player_y -= 1.5
        if keys[pygame.K_DOWN]:
            player_y += 1.5
            
        # Vérification que le joueur ne sorte pas de l'écran
        if screen_image_state == 1 :
            if player_x < 0:
                player_x = 0
            if player_x > width - default_vaisseau.get_width():
                player_x = width - default_vaisseau.get_width()
            if player_y < 0:
                player_y = 0
            if player_y > 880 - default_vaisseau.get_height():
                player_y = 880 - default_vaisseau.get_height()
        else:
            if player_x < 0:
                player_x = 0
            if player_x > screen_width - default_vaisseau.get_width():
                player_x = screen_width - default_vaisseau.get_width()
            if player_y < 0:
                player_y = 0
            if player_y > screen_height - default_vaisseau.get_height():
                player_y = screen_height - default_vaisseau.get_height()
        # Mise à jour de la position du boss
        boss_x += boss_speed_x
        boss_y += boss_speed_y
        # Vérification que le boss ne sorte pas de l'écran
        if boss_x < 0:
            boss_x = 0
            boss_speed_x = random.uniform(0.1, 0.5)
        if boss_x > screen_width - boss_image.get_width():
            boss_x = screen_width - boss_image.get_width()
            boss_speed_x = -random.uniform(0.1, 0.5)
        if boss_y < 0:
            boss_y = 0
            boss_speed_y = random.uniform(0.1, 0.5)
        if boss_y > screen_height - boss_image.get_height():
            boss_y = screen_height - boss_image.get_height()
            boss_speed_y = -random.uniform(0.1, 0.5)
        # Le boss tire sur le joueur
        if random.randint(1, 250) == 1:
            boss_shoot()
            
        # Déplacement des projectiles
        for bullet in bullets:
            bullet[0] += bullet[2]
            bullet[1] += bullet[3]
            # Vérifier si le projectile est sorti de l'écran
            if bullet[0] < 0 or bullet[0] > screen_width or bullet[1] < 0 or bullet[1] > screen_height:
                bullets.remove(bullet)
            # Vérifier si le joueur a été touché
            elif player_rect.colliderect(pygame.Rect(bullet[0], bullet[1], bullet_width, bullet_height)):
                if not shield_activer:
                    player_pv -= 5
                    bullets.remove(bullet)
                else:
                    bullets.remove(bullet)
                
        # Dessin des projectiles
        for bullet in bullets:
            bullet_rect = pygame.Rect(int(bullet[0]), int(bullet[1]), 100, 100)
            # Rotation de l'image de la balle du boss avec l'angle
            rotated_bullet_image = pygame.transform.rotate(boss_bullet_image[index_boss_bullet], angle)
            screen.blit(rotated_bullet_image, bullet_rect)
            # Mettre à jour l'angle pour faire la rotation continue
            if boss_health > 90:
                angle += 1.5
            elif boss_health > 70 and boss_health < 90:
                angle += 3
                bullet_speed = 2
            elif boss_health > 50 and boss_health < 70:
                angle += 6
                bullet_speed = 3
            elif boss_health < 50:
                angle += 10
                bullet_speed = 4
            if angle >= 360:
                angle = 0
            # Passer à l'image suivante de l'animation
            index_boss_bullet += 1
            if index_boss_bullet >= len(boss_bullet_image):
                index_boss_bullet = 0

        # -------------------------------------------------------- BOOST FOR THE PLAYER ------------------------------------------------ #

        for boost_shield_rect in boost_shield_list:
            if skin1 == True or skin2 == True or skin3 == True or skin5 == True or skin6 == True or skin7 == True:
                screen.blit(boost_shield_image, boost_shield_rect)
            else:
                pass

        for boost_shield_rect in boost_shield_list:
            boost_shield_rect.move_ip(0, boost_shield_speed-0.5)    

        boost_shield_spawn_counter += 1
        if not shield_attraper:
            if boost_shield_spawn_counter >= boost_shield_spawn_rate:
                boost_shield_rect = boost_shield_image.get_rect()
                boost_shield_rect.centerx = random.randint(0, width)
                boost_shield_rect.top = -boost_shield_rect.height
                boost_shield_list.append(boost_shield_rect)
                boost_shield_spawn_counter = 0

        for boost_shield_rect in boost_shield_list:
            if player_rect.colliderect(boost_shield_rect):
                boost_shield_list.remove(boost_shield_rect)
                shield_attraper = True

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and cooldown_text == False:
            sound_shield.play()
            shield_activer = True
            if skin1:
                screen.blit(vaisseau_01_shield_image[index_vaisseau], player_rect)
            if skin2:
                screen.blit(vaisseau_02_shield_image[index_vaisseau], player_rect)
            if skin3:
                screen.blit(vaisseau_03_shield_image[index_shield], player_rect)
            if skin5:
                screen.blit(vaisseau_05_shield_image, player_rect)
            if skin6:
                screen.blit(vaisseau_06_shield_image[index_vaisseau], player_rect)
            if skin7:
                screen.blit(vaisseau_07_shield_image[index_vaisseau], player_rect)
            # Passer à l'image suivante de l'animation
            if index_shield >= len(vaisseau_03_shield_image):
                index_shield = 0
            new_a_cooldown -= 0.05
        else:
            shield_activer = False
            sound_shield.stop()
        if cooldown_text == False:
            new_a_cooldown_rt = round(new_a_cooldown/1)
            a_skill_text = font.render("Shield Restant: " + str(new_a_cooldown_rt) + "%", True, (255,0,0))
            a_skill_rect = a_skill_text.get_rect(center=(300, 780))
            screen.blit(a_skill_text, a_skill_rect)
        if new_a_cooldown >= -1 and new_a_cooldown <= 0:
            shield_attraper = False
            cooldown_text = True
        if new_a_cooldown <= 0 and shield_attraper == False:
            a_cooldown = 600
            new_a_cooldown = 100
            new_a_cooldown_rt = 100


        for boost_rocket_rect in boost_rocket_list:
            screen.blit(boost_rocket_image, boost_rocket_rect)   

        boost_rocket_spawn_counter += 1
        if not rocket_attraper:
            if boost_rocket_spawn_counter >= boost_rocket_spawn_rate and skin6 == True:
                boost_rocket_rect = boost_rocket_image.get_rect()
                boost_rocket_rect.centerx = random.randint(0, width)
                boost_rocket_rect.top = -boost_rocket_rect.height
                boost_rocket_list.append(boost_rocket_rect)
                boost_rocket_spawn_counter = 0

        for boost_rocket_rect in boost_rocket_list:
            if player_rect.colliderect(boost_rocket_rect):
                boost_rocket_list.remove(boost_rocket_rect)
                rocket_attraper = True

        for boost_shield_rect in boost_shield_list:
            boost_shield_rect.move_ip(0, boost_shield_speed)

        for boost_rocket_rect in boost_rocket_list:
            boost_rocket_rect.move_ip(0, boost_rocket_speed)


        for w_skill_bullet_rect in w_skill_bullet_list:
            if w_skill_bullet_rect.colliderect(boss_rect):
                w_skill_bullet_list.remove(w_skill_bullet_rect)
                boss_health -= 5

        # Move the w skill bullets
        for w_skill_bullet_rect in w_skill_bullet_list:
            w_skill_bullet_rect.move_ip(0, -w_skill_bullet_speed)

        for w_skill_bullet_rect in w_skill_bullet_list:
            screen.blit(w_skill_bullet_image[w_skill_bullet_index], w_skill_bullet_rect)
            # Passer à l'image suivante de l'animation
            w_skill_bullet_index += 1
            if w_skill_bullet_index >= len(w_skill_bullet_image):
                w_skill_bullet_index = 0

        if cooldown_text_rocket == False:
            a_skill_text_rocket = font.render("Nombre de Rockets:" + str(nb_rocket), True, (255,0,0))
            a_skill_rect_rocket = a_skill_text_rocket.get_rect(center=(100,height+180))
            screen.blit(a_skill_text_rocket, a_skill_rect_rocket)

        if rocket_attraper == True:
            if cooldown_text_rocket == True:
                actif_tir_rocket = True
                a_skill_text_rocket = font.render("Nombre de Rockets:6", True, (255,0,0))
                a_skill_rect_rocket = a_skill_text_rocket.get_rect(center=(100,height+180))
                screen.blit(a_skill_text_rocket, a_skill_rect_rocket)

        hp_boss_text_rocket = font.render("Vies Boss : " + str(boss_health), True, (0,200,255))
        hp_boss_rect_rocket = hp_boss_text_rocket.get_rect(center=(902,40))
        screen.blit(hp_boss_text_rocket, hp_boss_rect_rocket)

        if shield_attraper == True:
            if a_cooldown >= 0 and cooldown_text == True and shield_attraper == True:
                a_cooldown_rt = round(a_cooldown/60)
                a_skill_text = font.render("Shield à: " + str(a_cooldown_rt) + "%", True, (255,0,0))
                a_skill_rect = a_skill_text.get_rect(center=(300, 780))
                screen.blit(a_skill_text, a_skill_rect)
                a_cooldown += 1

            if a_cooldown_rt >= 100.0:
                cooldown_text = False

        if not shield_activer:
            # Draw life
            if player_pv >= 40:
                life_bar_image = life_bar_imageFull
                update_life_bar(life_bar_image)
            elif player_pv >= 35:
                life_bar_image = life_bar_image1hit
                update_life_bar(life_bar_image)
            elif player_pv >= 30:
                life_bar_image = life_bar_image2hit
                update_life_bar(life_bar_image)
            elif player_pv >= 25:
                life_bar_image = life_bar_image3hit  
                update_life_bar(life_bar_image)
            elif player_pv >= 20:
                life_bar_image = life_bar_image4hit
                update_life_bar(life_bar_image)
            elif player_pv >= 15:
                life_bar_image = life_bar_image5hit
                update_life_bar(life_bar_image)
            elif player_pv >= 10:
                life_bar_image = life_bar_image6hit
                update_life_bar(life_bar_image)
            elif player_pv >= 5:
                life_bar_image = life_bar_image7hit
                update_life_bar(life_bar_image)
            elif player_pv <= 0:
                life_bar_image = life_bar_imageDead
                update_life_bar(life_bar_image)
        else:
            life_bar_image = life_bar_imageShield
            update_life_bar(life_bar_image)

        # Draw score
        score_text = font.render("Score: " + str(score), True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(width/2,20))
        screen.blit(score_text, score_rect)

        # Draw Gold
        gold_text = font.render("Gold: " + str(gold), True, (255, 255, 255))
        gold_rect = gold_text.get_rect(center=(900,10))
        screen.blit(gold_text, gold_rect)
        
        screen.blit(boss_image, (boss_x, boss_y))
        # Mise à jour de l'écran
        pygame.display.update()
    # Fermeture de Pygame
    pygame.quit()