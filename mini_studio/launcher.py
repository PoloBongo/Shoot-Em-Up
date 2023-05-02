import pygame, sys, random
from button import Button
from cosmetique import *
from mode_infinie import boucle_jeu, get_gold, get_stats
from vaisseau import *
from classe import *

pygame.init()

score = 0

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

pygame.display.set_caption("Alien Assault")

# Charger l'icône
icon = pygame.image.load("assets/alien_war_icon.png")

# Définir l'icône de la fenêtre
pygame.display.set_icon(icon)

# Lecture de l'état de l'image écran à partir du fichier
try:
    with open("Save_Stats/Screen_Stats.txt", "r") as f:
        screen_image_state = int(f.read())
except FileNotFoundError:
    screen_image_state = 1

# Définition de la taille d'écran initiale
if screen_image_state == 1:
    screen_size = (SCREEN_WIDTH, SCREEN_HEIGHT)
    screen_flags = pygame.FULLSCREEN
else:
    screen_size = (SCREEN_WIDTH, SCREEN_HEIGHT)
    screen_flags = 0

# Création de la surface d'écran
screen = pygame.display.set_mode(screen_size, screen_flags)

# Music de fond du Launcher
def sound():
    pygame.mixer.init()
    pygame.mixer.music.load('assets/music/background_music.mp3')
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play(-1)
# Activation de la music lors du lancement de la fenêtre
sound()

background_launcher = pygame.image.load("assets/background_laucher.png")
background_shop = pygame.image.load("assets/shop/background_shop.jpg")

start_btn = pygame.image.load('assets/launcher/start_btn.png').convert_alpha()
exit_btn = pygame.image.load('assets/launcher/exit_btn.png').convert_alpha()
setting_btn = pygame.image.load('assets/launcher/settings_btn.png').convert_alpha()
shop_btn = pygame.image.load('assets/launcher/shop_btn.png').convert_alpha()

font_shop = pygame.font.Font(None, 30)

def get_font(size): # Chargement d'un font import
    return pygame.font.Font("assets/SIXTY.ttf", size)

# Fonction pour dessiner le menu
def draw_menu(x, y):
    global selected_option
    for i, option in enumerate(menu_options):
        text = get_font(27).render(option, True, WHITE)
        rect = text.get_rect()
        rect.x = x
        rect.y = y + i * rect.height
        if rect.collidepoint(pygame.mouse.get_pos()):
            text = get_font(27).render(option, True, "#FFAA00")
            if pygame.mouse.get_pressed()[0]:
                selected_option = i
        screen.blit(text, rect)



# Fonction pour dessiner le boutton "Valider"
def draw_button_valider(x, y, stats):
    try:
        with open("Save_Stats/Screen_Stats.txt", "r") as f:
            screen_image_state = int(f.read())
    except FileNotFoundError:
        screen_image_state = 1

    gold = int(get_gold())
    button_text = get_font(27).render("Valider", True, WHITE)
    button_rect = button_text.get_rect()
    button_rect.x = x
    button_rect.y = y

    with open("./Save_Stats/Player_Gold.txt", "w") as f:
        f.write(str(gold))
    skin_gold_text = font.render("Gold : " + str(gold) + " $", True, "#FFAA00")
    if screen_image_state == 1:
        skin_gold_rect = skin_gold_text.get_rect(center=(780, 620))
    else:
        skin_gold_rect = skin_gold_text.get_rect(center=(750, 535))
    screen.blit(skin_gold_text, skin_gold_rect)

    if button_rect.collidepoint(pygame.mouse.get_pos()):
        button_text = get_font(27).render("Valider", True, "#FFAA00")
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if selected_option is not None and (List_Vaisseau[selected_option].locked == True and List_Vaisseau[selected_option].prix <= gold):
                        with open("./Save_Stats/Skin_Vaisseau.txt", "w") as f:
                            f.write(menu_options[selected_option])
                        with open("./Save_Stats/Vaisseau_stats.txt", "w") as f:
                            f.write(str(selected_option))
                        gold = gold - List_Vaisseau[selected_option].prix
                        List_Vaisseau[int(stats)].locked = False
                        with open("./Save_Stats/Player_Gold.txt", "w") as f:
                            f.write(str(gold))
    if selected_option is not None and List_Vaisseau[selected_option].locked == True and List_Vaisseau[selected_option].prix > gold:
        skin_lock_text = font_shop.render("Skin Vérouiller : " + str(List_Vaisseau[selected_option].prix) + " $", True, (255, 0, 0))
        if screen_image_state == 1:
            skin_lock_rect = skin_lock_text.get_rect(center=(730, 160))
        else:
            skin_lock_rect = skin_lock_text.get_rect(center=(720, 80))
        screen.blit(skin_lock_text, skin_lock_rect)
    else:
        if selected_option is not None:
            skin_unlock_text = font_shop.render("Skin Disponible à l'achat : " + str(List_Vaisseau[selected_option].prix) + " $", True, (0, 255, 0))
            if screen_image_state == 1:
                skin_unlock_rect = skin_unlock_text.get_rect(center=(730, 160))
            else:
                skin_unlock_rect = skin_unlock_text.get_rect(center=(720, 80))
            screen.blit(skin_unlock_text, skin_unlock_rect)
    screen.blit(button_text, button_rect)

# Fonction pour dessiner le boutton Retour du Shop
def draw_button_menu_principal(x, y):
    button_text = get_font(27).render("Retour", True, WHITE)
    button_rect = button_text.get_rect()
    button_rect.x = x
    button_rect.y = y
    if button_rect.collidepoint(pygame.mouse.get_pos()):
        button_text = get_font(27).render("Retour", True, "#FFAA00")
        if pygame.mouse.get_pressed()[0]:
            main_menu()
    screen.blit(button_text, button_rect)

# Fonction qui ouvre le fenêtre Shop pour choisir son vaisseau
def shop_cosmetique(stats):
    run_shop = True
    while run_shop:
        stats = get_stats()
        try:
            with open("Save_Stats/Screen_Stats.txt", "r") as f:
                screen_image_state = int(f.read())
        except FileNotFoundError:
            screen_image_state = 1

        if screen_image_state == 1:
            screen.blit(background_shop, (-50, 0))
            draw_menu(120, 265)
            draw_button_valider(320, 615, stats)
            draw_button_menu_principal(210, 615)
            MENU_TEXT = get_font(40).render("Skin Vaisseau", True, "#FFB833")
            MENU_RECT = MENU_TEXT.get_rect(center=(550, 80))
            screen.blit(MENU_TEXT, MENU_RECT)
        else:
            screen.blit(background_shop, (-100, -100))
            draw_menu(80, 180)
            draw_button_valider(290, 525, stats)
            draw_button_menu_principal(180, 525)
            MENU_TEXT = get_font(40).render("Skin Vaisseau", True, "#FFB833")
            MENU_RECT = MENU_TEXT.get_rect(center=(400, 80))
            screen.blit(MENU_TEXT, MENU_RECT)

        ################################### AFFICHER L IMAGE SELECTIONNER PAR LE JOUEUR #########################################

        if selected_option == 0:
            screen.blit(option1_image, (300, 250))
        elif selected_option == 1:
            screen.blit(option2_image, (300, 250))
        elif selected_option == 2:
            screen.blit(option3_image, (300, 250))
        elif selected_option == 3:
            screen.blit(option4_image, (300, 250))
        elif selected_option == 4:
            screen.blit(option5_image, (300, 250))
        elif selected_option == 5:
            screen.blit(option6_image, (300, 250))
        elif selected_option == 6:
            screen.blit(option7_image, (300, 250))
        elif selected_option == 7:
            screen.blit(option8_image, (300, 250))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        # Mise à jour de l'écran
        pygame.display.update()

# ------------------------------------------------------------------------ DEBUT FUNCTION OPTIONS ------------------------------------------------------------------------ #
def settings():

    font_touche = pygame.font.Font(None, 30)

    # Définition des zones de texte
    text_box = pygame.Rect(50, 75, 900, 500)
    text_box_touche = pygame.Rect(100, 195, 570, 280)

    # Variables de paramètres
    volume = 50

    # Charger des images de boutons et du curseur
    image1 = pygame.image.load("assets/settings/sound_on.png").convert_alpha()
    image2 = pygame.image.load("assets/settings/sound_off.png").convert_alpha()

    image_fenetre = pygame.image.load("assets/settings/ordi.png").convert_alpha()
    image_fullscreen = pygame.image.load("assets/settings/ordi.png").convert_alpha()
    volume_slider_cursor_img = pygame.transform.scale(pygame.image.load("assets/settings/ajuster_volume.png").convert_alpha(), (25, 25))
    # Créer des surfaces pour les boutons et le curseur
    volume_slider = pygame.Surface((200, 25))
    volume_slider.fill((255, 155, 0))
    volume_slider_rect = volume_slider.get_rect().move(300, 480)
    volume_slider_cursor_rect = pygame.Rect((volume / 100) * (volume_slider_rect.width + 395), 480, 40, volume_slider_rect.height - 100)

    # Définition des dimensions et de la position des boutons pour les touches
    bouton_retour = pygame.Rect(50, 75, 120, 50)
    bouton_touche_w = pygame.Rect(110, 250, 57, 50)
    bouton_touche_q = pygame.Rect(110, 300, 57, 50)
    bouton_touche_a = pygame.Rect(110, 350, 57, 50)
    bouton_touche_haut = pygame.Rect(350, 250, 40, 50)
    bouton_touche_droite = pygame.Rect(350, 300, 40, 50)
    bouton_touche_bas = pygame.Rect(350, 350, 40, 50)
    bouton_touche_gauche = pygame.Rect(350, 400, 40, 50)
    bouton_touche_espace = pygame.Rect(110, 400, 110, 50)

    try:
        with open("Save_Stats/Screen_Stats.txt", "r") as f:
            screen_image_state = int(f.read())
    except FileNotFoundError:
        screen_image_state = 1

    # Définition de la taille d'écran initiale
    if screen_image_state == 1:
        screen_size = (SCREEN_WIDTH, SCREEN_HEIGHT)
        screen_flags = pygame.FULLSCREEN
    else:
        screen_size = (SCREEN_WIDTH, SCREEN_HEIGHT)
        screen_flags = 0
        
    # Création de la surface d'écran en fonction de la save du screen
    screen = pygame.display.set_mode(screen_size, screen_flags)

    # Image pour activer / désactivé le son
    image = image1
    music_image_rect = image1.get_rect()
    music_image_rect.topright = (screen.get_width() - 20, 10)
    screen.blit(image, (0, 0))

    image_screen = image_fullscreen
    screen_image_rect = image_fullscreen.get_rect()
    screen_image_rect.topright = (screen.get_width() - 730, 515)
    screen.blit(image_screen, (0, 0))

    try:
        with open("Save_Stats/Music_Stats.txt", "r") as f:
            music_image_state = int(f.read())
    except FileNotFoundError:
        music_image_state = 1

    # Boucle principale
    running_setting = True
    while running_setting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_setting = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if music_image_rect.collidepoint(event.pos):
                    if music_image_state == 1:
                        music_image_state = 2
                        pygame.mixer.music.stop()
                    else:
                        music_image_state = 1
                        pygame.mixer.music.play()

                    with open("Save_Stats/Music_Stats.txt", "w") as f:
                        f.write(str(music_image_state))
                elif screen_image_rect.collidepoint(event.pos):
                    if screen_image_state == 1:
                        screen_image_state = 2
                    else:
                        screen_image_state = 1
                    with open("Save_Stats/Screen_Stats.txt", "w") as f:
                        f.write(str(screen_image_state))

                    # Changement du mode d'affichage
                    if screen_image_state == 1:
                        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
                    else:
                        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

                    # Rafraîchissement du screen
                    screen.blit(image_fullscreen, screen_image_rect)
                    pygame.display.flip()

                # Vérifie si le curseur de volume a été cliqué
                elif volume_slider_rect.collidepoint(pygame.mouse.get_pos()):
                    volume_slider_cursor_rect.centerx = pygame.mouse.get_pos()[0]
                    volume = int((volume_slider_cursor_rect.centerx - volume_slider_rect.x) / volume_slider_rect.width * 100)
                    pygame.mixer.music.set_volume(volume / 100)
                if bouton_retour.collidepoint(event.pos):
                    main_menu()
            elif event.type == pygame.ACTIVEEVENT:
                if event.gain == 1:
                    if screen_image_state == 1:
                        screen_size = (SCREEN_WIDTH, SCREEN_HEIGHT)
                        screen_flags = pygame.FULLSCREEN
                    else:
                        screen_size = (SCREEN_WIDTH, SCREEN_HEIGHT)
                        screen_flags = 0
                    # Mise à jour de la surface du screen
                    screen = pygame.display.set_mode(screen_size, screen_flags)

        # Affichage du fond
        screen.blit(background_launcher, (0, 0))

        # Permet de charger l'image du son
        if music_image_state == 1:
            screen.blit(image1, music_image_rect)
        else:
            screen.blit(image2, music_image_rect)
        
        # Permet de charger la taille d'écran
        if screen_image_state == 1:
            SCREEN_TEXT = font_touche.render("Mode Fenêtré : ", True, "#FFB833")
            SCREEN_RECT = SCREEN_TEXT.get_rect(center=(180, 525))
            screen.blit(SCREEN_TEXT, SCREEN_RECT)
            screen.blit(image_fenetre, screen_image_rect)
        else:
            SCREEN_TEXT = font_touche.render("Plein Ecran : ", True, "#FFB833")
            SCREEN_RECT = SCREEN_TEXT.get_rect(center=(170, 525))
            screen.blit(SCREEN_TEXT, SCREEN_RECT)
            screen.blit(image_fullscreen, screen_image_rect)

        screen.blit(volume_slider, volume_slider_rect)
        screen.blit(volume_slider_cursor_img, volume_slider_cursor_rect)
        pygame.draw.rect(screen, (255, 255, 255), volume_slider_cursor_rect)

        # Affichage du titre
        title = font.render("Paramètres", True, (65, 105, 225))
        title_rect = title.get_rect()
        title_rect.center = (SCREEN_WIDTH // 2, 50)
        screen.blit(title, title_rect)
        
        # ---------------------------------------------------- AFFICHAGE DES BOUTTONS/TEXTES POUR JOUER ------------------------------------------------ #

        TOUCHE_TEXT = font.render("Touches", True, "#00FFDC")
        TOUCHE_RECT = TOUCHE_TEXT.get_rect(center=(370, 225))
        screen.blit(TOUCHE_TEXT, TOUCHE_RECT)

        pygame.draw.rect(screen, (200, 200, 200), bouton_touche_w)
        texte_touche_w = font_touche.render("W :", True, (0, 0, 0))
        screen.blit(texte_touche_w, (bouton_touche_w.x + 10, bouton_touche_w.y + 15))

        TOUCHE_W_TEXT = font_touche.render("Rockets Skills", True, "#FFB833")
        TOUCHE_W_RECT = TOUCHE_W_TEXT.get_rect(center=(255, 275))
        screen.blit(TOUCHE_W_TEXT, TOUCHE_W_RECT)

        pygame.draw.rect(screen, (200, 200, 200), bouton_touche_q)
        texte_touche_q = font_touche.render("Q :", True, (0, 0, 0))
        screen.blit(texte_touche_q, (bouton_touche_q.x + 10, bouton_touche_q.y + 15))

        TOUCHE_Q_TEXT = font_touche.render("Laser Skills", True, "#FFB833")
        TOUCHE_Q_RECT = TOUCHE_Q_TEXT.get_rect(center=(245, 325))
        screen.blit(TOUCHE_Q_TEXT, TOUCHE_Q_RECT)

        pygame.draw.rect(screen, (200, 200, 200), bouton_touche_a)
        texte_touche_a = font_touche.render("A :", True, (0, 0, 0))
        screen.blit(texte_touche_a, (bouton_touche_a.x + 10, bouton_touche_a.y + 15))

        TOUCHE_A_TEXT = font_touche.render("Shield Skills", True, "#FFB833")
        TOUCHE_A_RECT = TOUCHE_A_TEXT.get_rect(center=(250, 375))
        screen.blit(TOUCHE_A_TEXT, TOUCHE_A_RECT)

        pygame.draw.rect(screen, (200, 200, 200), bouton_touche_espace)
        texte_touche_espace = font_touche.render("ESPACE :", True, (0, 0, 0))
        screen.blit(texte_touche_espace, (bouton_touche_espace.x + 10, bouton_touche_espace.y + 15))

        TOUCHE_ESPACE_TEXT = font_touche.render("Tirer", True, "#FFB833")
        TOUCHE_ESPACE_RECT = TOUCHE_ESPACE_TEXT.get_rect(center=(250, 425))
        screen.blit(TOUCHE_ESPACE_TEXT, TOUCHE_ESPACE_RECT)

        img_fleche_haut = pygame.image.load('assets/settings/fleche_haut.png').convert_alpha()
        pygame.draw.rect(screen, (200, 200, 200), bouton_touche_haut)
        pos_emoji_touche_haut = img_fleche_haut.get_rect(center=bouton_touche_haut.center)
        screen.blit(img_fleche_haut, pos_emoji_touche_haut)

        TOUCHE_HAUT_TEXT = font_touche.render("Se déplacer vers le haut", True, "#FFB833")
        TOUCHE_HAUT_RECT = TOUCHE_HAUT_TEXT.get_rect(center=(515, 275))
        screen.blit(TOUCHE_HAUT_TEXT, TOUCHE_HAUT_RECT)

        img_fleche_droite = pygame.image.load('assets/settings/fleche_droite.png').convert_alpha()
        pygame.draw.rect(screen, (200, 200, 200), bouton_touche_droite)
        pos_emoji_touche_droite = img_fleche_droite.get_rect(center=bouton_touche_droite.center)
        screen.blit(img_fleche_droite, pos_emoji_touche_droite)

        TOUCHE_DROITE_TEXT = font_touche.render("Se déplacer vers la droite", True, "#FFB833")
        TOUCHE_DROITE_RECT = TOUCHE_DROITE_TEXT.get_rect(center=(522, 325))
        screen.blit(TOUCHE_DROITE_TEXT, TOUCHE_DROITE_RECT)

        img_fleche_bas = pygame.image.load('assets/settings/fleche_bas.png').convert_alpha()
        pygame.draw.rect(screen, (200, 200, 200), bouton_touche_bas)
        pos_emoji_touche_bas = img_fleche_bas.get_rect(center=bouton_touche_bas.center)
        screen.blit(img_fleche_bas, pos_emoji_touche_bas)

        TOUCHE_BAS_TEXT = font_touche.render("Se déplacer vers le bas", True, "#FFB833")
        TOUCHE_BAS_RECT = TOUCHE_BAS_TEXT.get_rect(center=(510, 375))
        screen.blit(TOUCHE_BAS_TEXT, TOUCHE_BAS_RECT)

        img_fleche_gauche = pygame.image.load('assets/settings/fleche_gauche.png').convert_alpha()
        pygame.draw.rect(screen, (200, 200, 200), bouton_touche_gauche)
        pos_emoji_touche_gauche = img_fleche_gauche.get_rect(center=bouton_touche_gauche.center)
        screen.blit(img_fleche_gauche, pos_emoji_touche_gauche)

        TOUCHE_GAUCHE_TEXT = font_touche.render("Se déplacer vers la gauche", True, "#FFB833")
        TOUCHE_GAUCHE_RECT = TOUCHE_GAUCHE_TEXT.get_rect(center=(530, 425))
        screen.blit(TOUCHE_GAUCHE_TEXT, TOUCHE_GAUCHE_RECT)

        VOLUME_TEXT = font_touche.render("Ajuster le Volume : ", True, "#FFB833")
        VOLUME_RECT = VOLUME_TEXT.get_rect(center=(200, 493))
        screen.blit(VOLUME_TEXT, VOLUME_RECT)

        # ---------------------------------------------------- FIN DES AFFICHAGES DES BOUTTONS/TEXTES POUR JOUER ------------------------------------------------ #


        # Affichage du bouton retour
        pygame.draw.rect(screen, (200, 200, 200), bouton_retour)
        texte_retour = font.render("Retour", True, (0, 0, 0))
        screen.blit(texte_retour, (bouton_retour.x + 20, bouton_retour.y + 15))

        # Affichage de la zone de texte
        pygame.draw.rect(screen, (255, 255, 255), text_box, 2)
        pygame.draw.rect(screen, (255, 0, 0), text_box_touche, 2)

        # Affichage des instructions aléatoires dans l'animation de texte progressif
        instructions = "Comment Jouer ?"
        for i, lettre in enumerate(instructions):
            lettre_animee = LettreAnimee(lettre, (325 + i * 25, text_box.bottom - 500), (255, 255, 255), random.randint(0, 100))
            lettre_animee_group.add(lettre_animee)

        # Mise à jour de l'animation de texte progressif
        for lettre in lettre_animee_group:
            if lettre.delay == 0:
                lettre.update()
        lettre_animee_group.draw(screen)


        # Actualisation de l'affichage
        pygame.display.flip()

    # Fermeture de Pygame
    pygame.quit()

# Placement des bouttons sur le launcher
start_button = Button(200, 300, start_btn, 0.8)
exit_button = Button(500, 310, exit_btn, 0.74)
setting_button = Button(940, 10, setting_btn, 0.1)
shop_button = Button(800, 300, shop_btn, 0.1)

def main_menu():
    while True:
        stats = get_stats()

        screen.blit(background_launcher, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(50).render("Alien Assault", True, "#FFAA00")
        MENU_RECT = MENU_TEXT.get_rect(center=(SCREEN_WIDTH // 2, 100))

        PLAY_BUTTON = Button(SCREEN_WIDTH // 5, SCREEN_HEIGHT // 2, start_btn, 0.8)
        QUIT_BUTTON = Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 1.94, exit_btn, 0.74)
        OPTIONS_BUTTON = Button(940, 10, setting_btn, 0.1)
        SHOP_BUTTON = Button(10, 10, shop_btn, 0.1)

        screen.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, SHOP_BUTTON, QUIT_BUTTON]:

            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    boucle_jeu(score)
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    settings()
                if SHOP_BUTTON.checkForInput(MENU_MOUSE_POS):
                    shop_cosmetique(stats)
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()