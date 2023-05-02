import pygame
# -------------------------------------- Classe vaisseau pour le Shop -------------------------------------- #
class Vaisseau:
    def __init__(self, prix, locked, image_name, scale):
        self.prix = prix
        self.locked = locked
        self.image = pygame.image.load("assets/vaisseau/"+image_name+".png").convert_alpha()
        self.image = pygame.transform.scale(self.image,(scale,scale))


Vaisseau_1 = Vaisseau(0, True, "vaisseau_01", 40)
Vaisseau_2 = Vaisseau(0, True, "vaisseau_02", 40)
Vaisseau_3 = Vaisseau(0, True, "vaisseau_03", 40)
Vaisseau_4 = Vaisseau(250, True, "vaisseau_04", 40)
Vaisseau_5 = Vaisseau(250, True, "vaisseau_05", 40)
Vaisseau_6 = Vaisseau(250, True, "vaisseau_06", 40)
Vaisseau_7 = Vaisseau(250, True, "vaisseau_07", 40)
Vaisseau_8 = Vaisseau(250, True, "vaisseau_08", 40)

List_Vaisseau = [Vaisseau_1, Vaisseau_2, Vaisseau_3, Vaisseau_4, Vaisseau_5, Vaisseau_6, Vaisseau_7, Vaisseau_8]