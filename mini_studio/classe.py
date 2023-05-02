import pygame

class displayable :
    def __init__(self,image_name,scaleSize):
        self.image = pygame.image.load(image_name+".png").convert_alpha()
        self.image = pygame.transform.scale(self.image,(scaleSize,scaleSize))

# Définition de la police
font = pygame.font.Font(None, 40)

# Définition de la classe LettreAnimee pour l'animation de texte progressif
class LettreAnimee(pygame.sprite.Sprite):
    def __init__(self, lettre, position, couleur, delay):
        super().__init__()
        self.lettre = lettre
        self.couleur = couleur
        self.image = pygame.Surface((30, 40), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]
        self.delay = delay
        self.alpha = 255
        self.fadein_speed = 5

    def update(self):
        # Affiche la lettre
        self.image.fill((255, 255, 255, 0))
        lettre = font.render(self.lettre, True, self.couleur)
        lettre_rect = lettre.get_rect(center=self.image.get_rect().center)
        self.image.blit(lettre, lettre_rect)

# Création du groupe de sprites pour l'animation de texte progressif
lettre_animee_group = pygame.sprite.Group()