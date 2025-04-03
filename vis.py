import pygame

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
show_border = False

WHITE = (255, 255, 255)
RED = (255, 0, 0)
cell_size = 50
start_x, start_y = 200, 100
grid = [
        " │   │   │ ",
        "─┼───┼───┼─",
        " │       │ ",
        "─┼───┼─ ─┼─",
        "     │   │ ",
        "─┼─ ─┼───┼─",
        " │   │     ",
        "─┼───┼─ ─┼─",
        " │   │   │ ",
        "─┼─ ─┼───┼─",
        " │   │   │"
    ]       

def draw_numbers():
    font = pygame.font.Font(None, 24)  # Use default font with size 24

    # Draw column numbers below the grid
    for col_index in range(len(grid[0])):
        x = start_x + col_index * cell_size + cell_size // 2
        y = start_y + len(grid) * cell_size + 10
        text = font.render(str(col_index), True, WHITE)
        screen.blit(text, (x - text.get_width() // 2, y))

    # Draw row numbers to the left of the grid
    for row_index in range(len(grid)):
        x = start_x - 20
        y = start_y + row_index * cell_size + cell_size // 2
        text = font.render(str(row_index), True, WHITE)
        screen.blit(text, (x - text.get_width() // 2, y - text.get_height() // 2))

def draw_line(start, end):
    pygame.draw.line(screen, WHITE, start, end, 5)

def draw_track():
    for row_index, row in enumerate(grid):
        for col_index, char in enumerate(row):
            x = start_x + col_index * cell_size
            y = start_y + row_index * cell_size

            # Draw the cell border
            if show_border:
                pygame.draw.rect(screen, RED, (x, y, cell_size, cell_size), 1)

            # Draw the track elements
            if char == '─':  # Horizontal line
                draw_line((x, y + cell_size // 2), (x + cell_size, y + cell_size // 2))
            elif char == '│':  # Vertical line
                draw_line((x + cell_size // 2, y), (x + cell_size // 2, y + cell_size))
            elif char == '┼':  # Intersection
                # Draw both horizontal and vertical lines
                draw_line((x, y + cell_size // 2), (x + cell_size, y + cell_size // 2))  # Horizontal
                draw_line((x + cell_size // 2, y), (x + cell_size // 2, y + cell_size))  # Vertical

def draw_car(grid_x, grid_y, direction):
    # Calculate the center of the cell based on grid coordinates
    center_x = start_x + grid_x * cell_size + cell_size // 2
    center_y = start_y + grid_y * cell_size + cell_size // 2

    # Define the points of the triangle based on the direction
    if direction == "U":
        point1 = (center_x, center_y - cell_size // 3)  # Top point
        point2 = (center_x - cell_size // 3, center_y + cell_size // 3)  # Bottom-left point
        point3 = (center_x + cell_size // 3, center_y + cell_size // 3)  # Bottom-right point
    elif direction == "D":
        point1 = (center_x, center_y + cell_size // 3)  # Bottom point
        point2 = (center_x - cell_size // 3, center_y - cell_size // 3)  # Top-left point
        point3 = (center_x + cell_size // 3, center_y - cell_size // 3)  # Top-right point
    elif direction == "L":
        point1 = (center_x - cell_size // 3, center_y)  # Left point
        point2 = (center_x + cell_size // 3, center_y - cell_size // 3)  # Top-right point
        point3 = (center_x + cell_size // 3, center_y + cell_size // 3)  # Bottom-right point
    elif direction == "R":
        point1 = (center_x + cell_size // 3, center_y)  # Right point
        point2 = (center_x - cell_size // 3, center_y - cell_size // 3)  # Top-left point
        point3 = (center_x - cell_size // 3, center_y + cell_size // 3)  # Bottom-left point

    # Draw the triangle
    pygame.draw.polygon(screen, RED, [point1, point2, point3])

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.fill("black")
    draw_track()
    draw_numbers()
    draw_car(0,7,"R")
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
