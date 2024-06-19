import time
import pygame
import numpy as np
# initialising constants
COLOR_BG = (10, 10, 10,)
COLOR_GRID = (40, 40, 40)
COLOR_DIE = (170, 170, 170)
COLOR_ALIVE = (255, 255, 255)

pygame.init()
pygame.display.set_caption("Conway's Game of Life")
# function which updates the screen with each generation of the game
def update(screen, cells, size, with_progress=False):
    updated_cells = np.zeros((cells.shape[0], cells.shape[1]))

    for row, col in np.ndindex(cells.shape):
        alive = np.sum(cells[row-1:row+2, col-1:col+2]) - cells[row, col]
        color = COLOR_BG if cells[row, col] == 0 else COLOR_ALIVE

        if cells[row, col] == 1:
            if alive < 2 or alive > 3:
                if with_progress:
                    color = COLOR_DIE
            elif 2 <= alive <= 3:
                updated_cells[row, col] = 1
                if with_progress:
                    color = COLOR_ALIVE
        else:
            if alive == 3:
                updated_cells[row, col] = 1
                if with_progress:
                    color = COLOR_ALIVE

        pygame.draw.rect(screen, color, (col * size, row * size, size - 1, size - 1))

    return updated_cells

def main():
    pygame.init()

    # takes input from user for height and width
    w = int(input("Enter Width: "))
    h = int(input("Enter Height: "))
    screen = pygame.display.set_mode((w, h))
    cells = np.zeros((h // 10, w // 10))
    screen.fill(COLOR_GRID)
    update(screen, cells, 10)

    pygame.display.flip()
    pygame.display.update()

    running = False # solves the same purpose
    paused = False

    clock = pygame.time.Clock()
    #main loop which controls the flow of the simulation
    while True:
        for Q in pygame.event.get():
            if Q.type == pygame.QUIT:
                pygame.quit()
                return
            elif Q.type == pygame.KEYDOWN:
                if Q.key == pygame.K_SPACE: #space bar starts the simulation and pauses it too
                    running = not running
                    paused = False
                    update(screen, cells, 10)
                    pygame.display.update()
                elif Q.key == pygame.K_r: # R sets random pattern to start with
                    cells = np.random.randint(2, size=(h // 10, w // 10))
                    update(screen, cells, 10)
                    pygame.display.update()
                elif Q.key == pygame.K_s: # S helps to stop the simulation
                    running = False
                    paused = False
                    cells = np.zeros((h // 10, w // 10))
                    update(screen, cells, 10)
                    pygame.display.update()
                elif Q.key == pygame.K_p: # P is used to toggle paused state
                    paused = not paused

            if pygame.mouse.get_pressed()[0]: #turns cells alive
                pos = pygame.mouse.get_pos()
                cells[pos[1] // 10, pos[0] // 10] = 1
                update(screen, cells, 10)
                pygame.display.update()

        screen.fill(COLOR_GRID)

        if running and not paused:
            cells = update(screen, cells, 10, with_progress=True)
            pygame.display.update()

        clock.tick(4)  # controlled simulation speed

if __name__ == "__main__":
    main()
