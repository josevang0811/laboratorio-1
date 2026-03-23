import pygame
import sys
from game_data_manager import GameDataManager


class PygameGame:
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BLUE = (0, 100, 200)
    GREEN = (0, 200, 0)
    RED = (200, 0, 0)
    GRAY = (200, 200, 200)

    def __init__(self):
        #inicializa Pygame y el gestor de datos
        pygame.init()

        self.WIDTH = 800
        self.HEIGHT = 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Videojuego (Entrega Lab 1) - Tabla Hash")

        self.WHITE = PygameGame.WHITE
        self.BLACK = PygameGame.BLACK
        self.BLUE = PygameGame.BLUE
        self.GREEN = PygameGame.GREEN
        self.RED = PygameGame.RED
        self.GRAY = PygameGame.GRAY
        self.GREEN = (0, 200, 0)
        self.RED = (200, 0, 0)
        self.GRAY = (200, 200, 200)

        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)

        #estado de juego
        self.current_screen = "menu"
        self.current_player = None
        self.input_text = ""
        self.input_active = False
        self.error_message = ""
        self.success_message = ""
        self.message_timer = 0

        #gestor de datos para manejar la tabla hash
        self.manager = GameDataManager("player_data.json")

        #loop principal
        self.running = True
        self.clock = pygame.time.Clock()

    def draw_text(self, text, x, y, color=BLACK, font=None):
        #dibuja texto en pantalla
        if font is None:
            font = self.font
        text_surface = font.render(text, True, color)
        self.screen.blit(text_surface, (x, y))

    def draw_button(self, text, x, y, width, height, color, hover_color=None):
        #dibuja un botón y retorna si está siendo presionado
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if x < mouse[0] < x + width and y < mouse[1] < y + height:
            pygame.draw.rect(self.screen, hover_color or color, (x, y, width, height))
            if click[0]:
                return True
        else:
            pygame.draw.rect(self.screen, color, (x, y, width, height))

        pygame.draw.rect(self.screen, self.BLACK, (x, y, width, height), 2)

        text_surface = self.small_font.render(text, True, self.BLACK)
        text_x = x + (width - text_surface.get_width()) // 2
        text_y = y + (height - text_surface.get_height()) // 2
        self.screen.blit(text_surface, (text_x, text_y))

        return False

    def draw_input_box(self, x, y, width, height, text, active):
        #dibuja una caja de entrada de texto
        color = self.BLUE if active else self.GRAY
        pygame.draw.rect(self.screen, color, (x, y, width, height))
        pygame.draw.rect(self.screen, self.BLACK, (x, y, width, height), 2)

        text_surface = self.small_font.render(text, True, self.BLACK)
        self.screen.blit(text_surface, (x + 5, y + 5))

    def draw_message(self, message, x, y, color=RED):
        #dibuja un mensaje en pantalla
        if message:
            text_surface = self.small_font.render(message, True, color)
            self.screen.blit(text_surface, (x, y))

    def show_menu_screen(self):
        #pantalla del menú principal
        self.screen.fill(self.WHITE)

        self.error_message = ""
        self.success_message = ""

        self.draw_text("VIDEOJUEGO - TABLA HASH", 250, 50, self.BLUE)

        button_width = 200
        button_height = 50
        start_x = self.WIDTH // 2 - button_width // 2
        start_y = 150

        if self.draw_button("Crear Jugador", start_x, start_y, button_width, button_height, self.GREEN, self.BLUE):
            self.current_screen = "create_player"
            self.input_text = ""
            self.error_message = ""
            self.success_message = ""
            pygame.time.wait(200)

        if self.draw_button("Cargar Jugador o Leaderboard", start_x, start_y + 70, button_width, button_height, self.GREEN, self.BLUE):
            self.current_screen = "load_player"
            pygame.time.wait(200)

        if self.draw_button("Ver Estadísticas", start_x, start_y + 140, button_width, button_height, self.GRAY, self.BLUE):
            self.current_screen = "stats"
            pygame.time.wait(200)

        if self.draw_button("Salir", start_x, start_y + 210, button_width, button_height, self.RED, self.BLUE):
            self.running = False

    def show_create_player_screen(self):
        #pantalla para crear un nuevo jugador
        self.screen.fill(self.WHITE)

        input_x = 250
        input_y = 150
        input_width = 300
        input_height = 40

        self.draw_input_box(input_x, input_y, input_width, input_height, self.input_text, self.input_active)
        self.draw_text("Nombre del jugador:", input_x, input_y - 30)

        if self.draw_button("Crear", 350, 250, 100, 40, self.GREEN, self.BLUE):
            if self.input_text.strip():
                if self.manager.crear_jugador(self.input_text, self.input_text):
                    self.current_player = self.input_text
                    self.current_screen = "game"
                    self.error_message = ""
                    self.success_message = f"¡Jugador '{self.input_text}' creado exitosamente!"
                else:
                    self.error_message = f"El jugador '{self.input_text}' ya existe"
                    self.success_message = ""
            pygame.time.wait(200)

        if self.error_message:
            self.draw_message(self.error_message, 250, 200, self.RED)
        if self.success_message:
            self.draw_message(self.success_message, 250, 200, self.GREEN)

        if self.draw_button("Volver", 350, 300, 100, 40, self.GRAY, self.BLUE):
            self.current_screen = "menu"
            pygame.time.wait(200)

    def show_load_player_screen(self):
        #pantalla para cargar un jugador existente
        self.screen.fill(self.WHITE)

        self.draw_text("Cargar Jugador o Leaderboard", 320, 50, self.BLUE)

        players = self.manager.listar_todos_jugadores()
        y_pos = 120

        if not players:
            self.draw_text("No hay jugadores guardados", 280, y_pos, self.RED)
        else:
            self.draw_text("Jugadores disponibles:", 280, y_pos, self.BLACK)
            y_pos += 40

            for player_id, player_data in players:
                if self.draw_button(f"{player_data['nombre']} (Nivel {player_data['nivel']})",
                                  200, y_pos, 400, 35, self.GRAY, self.BLUE):
                    self.current_player = player_id
                    self.current_screen = "game"
                    pygame.time.wait(200)
                y_pos += 45

        if self.draw_button("Volver", 350, 500, 100, 40, self.GRAY, self.BLUE):
            self.current_screen = "menu"
            pygame.time.wait(200)

    def show_game_screen(self):
        #pantalla principal del juego
        self.screen.fill(self.WHITE)

        if self.current_player:
            player_data = self.manager.obtener_jugador(self.current_player)

            self.draw_text(f"Jugador: {player_data['nombre']}", 50, 50, self.BLUE)
            self.draw_text(f"Nivel: {player_data['nivel']}", 50, 90, self.BLACK)
            self.draw_text(f"Puntuación: {player_data['puntuacion']}", 50, 120, self.BLACK)
            self.draw_text(f"Items: {len(player_data['inventario'])}", 50, 150, self.BLACK)

            if self.draw_button("Ver Inventario", 50, 200, 150, 40, self.GREEN, self.BLUE):
                self.current_screen = "inventory"
                pygame.time.wait(200)

            if self.draw_button("Agregar Item", 50, 250, 150, 40, self.GREEN, self.BLUE):
                self.current_screen = "add_item"
                self.input_text = ""
                self.error_message = ""
                self.success_message = ""
                pygame.time.wait(200)

            if self.draw_button("Subir Nivel", 50, 300, 150, 40, self.BLUE, self.GREEN):
                player_data['nivel'] += 1
                player_data['puntuacion'] += 100
                self.manager.actualizar_jugador(self.current_player,
                                              nivel=player_data['nivel'],
                                              puntuacion=player_data['puntuacion'])
                pygame.time.wait(200)

        if self.draw_button("Menú Principal", 600, 500, 150, 40, self.GRAY, self.BLUE):
            self.current_screen = "menu"
            pygame.time.wait(200)

    def show_inventory_screen(self):
        #pantalla del inventario
        self.screen.fill(self.WHITE)

        self.draw_text("Inventario", 350, 50, self.BLUE)

        if self.current_player:
            inventory = self.manager.obtener_inventario(self.current_player)

            if not inventory:
                self.draw_text("Inventario vacío", 330, 150, self.RED)
            else:
                y_pos = 120
                for i, item in enumerate(inventory):
                    self.draw_text(f"{i+1}. {item}", 300, y_pos, self.BLACK)
                    y_pos += 30

        if self.draw_button("Volver", 350, 500, 100, 40, self.GRAY, self.BLUE):
            self.current_screen = "game"
            pygame.time.wait(200)

    def show_add_item_screen(self):
        #pantalla para agregar items al inventario
        self.screen.fill(self.WHITE)

        self.draw_text("Agregar Item al Inventario", 250, 50, self.BLUE)

        input_x = 250
        input_y = 150
        input_width = 300
        input_height = 40

        self.draw_input_box(input_x, input_y, input_width, input_height, self.input_text, self.input_active)
        self.draw_text("Nombre del item:", input_x, input_y - 30)

        if self.draw_button("Agregar", 350, 250, 100, 40, self.GREEN, self.BLUE):
            if self.input_text.strip() and self.current_player:
                if self.manager.agregar_item_inventario(self.current_player, self.input_text):
                    self.success_message = f"¡Item '{self.input_text}' agregado!"
                    self.error_message = ""
                    self.input_text = ""
                else:
                    self.error_message = "Error al agregar item"
                    self.success_message = ""
            pygame.time.wait(200)

        if self.error_message:
            self.draw_message(self.error_message, 250, 200, self.RED)
        if self.success_message:
            self.draw_message(self.success_message, 250, 200, self.GREEN)

        if self.draw_button("Volver", 350, 300, 100, 40, self.GRAY, self.BLUE):
            self.current_screen = "game"
            self.error_message = ""
            self.success_message = ""
            pygame.time.wait(200)

    def show_stats_screen(self):
        #pantalla de estadísticas de la tabla hash
        self.screen.fill(self.WHITE)

        self.draw_text("Estadísticas de la Tabla Hash", 250, 50, self.BLUE)

        stats = self.manager.obtener_estadisticas()

        self.draw_text(f"Tamaño de tabla: {stats['tamaño']}", 200, 120, self.BLACK)
        self.draw_text(f"Elementos: {stats['elementos']}", 200, 150, self.BLACK)
        self.draw_text(f"Factor de carga: {stats['factor_carga']:.2%}", 200, 180, self.BLACK)
        self.draw_text(f"Total jugadores: {stats['total_jugadores']}", 200, 210, self.BLACK)

        if self.draw_button("Volver", 350, 400, 100, 40, self.GRAY, self.BLUE):
            self.current_screen = "menu"
            pygame.time.wait(200)

    def handle_events(self):
        #eventos de Pygame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.current_screen in ["create_player", "add_item"]:
                    input_x, input_y = 250, 150
                    input_width, input_height = 300, 40

                    if input_x < event.pos[0] < input_x + input_width and \
                       input_y < event.pos[1] < input_y + input_height:
                        self.input_active = True
                    else:
                        self.input_active = False

            elif event.type == pygame.KEYDOWN:
                if self.input_active:
                    if event.key == pygame.K_RETURN:
                        self.input_active = False
                    elif event.key == pygame.K_BACKSPACE:
                        self.input_text = self.input_text[:-1]
                    else:
                        self.input_text += event.unicode

    def run(self):
        #loop principal del juego
        while self.running:
            self.handle_events()

            if self.current_screen == "menu":
                self.show_menu_screen()
            elif self.current_screen == "create_player":
                self.show_create_player_screen()
            elif self.current_screen == "load_player":
                self.show_load_player_screen()
            elif self.current_screen == "game":
                self.show_game_screen()
            elif self.current_screen == "inventory":
                self.show_inventory_screen()
            elif self.current_screen == "add_item":
                self.show_add_item_screen()
            elif self.current_screen == "stats":
                self.show_stats_screen()

            pygame.display.flip()

            if self.error_message or self.success_message:
                self.message_timer += 1
                if self.message_timer > 180:
                    self.error_message = ""
                    self.success_message = ""
                    self.message_timer = 0
            
            self.clock.tick(60)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = PygameGame()
    game.run()
