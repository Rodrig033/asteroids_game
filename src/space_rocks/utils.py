from pygame.image import load # Lee las imágenes
from pygame.transform import scale
from pygame.math import Vector2
from pygame.mixer import Sound
from pygame import Color
import random

def load_sprite(name, with_alpha = True):
    path = f"assets/sprites/{name}.png" 
    loaded_sprite = load(path)

    if with_alpha:
        return loaded_sprite.convert_alpha() # Convierte la imagen a un formato que se ajusta mejor a la pantalla
    else:
        return loaded_sprite.convert()
    

def wrap_position(position, surface):
    x, y = position 
    w, h = surface.get_size() # ancho y altura
    return Vector2(x % w, y % h) # Convertimos de tupla a Vector2 

def get_posicion_aletoria(surface):
    return Vector2(random.randrange(surface.get_width()),
                   random.randrange(surface.get_height()),)

def get_random_velocity(min_speed, max_speed):
    speed = random.randint(min_speed, max_speed)
    angle = random.randrange(0, 360) # Entre 0 y 360 grados
    return Vector2(speed, 0).rotate(angle)

def load_sound(name):
     path = f"assets/sounds/{name}.wav" 
     return Sound(path)

def print_text(surface, text, font, color = Color("darkmagenta")):
    text_surface = font.render(text, True, color)

    rect = text_surface.get_rect()
    rect.center = Vector2(surface.get_size()) / 2

    surface.blit(text_surface, rect)