from pygame.math import Vector2
from utils import load_sprite, wrap_position, get_random_velocity, load_sound
from pygame.transform import rotozoom


UP = Vector2(0, -1)

class GameObject:
    def __init__(self, position, sprite, velocity):
        self.position = Vector2(position)
        self.sprite = sprite
        self.radius = sprite.get_width() / 2
        self.velocity = Vector2(velocity)
    
    def draw(self, surface):
        blit_position = self.position - Vector2(self.radius)
        surface.blit(self.sprite, blit_position)

    def move(self, surface):
        self.position = self.position + self.velocity
        self.position = wrap_position(self.position, surface)


    def coliciones(self, other_object):
        distance = self.position.distance_to(other_object.position)
        return distance < self.radius + other_object.radius
        

    
class Spaceship(GameObject):
    MANEUVERABILITY = 3
    ACCELERATION = 0.25 # Constante
    VELOCIDAD_BALA = 4
    MAX_VELOCIDAD = 3
    FRICCION = 0.98 # Que tan rapido se detiene la nave si no aceleras
    def __init__(self, position, llamada_crear_bala):
        self.llamada_crear_bala = llamada_crear_bala
        self.laser_sound = load_sound("laser")


        self.direction = Vector2(UP)
        super().__init__(position, load_sprite("spaceship_10"), Vector2(0))
    
    def rotate(self, clockwise = True):
        sign = 1 if clockwise else -1
        angulo = self.MANEUVERABILITY * sign
        self.direction.rotate_ip(angulo)

    def draw(self, surface):
        angulo = self.direction.angle_to(UP)
        rotated_surface = rotozoom(self.sprite, angulo, 1.0)
        rotated_surface_size = Vector2(rotated_surface.get_size())
        blit_position = self.position - rotated_surface_size * 0.5
        surface.blit(rotated_surface, blit_position)
    
    def acelerar(self):
        # Nota: Velocity y direction son vectores.
        self.velocity += self.direction * self.ACCELERATION
        
        if self.velocity.length() > self.MAX_VELOCIDAD:
            self.velocity.scale_to_length(self.MAX_VELOCIDAD) # Limita la velocidad
    
    def retroceder(self):
         # Nota: Velocity y direction son vectores.
        self.velocity -= self.direction * self.ACCELERATION
        
        if self.velocity.length() > self.MAX_VELOCIDAD:
            self.velocity.scale_to_length(self.MAX_VELOCIDAD)

    def disparo(self):
        velocidad_bala = self.direction * self.VELOCIDAD_BALA + self.velocity
        bala = Bullet(self.position, velocidad_bala)
        self.llamada_crear_bala(bala)
        self.laser_sound.play()

class Asteroide(GameObject):
    def __init__(self, position, llamada_crear_asteroide, size = 3):
        self.llamada_crear_asteroide = llamada_crear_asteroide        
        self.size = size

        size_to_scale = {
            3: 1,
            2: 0.5,
            1: 0.25,
        }
        
        scale = size_to_scale[size]
        sprite = rotozoom(load_sprite("asteroid"), 0, scale)

        super().__init__(position, sprite ,get_random_velocity(1,3))

    def split(self):
        if self.size > 1:
            for _ in range(2):
                asteroid = Asteroide(self.position, self.llamada_crear_asteroide, self.size - 1) # Tres parámetros: posición, llamada, tamaño

                self.llamada_crear_asteroide(asteroid)



class Bullet(GameObject):
    def __init__(self, position, velocity):
        super().__init__(position, load_sprite("bullet"), velocity)

    def move(self, surface):
        self.position = self.position + self.velocity
        