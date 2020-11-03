import pygame
import random
import sqlite3

# COULEURS
BLUE = (113, 177, 227)
WHITE = (255, 255, 255)

# INITIALISATION DE PYGAME
pygame.init()

# INITIALISATION DE LA DATABASE SQLITE
database = "D:/Projects/boom/scores/hiscore.sq3"
connexion_db = sqlite3.connect(database=database)
cursor_db = connexion_db.cursor()
# cursor_db.execute("CREATE TABLE players (score integer)")
# connexion_db.commit()
# cursor_db.execute("INSERT INTO players (score) VALUES (0)")
# connexion_db.commit()
# cursor_db.execute("INSERT INTO players (score) VALUES (0)")
# connexion_db.commit()

# DEFNITION DES DIFFERENTES SURFACE
SURFACE_WIDTH = 800
SURFACE_HEIGHT = 500
BALLON_WIDTH = 50
BALLON_HEIGHT = 66
NUAGE_WIDTH = 300
NUAGE_HEIGHT = 300

# PARAMETRAGE DE L'ECRAN DE JEU
ecran = pygame.display.set_mode((SURFACE_WIDTH, SURFACE_HEIGHT))
pygame.display.set_caption("Flappy Balloon")
horloge = pygame.time.Clock()

img_ballon = pygame.image.load('D:/Projects/boom/Ballon01.png')
image_nuage01 = pygame.image.load('D:/Projects/boom/NuageHaut.png')
image_nuage02 = pygame.image.load('D:/Projects/boom/NuageBas.png')


def score(compte):
    police = pygame.font.Font('D:\Projects/boom/BradBunR.ttf', 16)
    texte = police.render("Score: " + str(compte), True, WHITE)
    ecran.blit(texte, [10, 0])


def high_score(compte):
    police = pygame.font.Font('D:\Projects/boom/BradBunR.ttf', 16)
    texte = police.render("High-Score: " + str(compte), True, WHITE)
    ecran.blit(texte, [700, 0])


def nuages(p_x, p_y, p_espace):
    ecran.blit(image_nuage01, (p_x, p_y))
    ecran.blit(image_nuage02, (p_x, (p_y + NUAGE_WIDTH + p_espace)))


def replay_or_quit():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYUP:
            continue
        return event.type
    return None


def crea_texte_objet(texte, font):
    texte_ecran = font.render(texte, True, WHITE)
    return texte_ecran, texte_ecran.get_rect()


def message(texte):
    go_texte = pygame.font.Font('D:\Projects/boom/BradBunR.ttf', 150)
    go_texte_ecran, go_texte_rect = crea_texte_objet(texte, go_texte)
    go_texte_rect.center = SURFACE_WIDTH / 2, ((SURFACE_HEIGHT / 2) - 50)
    ecran.blit(go_texte_ecran, go_texte_rect)

    petit_texte = pygame.font.Font('D:\Projects/boom/BradBunR.ttf', 25)
    petit_texte_ecran, petit_texte_rect = crea_texte_objet("Appuyer sur une touche pour continuer", petit_texte)
    petit_texte_rect.center = SURFACE_WIDTH / 2, ((SURFACE_HEIGHT / 2) + 50)
    ecran.blit(petit_texte_ecran, petit_texte_rect)

    pygame.display.update()

    while replay_or_quit() is None:
        horloge.tick()

    game()


def gameover(score_actuel):
    # a = list(str(score_actuel))
    a = [str(score_actuel)]
    # string = ''
    database = "D:/Projects/boom/scores/hiscore.sq3"
    connexion_db = sqlite3.connect(database)
    cursor_db = connexion_db.cursor()
    cursor_db.execute("SELECT * FROM players")
    liste = list(cursor_db)
    hscore = []
    for i in range(0, len(liste)):
        hscore += liste[i]

    if int(hscore[-1]) < score_actuel:
        # for i in range(0, len(a)):
        #     string += str(a[i])
        #     print(str(string))
        # print(list(str(string)))
        cursor_db.execute("INSERT INTO players VALUES (?)", a)
        connexion_db.commit()
        cursor_db.close()
        connexion_db.close()
    message("Boom!")


def ballon(p_x, p_y, p_image):
    ecran.blit(p_image, (p_x, p_y))


def game():
    ballon_x = 150
    ballon_y = 200
    mouvement = 0

    nuage_x = SURFACE_WIDTH
    nuage_y = random.randint(-300, 20)
    espace = BALLON_HEIGHT * 3
    nuage_vitesse = 6

    score_actuel = 0

    display_it = True

    while display_it:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                display_it = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    mouvement = -5
            if event.type == pygame.KEYUP:
                mouvement = 5
        ballon_y = ballon_y + mouvement
        ecran.fill(BLUE)
        ballon(ballon_x, ballon_y, img_ballon)
        nuages(nuage_x, nuage_y, espace)
        score(score_actuel)
        cursor_db.execute("SELECT * FROM players")
        liste = list(cursor_db)
        print(cursor_db)
        print(liste)

        hscore = []
        for i in range(0, len(liste)):
            hscore += liste[i]

        high_score(hscore[-1])

        nuage_x -= nuage_vitesse

        if ballon_y > (SURFACE_HEIGHT - BALLON_HEIGHT) or ballon_y < 0:
            gameover(score_actuel)

        if 3 <= score_actuel < 5:
            nuage_vitesse = 7
            espace = BALLON_HEIGHT * 2.8
        if 6 <= score_actuel < 9:
            nuage_vitesse = 8
            espace = BALLON_HEIGHT * 2.7
        if 10 <= score_actuel < 15:
            nuage_vitesse = 9
            espace = BALLON_HEIGHT * 2.6
        if 16 <= score_actuel < 20:
            nuage_vitesse = 9.25
            espace = BALLON_HEIGHT * 2.5
        if 21 <= score_actuel < 30:
            nuage_vitesse = 9.33
            espace = BALLON_HEIGHT * 2.4
        if score_actuel >= 30:
            nuage_vitesse = 9.40
            espace = BALLON_HEIGHT * 2.25

        if ballon_x + BALLON_WIDTH > nuage_x + 40:
            if ballon_y < nuage_y + NUAGE_HEIGHT - 50:
                if ballon_x - BALLON_WIDTH < nuage_x + NUAGE_WIDTH - 20:
                    gameover(score_actuel)

        if ballon_x + BALLON_WIDTH > nuage_x + 40:
            if ballon_y + BALLON_HEIGHT > nuage_y + NUAGE_HEIGHT + espace + 50:
                if ballon_x - BALLON_WIDTH < nuage_x + NUAGE_WIDTH - 20:
                    gameover(score_actuel)

        if nuage_x < (-1 * NUAGE_WIDTH):
            nuage_x = SURFACE_WIDTH
            nuage_y = random.randint(-300, 20)

        if nuage_x < (ballon_x - NUAGE_WIDTH) < nuage_x + nuage_vitesse:
            score_actuel += 1

        pygame.display.update()
        horloge.tick(60)

    pygame.quit()
    quit()


game()
