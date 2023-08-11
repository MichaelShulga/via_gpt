import pygame
import pymunk
import pymunk.pygame_util


# Видео параметры
WIDTH, HEIGHT = 800, 600
FPS = 60

# Инициализация Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Инициализация Pymunk
space = pymunk.Space()
space.gravity = (0, 0)  # Отключение гравитации для упрощения

# Физические константы
G = 1

# Расчет скорости под действием силы притяжения
def planetGravity(body, gravity, damping, dt): 
    g = pymunk.Vec2d(0, 0) 
    for other_body in space.bodies: 
        r = other_body.position - body.position 
        if r.length: 
            force = G * (other_body.mass * body.mass) / (r.length ** 2) * (r / r.length) 
            g += force / body.mass 
    pymunk.Body.update_velocity(body, g, damping, dt) 
        
# Создание звезды
star_mass = 1000_000
star_radius = 30
star_moment = pymunk.moment_for_circle(star_mass, 0, star_radius)
star_body = pymunk.Body(star_mass, star_moment)
star_body.position = (WIDTH // 2, HEIGHT // 2)
star_body.velocity = (10, 10)
star_body.velocity_func = planetGravity
star_shape = pymunk.Circle(star_body, star_radius)
space.add(star_body, star_shape)

# Переменные для отслеживания добавления нового тела
new_body = None
mouse_pressed = False

# Создание Pygame экрана для рисования
draw_options = pymunk.pygame_util.DrawOptions(screen)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Запомнить начальное положение мыши при нажатии
            mouse_pressed = True

            body_mass = 1
            body_radius = 5
            body_moment = pymunk.moment_for_circle(body_mass, 0, body_radius)
            new_body = pymunk.Body(body_mass, body_moment)
            new_body.position = event.pos
            new_body.velocity_func = planetGravity
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if mouse_pressed:
                new_body.velocity = pymunk.Vec2d(*event.pos) - pymunk.Vec2d(*new_body.position)
                space.add(new_body, pymunk.Circle(new_body, body_radius))
                
                new_body = None
                mouse_pressed = False

    # Обновление симуляции
    space.step(1/FPS)
    
    # Отрисовка
    screen.fill((255, 255, 255))
    space.debug_draw(draw_options)
    
    # Отображение вектора скорости
    if mouse_pressed:
        pygame.draw.line(screen, (255, 0, 0), new_body.position, event.pos, 2)

        trajectory = [new_body.position]
        space_copy = space.copy()
        body_copy = new_body.copy()
        body_copy.velocity = pymunk.Vec2d(*event.pos) - pymunk.Vec2d(*new_body.position)
        space_copy.add(body_copy, pymunk.Circle(body_copy, body_radius))
        for n in range(1, 1000):
            space_copy.step(1/FPS)
            trajectory.append(body_copy.position)
        for i in range(len(trajectory) - 1):
            pygame.draw.line(screen, (100, 100, 255), trajectory[i], trajectory[i + 1], 2)


    
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
