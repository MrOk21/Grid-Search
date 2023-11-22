from os import truncate
import turtle
import heapq
import numpy as np

rows, cols = 10, 10
grid = np.zeros((rows, cols), dtype=int)

# Euristica da usare per A*
euclidean = True # Da scegliere se si vuole utilizzare la distanza euclidea
# euclidean = False # Da scegliere se si vuole utilizzare la distanza di manatthan

# Impostazioni Turtle
turtle.setup(width=800, height=600)
window = turtle.Screen()
window.title("A* Algorithm")
turtle.speed(0)

# Definisco i colori per i percorsi e per i nodi importanti
path_color = "blue"
color_visited_A_star = "green"
color_frontier = "gray"

# Dichiarazione degli insiemi per i punti
visited_nodes_A_star = set()  # Nodi visitati da A*
frontier_nodes = set()  # Nodi nella frontiera

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

# Funzione per evidenziare i nodi visitati da A*
def highlight_visited_A_star(color_visited_A_star):
    for node in visited_nodes_A_star:
        draw_point(node, color_visited_A_star)

# Funzione per evidenziare i nodi di frontiera
def highlight_frontier(color_frontier):
    for node in frontier_nodes:
        draw_point(node, color_frontier)

# Funzione per evidenziare i nodi esplorati (visitati e di frontiera)
def highlight_explored(color_explored):
    explored_nodes = visited_nodes_A_star | frontier_nodes
    for node in explored_nodes:
        draw_point(node, color_explored)

# Implementazione di A*
def a_star(grid, start, end):
    open_list = [(0, start)]  
    came_from = {}  
    g_score = {pos: float('inf') for pos in np.ndindex(grid.shape)} 
    g_score[start] = 0
    f_score = {pos: float('inf') for pos in np.ndindex(grid.shape)}
    
    if euclidean == True: 
        f_score[start] = euclidean_distance(start, end)
    else: 
        f_score[start] = manhattan_distance(start, end)

    while open_list:
        _, current = heapq.heappop(open_list)

        highlight_frontier(color_frontier)

        if current == end:
            path = reconstruct_path_A_star(came_from, current)
            visited_nodes_A_star.update(path)
            highlight_visited_A_star(color_visited_A_star)
            return path
            
        for direction in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            neighbor = (current[0] + direction[0], current[1] + direction[1])

            if not (0 <= neighbor[0] < grid.shape[0] and 0 <= neighbor[1] < grid.shape[1]) or grid[neighbor] == 1:
                continue

            tentative_g_score = g_score[current] + 1 

            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                if euclidean == True:
                    f_score[neighbor] = g_score[neighbor] + euclidean_distance(neighbor, end)
                else:
                    f_score[neighbor] = g_score[neighbor] + manhattan_distance(neighbor, end)
                heapq.heappush(open_list, (f_score[neighbor], neighbor))
                frontier_nodes.add(neighbor)
    return None

# Funzione euristica: Distanza Euclidea
def euclidean_distance(point1, point2):
    return np.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

# Funzione euristica: Distanza di Manatthan
def manhattan_distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return abs(x1 - x2) + abs(y1 - y2)

def reconstruct_path_A_star(came_from, current):
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    path.reverse()
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

# Eseguo A* e ottengo il percorso
path_a_star = a_star(grid, start_point, end_point)
print("Percorso A*:")
for step, point in enumerate(path_a_star):
    print(f"Passo {step + 1}: {point}")
draw_path(path_a_star, path_color, 100)

def close_window():
    turtle.bye()

# Configuro l'animazione affinchè si chiuda con il tasto ENTER
turtle.onkeypress(close_window, "Return")
turtle.listen()
turtle.mainloop()

