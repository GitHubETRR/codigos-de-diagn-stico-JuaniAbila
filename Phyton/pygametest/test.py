import pygame
import time
import random

# Inicializar Pygame
pygame.init()

# Colores
blanco = (255, 255, 255)
negro = (0, 0, 0)
rojo = (213, 50, 80)
verde = (0, 255, 0)
azul = (50, 153, 213)

# Tamaño de la pantalla
ancho = 600
alto = 400
pantalla = pygame.display.set_mode((ancho, alto))
pygame.display.set_caption('Snake 🐍')

# Reloj y fuente
reloj = pygame.time.Clock()
fuente = pygame.font.SysFont("bahnschrift", 25)

# Tamaño del bloque y velocidad
bloque = 20
velocidad = 5

def mensaje(msg, color):
    texto = fuente.render(msg, True, color)
    pantalla.blit(texto, [ancho / 6, alto / 3])

def juego():
    game_over = False
    game_close = False

    x = ancho / 2
    y = alto / 2
    dx = 0
    dy = 0

    cuerpo = []
    largo = 1

    comida_x = round(random.randrange(0, ancho - bloque) / 20.0) * 20.0
    comida_y = round(random.randrange(0, alto - bloque) / 20.0) * 20.0

    while not game_over:

        while game_close:
            pantalla.fill(negro)
            mensaje("¡Perdiste! Q para salir o C para continuar", rojo)
            pygame.display.update()

            for evento in pygame.event.get():
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if evento.key == pygame.K_c:
                        juego()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                game_over = True
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_LEFT:
                    dx = -bloque
                    dy = 0
                elif evento.key == pygame.K_RIGHT:
                    dx = bloque
                    dy = 0
                elif evento.key == pygame.K_UP:
                    dy = -bloque
                    dx = 0
                elif evento.key == pygame.K_DOWN:
                    dy = bloque
                    dx = 0

        x += dx
        y += dy

        if x >= ancho or x < 0 or y >= alto or y < 0:
            game_close = True

        pantalla.fill(azul)
        pygame.draw.rect(pantalla, verde, [comida_x, comida_y, bloque, bloque])

        cabeza = []
        cabeza.append(x)
        cabeza.append(y)
        cuerpo.append(cabeza)

        if len(cuerpo) > largo:
            del cuerpo[0]

        for segmento in cuerpo[:-1]:
            if segmento == cabeza:
                game_close = True

        for parte in cuerpo:
            pygame.draw.rect(pantalla, blanco, [parte[0], parte[1], bloque, bloque])

        pygame.display.update()

        if x == comida_x and y == comida_y:
            comida_x = round(random.randrange(0, ancho - bloque) / 20.0) * 20.0
            comida_y = round(random.randrange(0, alto - bloque) / 20.0) * 20.0
            largo += 1

        reloj.tick(velocidad)

    pygame.quit()
    quit()

juego()