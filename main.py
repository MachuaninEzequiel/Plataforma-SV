import pygame
import os


pygame.init()


ANCHO_PANTALLA = 640
ALTO_PANTALLA = 480
TAMANIO_TILE = 32
TILES_HORIZONTAL = ANCHO_PANTALLA // TAMANIO_TILE  # 20 tiles
TILES_VERTICAL = ALTO_PANTALLA // TAMANIO_TILE  # 15 tiles
pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
pygame.display.set_caption('Juego de Plataforma con Colisiones Detalladas')


BLANCO = (255, 255, 255)


VELOCIDAD_JUGADOR = 5
GRAVEDAD = 1
FUERZA_SALTO = -10


def cargar_sprites(ruta, cantidad):
    imagenes = []
    for i in range(cantidad):
        imagen = pygame.image.load(os.path.join(ruta, f'{i}.png')).convert_alpha()
        imagen = pygame.transform.scale(imagen, (TAMANIO_TILE, TAMANIO_TILE))
        imagenes.append(imagen)
    return imagenes


sprites_parado = cargar_sprites('assets/jugador/parado', 1)
sprites_izquierda = cargar_sprites('assets/jugador/izquierda', 8)
sprites_derecha = cargar_sprites('assets/jugador/derecha', 8)


def cargar_tiles(ruta):
    tiles = []
    for nombre_archivo in os.listdir(ruta):
        if nombre_archivo.endswith('.png'):
            imagen = pygame.image.load(os.path.join(ruta, nombre_archivo)).convert_alpha()
            imagen = pygame.transform.scale(imagen, (TAMANIO_TILE, TAMANIO_TILE))
            tiles.append(imagen)
    return tiles

tiles_mapa = cargar_tiles('assets/tiles')


mapa = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]


pos_x = TAMANIO_TILE  # Posición inicial en X
pos_y = ALTO_PANTALLA - 2 * TAMANIO_TILE  # Posición inicial en Y (un poco por encima del piso)
vel_y = 0
saltando = False
indice_sprite = 0
reloj = pygame.time.Clock()


def renderizar_mapa(mapa):
    for fila_idx, fila in enumerate(mapa):
        for col_idx, tile in enumerate(fila):
            if tile != 0:  # Asumiendo que 0 es un espacio vacío
                pantalla.blit(tiles_mapa[tile - 1], (col_idx * TAMANIO_TILE, fila_idx * TAMANIO_TILE))


def comprobar_colision(mapa, pos_x, pos_y):
    jugador_rect = pygame.Rect(pos_x, pos_y, TAMANIO_TILE, TAMANIO_TILE)
    for fila_idx, fila in enumerate(mapa):
        for col_idx, tile in enumerate(fila):
            if tile != 0:  # Si no es una tile vacía, es sólida
                tile_rect = pygame.Rect(col_idx * TAMANIO_TILE, fila_idx * TAMANIO_TILE, TAMANIO_TILE, TAMANIO_TILE)
                if jugador_rect.colliderect(tile_rect):
                    return tile_rect
    return None


jugando = True
while jugando:
    pantalla.fill(BLANCO)

    
    renderizar_mapa(mapa)

    
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            jugando = False

    
    teclas = pygame.key.get_pressed()
    moviendo_izquierda = teclas[pygame.K_LEFT]
    moviendo_derecha = teclas[pygame.K_RIGHT]

    # Movimiento horizontal
    if moviendo_izquierda:
        nueva_pos_x = pos_x - VELOCIDAD_JUGADOR
        if not comprobar_colision(mapa, nueva_pos_x, pos_y):
            pos_x = nueva_pos_x
        indice_sprite = (indice_sprite + 1) % len(sprites_izquierda)
        pantalla.blit(sprites_izquierda[indice_sprite], (pos_x, pos_y))
    elif moviendo_derecha:
        nueva_pos_x = pos_x + VELOCIDAD_JUGADOR
        if not comprobar_colision(mapa, nueva_pos_x, pos_y):
            pos_x = nueva_pos_x
        indice_sprite = (indice_sprite + 1) % len(sprites_derecha)
        pantalla.blit(sprites_derecha[indice_sprite], (pos_x, pos_y))
    else:
        indice_sprite = (indice_sprite + 1) % len(sprites_parado)
        pantalla.blit(sprites_parado[indice_sprite], (pos_x, pos_y))

    
    if teclas[pygame.K_SPACE] and not saltando:
        vel_y = FUERZA_SALTO
        saltando = True

    
    vel_y += GRAVEDAD
    nueva_pos_y = pos_y + vel_y
    colision_tile = comprobar_colision(mapa, pos_x, nueva_pos_y)
    if colision_tile:
        
        if vel_y > 0 and pos_y + TAMANIO_TILE <= colision_tile.top:
            pos_y = colision_tile.top - TAMANIO_TILE
            vel_y = 0
            saltando = False
        else:
            vel_y = 0  
    else:
        pos_y = nueva_pos_y

    
    pygame.display.flip()
    reloj.tick(25)


pygame.quit()


