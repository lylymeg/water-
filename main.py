import pygame
import sys

pygame.init()

# Dimensions de la fenêtre (Résolution réduite pour un effet rétro de grille de fluide fluide)
WIDTH, HEIGHT = 800, 600
SCALE = 4  # Chaque "cellule" d'eau fait 4x4 pixels
COLS = WIDTH // SCALE
ROWS = HEIGHT // SCALE

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulateur de Fluide & Ondes Numériques (Water Ripples)")
clock = pygame.time.Clock()

# Deux matrices tampons pour propager l'onde (algorithme de simulation d'eau standard)
buffer1 = [[0.0 for _ in range(COLS)] for _ in range(ROWS)]
buffer2 = [[0.0 for _ in range(COLS)] for _ in range(ROWS)]

# Polices
font_medium = pygame.font.SysFont("Arial", 20, bold=True)
font_small = pygame.font.SysFont("Arial", 15)

running = True
while running:
    mouse_pos = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                # Réinitialiser les tampons d'eau
                buffer1 = [[0.0 for _ in range(COLS)] for _ in range(ROWS)]
                buffer2 = [[0.0 for _ in range(COLS)] for _ in range(ROWS)]

    # Si on clique ou glisse la souris sur l'eau, on crée une perturbation (impact)
    if mouse_pressed[0]:
        mx = mouse_pos[0] // SCALE
        my = mouse_pos[1] // SCALE
        if 2 < mx < COLS - 2 and 2 < my < ROWS - 2:
            buffer1[my][mx] = 750.0  # Intensité de l'impact

    # --- CALCUL DE LA PHYSIQUE DES ONDES ---
    # Équation d'onde 2D : propagation de l'eau voisine avec amortissement
        # Équation d'onde 2D : propagation de l'eau voisine avec amortissement
    for y in range(1, ROWS - 1):
        for x in range(1, COLS - 1):
            # Formule classique de simulation d'eau par moyenne des voisins
            data = (
                buffer1[y - 1][x] +
                buffer1[y + 1][x] +
                buffer1[y][x - 1] +
                buffer1[y][x + 1]
            ) / 2.0 - buffer2[y][x]
            
            # Amortissement (friction de l'eau)
            data *= 0.99
            buffer2[y][x] = data

    # Échange des tampons pour la prochaine frame
    buffer1, buffer2 = buffer2, buffer1

    # --- RENDU GRAPHIQUE DIRECT PAR SURFACE ---
    water_surface = pygame.Surface((WIDTH, HEIGHT))
    
    # Remplir le fond (Teinte bleu nuit profond)
    water_surface.fill((10, 15, 25))

    # Optimisation : Utilisation d'un tableau de pixels pour un rendu fluide
    pixel_array = pygame.PixelArray(water_surface)
    
    for y in range(1, ROWS - 1):
        for x in range(1, COLS - 1):
            val = buffer1[y][x]
            if abs(val) > 0.5:
                # Coloration basée sur l'amplitude de l'onde (effet réfraction / lumière)
                color_intensity = min(255, int(abs(val) * 3))
                # Reflets cyan et bleus
                pixel_array[x * SCALE:(x + 1) * SCALE, y * SCALE:(y + 1) * SCALE] = (
                    0, 
                    min(255, 80 + color_intensity), 
                    min(255, 160 + color_intensity)
                )

    pixel_array.close()
    screen.blit(water_surface, (0, 0))

    # --- HUD ET INSTRUCTIONS ---
    title_txt = font_medium.render("SIMULATEUR DE FLUIDE & ONDES NUMÉRIQUES", True, (255, 255, 255))
    screen.blit(title_txt, (WIDTH // 2 - title_txt.get_width() // 2, 15))

    inst_txt = font_small.render("CLIC GAUCHE (maintenir & glisser) : Perturber l'eau | R : Calmer l'eau", True, (120, 130, 150))
    screen.blit(inst_txt, (WIDTH // 2 - inst_txt.get_width() // 2, 45))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()