from os import truncate
import turtle
import heapq
import numpy as np
import math

rows, cols = 10, 10
grid = np.zeros((rows, cols), dtype=int)

# Impostazioni Turtle
turtle.setup(width=800, height=600)
window = turtle.Screen()
window.title("Theta* Algorithm")
turtle.speed(0)

# Definisco i colori per i percorsi e per i nodi importanti
path_theta_color = "red"
color_visited_Theta_star = "purple"
color_visibility = "yellow"

# Dichiarazione degli insiemi per i punti
visited_nodes_Theta_star = set()  # Nodi visitati da Theta*
visibility_nodes = set()  # Nodi di visibilità 

# Funzione per disegnare la griglia
def draw_grid(rows, cols):
    turtle.penup()
    for row in range(rows):
        for col in range(cols):
            x = col * 30 - (cols * 15)
            y = -(row * 30 - (rows * 15))
            turtle.goto(x, y)
            turtle.pendown()
            for _ in range(4):
                turtle.forward(30)
                turtle.right(90)
            turtle.penup()

# Funzione per disegnare un percorso
def draw_path(path, color, delay):
    turtle.penup()
    turtle.color(color)
    turtle.pensize(2)
    for node in path:
        x, y = node
        x = x * 30 - (cols * 15)
        y = -(y * 30 - (rows * 15))
        turtle.goto(x, y)
        turtle.pendown()
        turtle.delay(delay) 
    turtle.penup()

def is_valid(x, y):
    return 0 <= x < len(grid) and 0 <= y < len(grid[0]) and grid[x][y] == 0

# Funzione per evidenziare i nodi visitati da Theta*
def highlight_visited_Theta_star(color_visited_Theta_star):
    for node in visited_nodes_Theta_star:
        draw_point(node, color_visited_Theta_star)

# Funzione per evidenziare i nodi di visibilità
def highlight_visibility(color_visibility):
    for node in visibility_nodes:
        draw_point(node, color_visibility)

# Implementazione di Theta*
def theta_star(grid, start, goal):
    open_set = {start}
    came_from = {}
    movements = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    g_score = {(x, y): float('inf') for x in range(len(grid)) for y in range(len(grid[0])) if grid[x][y] == 0}
    g_score[start] = 0

    f_score = {pos: float('inf') for row in grid for pos in row}
    f_score[start] = line_of_sight(start, goal, grid)

    while open_set:
        current = min(open_set, key=lambda pos: f_score[pos])

        highlight_visibility(color_visibility)

        if current == goal:
            path = reconstruct_path_Theta_star(came_from, current)
            visited_nodes_Theta_star.update(path)
            visibility_nodes.update(path)
            highlight_visited_Theta_star(color_visited_Theta_star)
            return path

        open_set.remove(current)

        for dx, dy in movements:
            neighbor = (current[0] + dx, current[1] + dy)
            if is_valid(neighbor[0], neighbor[1]):
                tentative_g_score = g_score[current] + line_of_sight(current, neighbor, grid)
        
                if tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = g_score[neighbor] + line_of_sight(neighbor, goal, grid)
                
                    if neighbor not in open_set:
                        open_set.add(neighbor)
                        visibility_nodes.add(neighbor)

    return None

# Funzione euristica: Line of sight
def line_of_sight(current, goal, grid):
    x1, y1 = current
    x2, y2 = goal
    dx = x2 - x1
    dy = y2 - y1
    distance = math.sqrt(dx ** 2 + dy ** 2)

    if dx == 0:
        step_x = 0
        step_y = 1 if dy > 0 else -1
    elif dy == 0:
        step_x = 1 if dx > 0 else -1
        step_y = 0
    else:
        gcd = math.gcd(dx, dy)
        step_x = dx // gcd
        step_y = dy // gcd

    x, y = x1, y1
    while x != x2 or y != y2:
        if not (0 <= x < len(grid) and 0 <= y < len(grid[0])):
            return float('inf')

        if grid[x][y] == 1:
            return float('inf')

        x += step_x
        y += step_y
    return distance

def reconstruct_path_Theta_star(came_from, current):
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.insert(0, current)
    return path
    
def draw_point(point, color):
    turtle.penup()
    turtle.color(color)
    x, y = point
    x = x * 30 - (cols * 15)
    y = -(y * 30 - (rows * 15))
    turtle.goto(x, y)
    turtle.dot(10) 
    turtle.penup()

start_point = (0, 0)  
end_point = (rows - 1, cols - 1) 

# Configuro la griglia
draw_grid(rows, cols)
draw_point(start_point, "green")
draw_point(end_point, "red")

# Eseguo Theta* e ottengo il percorso
path_theta_star = theta_star(grid, start_point, end_point)
print("Percorso Theta*:")
for step, point in enumerate(path_theta_star):
    print(f"Passo {step + 1}: {point}")
draw_path(path_theta_star, path_theta_color, 100)

def close_window():
    turtle.bye()

# Configuro l'animazione affinchè si chiuda con il tasto ENTER
turtle.onkeypress(close_window, "Return")
turtle.listen()
turtle.mainloop()

