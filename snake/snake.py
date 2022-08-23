import pygame 
import random
from enum import Enum

pygame.init()
# set the font for pygame
font = pygame.font.SysFont('arial', 24)
pygame.display.set_caption("Snake")

# define color constants
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0,0,0)
GRAY = (30,30,30)
RED = (255, 0, 0)

SPEED = 7
CELL = 16 # all moves will be CELL based 
GAP = 1

class Grid:
    def __init__(s, w=640, h=480, cell=CELL):
        s.cell_size = cell
        s.width = (w // cell) * cell  # make the width multiple of the cell size
        s.height = (h // cell) * cell
        s.x_vertices = range(0, s.width, s.cell_size) 
        s.y_vertices = range(0, s.height, s.cell_size)

class Vertex:
    '''a vertex represents the top left corner of a square'''
    def __init__(s, x, y ):
        s.x = x 
        s.y = y  
        # print(s)
    def __add__(s, p):
        return Vertex( s.x  + p.x , s.y + p.y)
    def __sub__(s, p):
        return Vertex( s.x  - p.x, s.y - p.y) 
    def __eq__(s, p):
        if not isinstance(p, Vertex):
            # don't compare againt unrelated types
            return NotImplemented
        return s.x == p.x and s.y == p.y
    def __repr__(s):
        return f'Vertex{s.x, s.y}'

class Direction():
    def __init__(s, cell_size):
        s.RIGHT = Vertex(cell_size, 0)
        s.LEFT  = Vertex(-cell_size, 0)
        s.DOWN  = Vertex(0, cell_size)
        s.UP    = Vertex(0, -cell_size)

class Snake:
    def __init__(s, grid):
        s.w = grid.width
        s.h = grid.height 
        s.cz = grid.cell_size
        s.grid = grid
        s.direction = Direction(s.cz)

        # set initial game state
        s.head =  Vertex(s.w//2, s.h//2)
        s.snake = [s.head, s.head - Vertex(s.cz, 0) , s.head - Vertex(2*s.cz, 0)]
        s.step = s.direction.RIGHT
        s.score = 0 
        s.food = s._gen_food()

    def _gen_food(s):
        food_v = Vertex( random.choice(s.grid.x_vertices),  random.choice(s.grid.y_vertices))
        print(food_v)
        if food_v in s.snake:
            # if food_v is on the snake generate a new food_v
            s._gen_food()
        return food_v
        
    def _handle_user_input(s):
        '''This method handles user input'''
        for event in pygame.event.get():
            # pygame.QUIT event happens when the user click on the window closing button 
            if event.type == pygame.QUIT:
                pygame.quit()   # quit pygame

            # check if a key is pressed 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    s.step = s.direction.LEFT
                elif event.key == pygame.K_RIGHT:
                    s.step = s.direction.RIGHT
                elif event.key == pygame.K_DOWN:
                    s.step = s.direction.DOWN
                elif event.key == pygame.K_UP:
                    s.step = s.direction.UP
    
    def move_snake(s):
        s._handle_user_input()
        s.head += s.step
        s.snake.insert(0, snake.head)
        if not snake.there_is_food():
            snake.snake.pop()   

    def there_is_food(s):
        if s.head == s.food:
            s.score +=1
            print(s.score)
            s.food = s._gen_food()
            return True
        return False 

    def snake_died(s):
        died =False
        if s.head.x > s.grid.x_vertices[-1]  or s.head.y > s.grid.y_vertices[-1]  or s.head.x < 0 or s.head.y < 0 :
            died  = True
        elif s.head in s.snake[1:]:
            died  = True
        return died  

class Window:
    def __init__(s, grid, snake):
        s.snake = snake   
        s.grid = grid
        s.cz = grid.cell_size    
        s.w = grid.width
        s.h = grid.height
        s.display = pygame.display.set_mode((s.w, s.h ))
        s.clock = pygame.time.Clock()

    def draw_grid(s, vertex=False):
        for i in s.grid.x_vertices:
            for j in s.grid.y_vertices:
                rect = (i, j, s.cz-1, s.cz-1)
                pygame.draw.rect(s.display, (BLACK), rect)
                if vertex:
                    vertex_point = (i, j, 2, 2)
                    pygame.draw.rect(s.display, RED, vertex_point)

    def update(s):
        s.display.fill(GRAY)
        s.draw_grid(True)
        for pt in s.snake.snake:
            pygame.draw.rect(s.display, WHITE, pygame.Rect(pt.x, pt.y, s.cz-GAP, s.cz-GAP))
        text = font.render(f"Score: {s.snake.score}", True, WHITE)
        s.display.blit(text, [0,0])
        pygame.draw.rect(s.display, GREEN, pygame.Rect(s.snake.food.x, s.snake.food.y, s.cz, s.cz))
        s.clock.tick(SPEED)
        pygame.display.flip()

if __name__ == '__main__':
    num_lives = 9
    for _ in range(num_lives):
        grid = Grid()
        snake = Snake(grid)
        window = Window(grid, snake)
        while not snake.snake_died():  
            snake.move_snake()
            window.update()

        print('Snake died!')
    print('Game is over!')
    pygame.quit()
    quit()
