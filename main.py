import pygame

timer = pygame.time.Clock()
SURFACE_SIZE = (1366, 768)
ASPECT_RATIO = 16 / 9
FPS_LIMIT = 60
screen = pygame.display.set_mode(SURFACE_SIZE, pygame.RESIZABLE)
pygame.display.set_caption("PyGameEngine")
pygame.mouse.set_visible(False)

render_surface = pygame.Surface(SURFACE_SIZE).convert()

# Center and scale the render surface within the window while maintaining the aspect ratio.
def blit_scale_screen():
    win_w, win_h = screen.get_size()
    target_w = win_w
    target_h = int(target_w / ASPECT_RATIO)
    if target_h > win_h:
        target_h = win_h
        target_w = int(target_h * ASPECT_RATIO)
    scaled = pygame.transform.smoothscale(render_surface, (target_w, target_h))
    w = (win_w - target_w) // 2
    h = (win_h - target_h) // 2
    screen.fill((0, 0, 0))
    screen.blit(scaled, (w, h))

# Gets current FPS and renders on screen.
def blit_fps_counter():
    fps_counter_surf, fps_counter_coor = UI.window("fps_counter", (0, SURFACE_SIZE[1] - 25), (80, 25), (0, 0, 0), 3)
    UI.text(f"FPS[{timer.get_fps() :.0f}]", 30, (0, 0), (255, 0, 0), win_name="fps_counter", font="segoescript")
    screen.blit(fps_counter_surf, fps_counter_coor)

from game_engine.ui import designer, game, home
from game_engine.package import UI

home_ = home.Window(render_surface)
game_ = None
designer_ = None


command = "home_start"
while command:
    if command.startswith("home"):
        command = home_.update()
    elif command.startswith("game"):
        if game_ is None:
            game_ = game.Window(render_surface)

        command = game_.update()

        if command.endswith("close"):
            home_.command = "home_start"
            game_.command = "game_start"
            command = "home_start"
    elif command.startswith("designer"):
        if designer_ is None:
            designer_ = designer.Window(
                render_surface
            )  # It needs to be designer_.tile_dict_RAW and designer_.tile_dict parameters reloaded.

        command = designer_.update()

        if command.endswith("close"):
            game_.command = "game_start"
            designer_.command = "designer_start"
            command = "game_start"

    if command == "quit":
        break

    blit_scale_screen()
    blit_fps_counter()
    pygame.display.update()

    timer.tick(FPS_LIMIT)

pygame.quit()
