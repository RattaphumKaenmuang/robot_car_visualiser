import pygame

SHOW_BORDER = False
MANUAL_CONTROL = False

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

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
grid_size_x = len(grid[0])
grid_size_y = len(grid)

def out_of_bound(grid_x, grid_y):
    return not(0 <= grid_x < grid_size_x and 0 <= grid_y < grid_size_y)

def whitespace_hit(grid_x, grid_y):
    return grid[grid_y][grid_x] == " "

class Car:
    def __init__(self, grid_x, grid_y, dir_str):
        self.grid_x = grid_x
        self.grid_y = grid_y
        
        if dir_str == "U":
            self.dir = (0, -1)
        elif dir_str == "R":
            self.dir = (1, 0)
        elif dir_str == "D":
            self.dir = (0, 1)
        elif dir_str == "L":
            self.dir = (-1, 0)
        
    def dir_to_str(self):
        strng = None
        if self.dir == (0, -1):
            strng = "U"
        elif self.dir == (1, 0):
            strng = "R"
        elif self.dir == (0, 1):
            strng = "D"
        elif self.dir == (-1, 0):
            strng = "L"
        
        # print(f"vec = {self.dir}, dir = {strng}")
        return strng

    def get_rel_dir(self, dir_str):
        if dir_str == "R":
            return (self.dir[1]*-1, self.dir[0])
        elif dir_str == "L":
            return (self.dir[1], self.dir[0]*-1)
    
    def turn(self, dir_str):
        self.dir = self.get_rel_dir(dir_str)

    def u_turn(self):
        self.dir = (self.dir[0] * -1, self.dir[1] * -1)
        
    def go(self):
        new_grid_x = self.grid_x + self.dir[0]
        new_grid_y = self.grid_y + self.dir[1]

        if out_of_bound(new_grid_x, new_grid_y) or whitespace_hit(new_grid_x, new_grid_y):
            raise ValueError("Car tried to move into empty space.")
        else:
            self.grid_x = new_grid_x
            self.grid_y = new_grid_y

class Simulation:
    def __init__(self, car, start_grid, goal_grid):
        self.car = car
        self.start_grid = start_grid
        self.goal_grid = goal_grid
        self.turns = []
        self.step = 0

        self.turned_at_intersection = False
        self.goal_reached = False
        self.backtracking_finished = False
    
    def progress_steps(self):
        self.step += 1
        new_grid_x = self.car.grid_x + car.dir[0]
        new_grid_y = self.car.grid_y + car.dir[1]
        cur_tile = grid[self.car.grid_y][self.car.grid_x]

        if not self.goal_reached:
            if (self.car.grid_x, self.car.grid_y) == self.goal_grid:
                self.goal_reached = True
                return
            
            if out_of_bound(new_grid_x, new_grid_y) or whitespace_hit(new_grid_x, new_grid_y) and self.turns:
                self.car.u_turn()
                self.turns.pop()
            elif cur_tile == "┼" and not self.turned_at_intersection:
                self.car.turn("R")
                self.turned_at_intersection = True
                self.turns.append("R")
            elif cur_tile == "┼":
                self.car.go()
                self.turned_at_intersection = False
            else:
                self.car.go()
            
        else:
            pass

        print(self.turns)
            

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
            if SHOW_BORDER:
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
    elif direction == "R":
        point1 = (center_x + cell_size // 3, center_y)  # Right point
        point2 = (center_x - cell_size // 3, center_y - cell_size // 3)  # Top-left point
        point3 = (center_x - cell_size // 3, center_y + cell_size // 3)  # Bottom-left point
    elif direction == "D":
        point1 = (center_x, center_y + cell_size // 3)  # Bottom point
        point2 = (center_x - cell_size // 3, center_y - cell_size // 3)  # Top-left point
        point3 = (center_x + cell_size // 3, center_y - cell_size // 3)  # Top-right point
    elif direction == "L":
        point1 = (center_x - cell_size // 3, center_y)  # Left point
        point2 = (center_x + cell_size // 3, center_y - cell_size // 3)  # Top-right point
        point3 = (center_x + cell_size // 3, center_y + cell_size // 3)  # Bottom-right point

    # Draw the triangle
    pygame.draw.polygon(screen, RED, [point1, point2, point3])

start = (0, 7)
goal = (10, 1)
car = Car(start[0], start[1], "R")  # Initialize the car at grid position (0, 7) facing right
sim = Simulation(car, start, goal)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYUP:
            if MANUAL_CONTROL:
                if event.key == pygame.K_RIGHT:
                    car.turn("R")
                elif event.key == pygame.K_LEFT:
                    car.turn("L")
                elif event.key == pygame.K_SPACE:
                    try:
                        car.go()
                    except ValueError as e:
                        print(e)

            elif event.key == pygame.K_SPACE:
                sim.progress_steps()

    screen.fill("black")
    draw_track()
    draw_numbers()
    draw_car(car.grid_x, car.grid_y, car.dir_to_str())  # Draw the car
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
