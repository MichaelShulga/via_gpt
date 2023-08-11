import pygame
import numpy as np
import time

# Initialize Pygame
pygame.init()

# Window dimensions
width, height = 250, 250
screen = pygame.display.set_mode((width, height))

# Mandelbrot parameters
xmin, xmax = -2.0, 1.0
ymin, ymax = -1.5, 1.5
max_iter = 100

# Precompute color values
color_values = np.linspace(0, 255, max_iter)

def calculate_mandelbrot(x, y):
    zx, zy = x * (xmax - xmin) / (width - 1) + xmin, y * (ymax - ymin) / (height - 1) + ymin
    c = zx + zy * 1j
    z = c
    for i in range(max_iter):
        if abs(z) > 2.0:
            return i
        z = z * z + c
    return max_iter - 1

# Keyboard navigation variables
zoom_factor = 0.1
pan_factor = 0.1

# Main loop
running = True
while running:
    start_time = time.time()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:  # Scroll up to zoom in
                dx = (xmax - xmin) * zoom_factor
                dy = (ymax - ymin) * zoom_factor
                xmin += dx
                xmax -= dx
                ymin += dy
                ymax -= dy
            elif event.button == 5:  # Scroll down to zoom out
                dx = (xmax - xmin) * zoom_factor
                dy = (ymax - ymin) * zoom_factor
                xmin -= dx
                xmax += dx
                ymin -= dy
                ymax += dy

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:  # Pan left
                dx = (xmax - xmin) * pan_factor
                xmin -= dx
                xmax -= dx
            elif event.key == pygame.K_RIGHT:  # Pan right
                dx = (xmax - xmin) * pan_factor
                xmin += dx
                xmax += dx
            elif event.key == pygame.K_UP:  # Pan up
                dy = (ymax - ymin) * pan_factor
                ymin -= dy
                ymax -= dy
            elif event.key == pygame.K_DOWN:  # Pan down
                dy = (ymax - ymin) * pan_factor
                ymin += dy
                ymax += dy

    for x in range(width):
        for y in range(height):
            iterations = calculate_mandelbrot(x, y)
            color_value = color_values[iterations]
            screen.set_at((x, y), (int(color_value), int(color_value), int(color_value)))

    pygame.display.flip()

# Pygame shutdown
pygame.quit()
