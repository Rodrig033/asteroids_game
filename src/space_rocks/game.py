import pygame 
from utils import load_sprite, get_posicion_aletoria, print_text
from pygame.transform import scale 
from models import Spaceship, Asteroide, Bullet, load_sound
from pygame import color


# ---- División del juego ---- 
#  - Manejo de entradas
#  - Lógica del juego
#  - Draw


class SpaceRocks:
    DISTANCIA_MIN_ASTEROIDE = 250
    def __init__(self): # Método constructor 
        self._init_pygame()
        self.screen = pygame.display.set_mode((800, 600)) # Crea la superficie
        self.background = load_sprite("space", False)
        self.imagen_inicio = pygame.image.load("assets/sprites/inicio.png").convert()
        self.imagen_inicio = pygame.transform.scale(self.imagen_inicio, (800, 600))
        self.width, self.height = self.screen.get_size()
        self.background = scale(self.background, self.screen.get_size()) # Me permite ajustar automáticamente la imagen a mi ventana
        self.clock = pygame.time.Clock() # Se encarga de funcionar con una cantidad fija de fps.
        # Voy a crear un menú (necesitamos una variable para controlar el estado del juego).
        self.estado = "inicio"
        self.font_mensaje = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 25) # Fuente | None es una fuente predeterminada.
        self.font = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 12) # Fuente | None es una fuente predeterminada.
        self.font_titulo = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 15)
        self.font_inicio = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 10)
        self.font_reiniciar = pygame.font.Font("assets/fonts/PressStart2p-Regular.ttf", 10)
        self.mensaje = ""
        self.asteroides_destruidos = 0
        self.total_destruir = 50
        self.spaceship = None
        # Limitare la visualización en la ventana a 5 asteroides y 10 generaciones.
        self.total_generaciones = 2 
        self.partes_por_asteroide = 7
        self.generaciones_realizadas = 0
        self.ultima_generacion = 0
        self.collision_sound = load_sound("collision")
        self.ganar_sound = load_sound("win")
        self.menu_sound = load_sound("Space_Waves")
        self.pausa_sound = load_sound("interestelar")
        self.pendiente_generar = False
        self.llamada_crear_asteroide = self._crear_asteroide
        # Botón de pausa:
        self.boton_pausa = pygame.Rect(680, 20, 100, 20)
        self.fuente_pausa = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 10)
        self.pausa = False
        



    def reiniciar_juego(self): 
        self.asteroides = []
        self.balas = [] # Regitra balas
        self.spaceship = Spaceship((400, 300), self.balas.append)

        # Definir los límites de la venta: 
        # Podrías necesitar la distancia y posición del objeto
       
        #Asteroides:
        for _ in range(4):
            while True:
                position = get_posicion_aletoria(self.screen)
                if (
                    position.distance_to(self.spaceship.position) > self.DISTANCIA_MIN_ASTEROIDE
                ):
                    break



            self.asteroides.append(Asteroide(position, self.asteroides.append)) # Almacena la posicion en el arreglo asteroides.
        
        self.estado = "jugando"

        # Reiniciar si ganaste o perdiste:
        # if self.estado == "ganado" or "perdido":
            # instrucciones = self.font_inicio.render("Presiona ENTER para reiniciar", True, (200, 200, 200))
            # instrucciones_reiniciar = instrucciones.get_rect(center = (self. width // 2, 110))
            # self.screen.blit(instrucciones, instrucciones_reiniciar)


    def main_loop(self):
        while True:
            self.handle_input()
            if self.estado == "jugando":
                self.logica_juego()
            
            self.draw()

            if self.pausa:
                pygame.mixer.music.set_volume(0.7) 
                self.pausa_sound.play()
            else:
                self.pausa_sound.stop()


    def _init_pygame(self): # Inicialización 
        pygame.init()
        pygame.display.set_caption("Space Rocks")

    def _get_game_object(self):
        game_objects = [*self.asteroides, *self.balas]

        if self.spaceship:
            game_objects.append(self.spaceship)

        return game_objects
    
    def _crear_asteroide(self, asteroide):
        self.asteroides.append(asteroide)
    

    def handle_input(self):
       
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.boton_pausa.collidepoint(pygame.mouse.get_pos()):
                    self.pausa = not self.pausa
            
            if self.estado == "inicio":
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    self.reiniciar_juego()
                    return
            
            if self.estado in ("ganado", "perdido"):
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    self.reiniciar_juego()
                    return
            

            if self.estado == "jugando":
                if self.spaceship:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            self.spaceship.disparo()


            elif (self.spaceship and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
                  self.spaceship.disparo()

        
 
            
        is_key_pressed = pygame.key.get_pressed()
            
        if self.spaceship:
            if is_key_pressed[pygame.K_RIGHT]:
                self.spaceship.rotate(clockwise=True)
            elif is_key_pressed[pygame.K_LEFT]:
                self.spaceship.rotate(clockwise=False)
            if is_key_pressed[pygame.K_UP]: # Aceleramos 
                self.spaceship.acelerar()
            if is_key_pressed[pygame.K_DOWN]:
                self.spaceship.retroceder()
        
        



    def logica_juego(self):
        if self.pausa:
            return
        
        self.spaceship.move(self.screen)

        for bala in self.balas:
                    bala.move(self.screen)

        for asteroide in self.asteroides:
                    asteroide.move(self.screen)
                                
                    

        #for game_object in self._get_game_object():
            #game_object.move(self.screen)
        
        #if self.pausa:
            #return
        


        # Coliciones con asteroides:
        if self.spaceship:
            for asteroide in self.asteroides:
                if asteroide.coliciones(self.spaceship):
                    self.collision_sound.play() # Sonido de colisión
                    self.spaceship = None
                    self.mensaje = "YOU LOST!"
                    self.estado = "perdido"
                    break

        for bala in self.balas[:]:
            for asteroide in self.asteroides[:]:
                if asteroide.coliciones(bala):
                    self.asteroides.remove(asteroide)
                    self.balas.remove(bala)
                    asteroide.split() # Dividimos la lista en subcadena
                    self.asteroides_destruidos += 1 # Contador
                
                    # Generar nuevos asteroides al terminar con 4 (28 partes): 
                    if self.asteroides_destruidos == 28:
                        #Asteroides:
                        for _ in range(4):
                            while True:
                                    position = get_posicion_aletoria(self.screen)
                                    if (
                                        position.distance_to(self.spaceship.position) > self.DISTANCIA_MIN_ASTEROIDE
                                    ):
                                        break 
                            self.asteroides.append(Asteroide(position, self.asteroides.append)) # Almacena la posicion en el arreglo asteroides.


                    break

        for bala in self.balas[:]:
            if not self.screen.get_rect().collidepoint(bala.position):
                self.balas.remove(bala)

        

        if self.asteroides_destruidos >= self.total_destruir and self.spaceship:
            self.ganar_sound.play()
            self.mensaje = "YOU WIN!" 
            self.estado = "ganado"
        
        

        

    def draw(self):
           
        self.screen.blit(self.background, (0, 0))
        # Pantalla de inicio:

        if self.estado == "inicio":
            self.draw_pantalla_inicio()
            pygame.display.flip()
            self.clock.tick(60)
            return
        
        if self.spaceship:
            self.menu_sound.stop()
            self.spaceship.draw(self.screen)
        for game_object in self._get_game_object():
            game_object.draw(self.screen)


        # Pantalla para reiniciar:
        if self.estado in ("ganado", "perdido"):
            print_text(self.screen, self.mensaje, self.font_mensaje)
            instrucciones = self.font_inicio.render("Presiona ENTER para reiniciar", True, (53, 9, 125))
            instrucciones_rein = instrucciones.get_rect(center = (self. width // 2, self.height // 2 + 30))
            self.screen.blit(instrucciones, instrucciones_rein)
            pygame.display.flip()
            self.clock.tick(60) # Ten mucho cuidado en identificar los métodos.
            self.asteroides_destruidos = 0 # Reinicio el contador de los asteroides.

            return


        # C. Contador 
        hud_ancho = 300
        hud_alto = 40
        hud_pos = (10, 10) # Coordenadas
        hud_color = (30, 30, 30, 180) # Rgb + alpha
        hud_borde = 10
        
        hud_surface = pygame.Surface((hud_ancho, hud_alto), pygame.SRCALPHA)
        pygame.draw.rect(hud_surface, hud_color, (0,0, hud_ancho, hud_alto), border_radius= 12)
        # Contador
        contador_texto = f"Asteroides {self.asteroides_destruidos} / {self. total_destruir}"
        contador_render = self.font.render(contador_texto, True, (255, 255, 255))
        texto_rect = contador_render.get_rect(center = (hud_ancho // 2, hud_alto // 2 ))
        hud_surface.blit(contador_render, texto_rect)
        self.screen.blit(hud_surface, hud_pos)

        # Dibjuar botón de pausa:

        boton_ancho = 120
        boton_alto = 40
        alpha = 180 if self.pausa else 150
        boton_color = (128, 0, 128 , alpha) 
        margen = 10
        
        boton_posicion = (self.screen.get_width() - boton_ancho - margen, margen )
        boton_surface = pygame.Surface((boton_ancho, boton_alto), pygame.SRCALPHA)
        pygame.draw.rect(boton_surface, boton_color, (0, 0, boton_ancho, boton_alto), border_radius= 12)
        #self.screen.blit(boton_surface, (650, 20))

        texto_pausa = "Reanudar" if self.pausa else "Pausa" # Si pausa es True...
        renderizar_pausa = self.fuente_pausa.render(texto_pausa, True, (255, 255, 255))
        texto_pausa_rect = renderizar_pausa.get_rect(center= (boton_ancho // 2, boton_alto // 2))
        boton_surface.blit(renderizar_pausa, texto_pausa_rect)
        self.screen.blit(boton_surface, boton_posicion)


        
        pygame.display.flip() # Actualizamos el contenido de la pantalla
        self.clock.tick(90) # Debe de esperar a alcanzar los fps

    def draw_pantalla_inicio(self):
        self.menu_sound.play()
        self.screen.blit(self.imagen_inicio, (0,0))
        titulo = self.font_titulo.render("ASTEROIDS", True, (255, 255, 255))
        titulo_rect = titulo.get_rect(center = (self.width // 2, 90) )
        self.screen.blit(titulo, titulo_rect)
        # Iniciar: 
        instrucciones = self.font_inicio.render("Presiona ENTER para iniciar la aventura", True, (200, 200, 200))
        instrucciones_rect = instrucciones.get_rect(center = (self. width // 2, 110))
        self.screen.blit(instrucciones, instrucciones_rect)


    
if __name__ == "__main__":
    game = SpaceRocks()
    game.main_loop()