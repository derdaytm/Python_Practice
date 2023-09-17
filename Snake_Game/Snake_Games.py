import pygame
import sys
import random
import tkinter as tk

screen_width = 600
screen_height = 600

gridsize = 20
grid_width = screen_width // gridsize
grid_height = screen_height // gridsize

light_green = (0, 170, 140)
dark_green = (0, 140, 120)
food_color = (250, 200, 0)
snake_color = (34, 34, 34)

up = (0, -1)
down = (0, 1)
right = (1, 0)
left = (-1, 0)

class Snake:
    def __init__(self):
        self.positions = [(screen_width // 2, screen_height // 2)]
        self.length = 1
        self.direction = random.choice([up, down, right, left])
        self.color = snake_color
        self.score = 0

    def draw(self, surface):
        for p in self.positions:
            rect = pygame.Rect((int(p[0]), int(p[1])), (gridsize, gridsize))
            pygame.draw.rect(surface, self.color, rect)

    def move(self):
        current = self.positions[0]
        x, y = self.direction
        new = ((current[0] + (x * gridsize)) % screen_width, (current[1] + (y * gridsize)) % screen_height)

        if new in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0, new)
            
            if len(self.positions) > self.length:
                self.positions.pop()

    def reset(self):
        self.length = 1
        self.positions = [(screen_width // 2, screen_height // 2)]
        self.direction = random.choice([up, down, right, left])
        self.score = 0

    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.turn(up)
                
                elif event.key == pygame.K_DOWN:
                    self.turn(down) 
                
                elif event.key == pygame.K_RIGHT:
                    self.turn(right)             
                
                elif event.key == pygame.K_LEFT:
                    self.turn(left)

    def turn(self, direction):
        if (direction[0] * -1, direction[1] * -1) == self.direction:
            return
        
        else:
            self.direction = direction

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = food_color
        self.random_position()

    def random_position(self):
        self.position = (random.randint(0, grid_width - 1) * gridsize, random.randint(0, grid_height - 1) * gridsize)

    def draw(self, surface):
        rect = pygame.Rect((self.position[0], self.position[1]), (gridsize, gridsize))
        pygame.draw.rect(surface, self.color, rect)

def drawGrid(surface):
    for y in range(0, int(grid_height)):
        for x in range(0, int(grid_width)):
            if (x + y) % 2 == 0:
                light = pygame.Rect((x * gridsize, y * gridsize), (gridsize, gridsize))
                pygame.draw.rect(surface, light_green, light)
            
            else:
                dark = pygame.Rect((x * gridsize, y * gridsize), (gridsize, gridsize))
                pygame.draw.rect(surface, dark_green, dark)

def is_game_over(snake):
    head = snake.positions[0]  
    
    for segment in snake.positions[1:]:
        if head == segment:
            return True
    
    if (head[0] < 0 or head[0] >= screen_width
            or head[1] < 0 or head[1] >= screen_height):
        return True
    
    return False

def Gamespeed_easy () :
    global gamespeed
    gamespeed = 3

def Gamespeed_normal () :
    global gamespeed
    gamespeed = 10

def Gamespeed_hard () :
    global gamespeed
    gamespeed = 20

def close_window():
    menu.destroy()

def speedfixed () :
    global helpp
    helpp = 1

def speedup () :
    global gamespeed
    global helpp
    helpp = 0 
    gamespeed += 1
    return

def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    window.geometry(f"{width}x{height}+{x}+{y}")

menu = tk.Tk()
menu.title("Game Menu")

window_width = 200
window_height = 200

center_window(menu, window_width, window_height)

frame = tk.Frame(menu)
frame.pack()

title = tk.Label(frame, text="Snake Games", font='arial')
title.pack()
title = tk.Label(frame, text="------------------------", font='arial')
title.pack()
title = tk.Label(frame, text="Game Difficulty", font='arial')
title.pack()

difficulty_frame = tk.Frame(frame)
difficulty_frame.pack()

button_easy = tk.Button(difficulty_frame, text="Easy", command=Gamespeed_easy)
button_normal = tk.Button(difficulty_frame, text="Normal", command=Gamespeed_normal)
button_hard = tk.Button(difficulty_frame, text="Hard", command=Gamespeed_hard)

button_easy.pack(side="left")
button_normal.pack(side="left")
button_hard.pack(side="left")

title = tk.Label(frame, text="------------------------", font='arial')
title.pack()

title = tk.Label(frame, text="Speed Fixed", font='arial')
title.pack()

play_frame = tk.Frame(frame) 
play_frame.pack()

button_yes = tk.Button(play_frame, text="yes", command=speedfixed)
button_no = tk.Button(play_frame, text="no", command=speedup)

button_yes.pack(side="left")
button_no.pack(side="left")

close_button = tk.Button(menu, text="Game Start", command=close_window)
close_button.pack()

menu.mainloop()

def Game():
    global helpp
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arial black", 20)
    surface = pygame.Surface(screen.get_size())
    surface = surface.convert() 

    snake = Snake()
    food = Food()
    
    while True:
        clock.tick(gamespeed)
        snake.handle_keys()
        snake.move()
        drawGrid(surface)

        if snake.positions[0] == food.position:
            snake.length += 1
            snake.score += 1
            food.random_position()
            if helpp == 0 :
                speedup ()
                helpp == 0
                

        snake.draw(surface)
        food.draw(surface)
        screen.blit(surface, (0, 0))
        score_text = font.render(f"Score: {snake.score}", True, (0, 0, 0))
        screen.blit(score_text, (265, 10))
        pygame.display.update()
        
        if is_game_over(snake):
            game_over_text = font.render("Game Over! Play again? (Y/N)", True, (255, 0, 0))
            screen.blit(game_over_text, (200, 300))
            pygame.display.update()

            waiting_for_input = True
            while waiting_for_input:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_y:
                            snake.reset()
                            food.random_position()
                            waiting_for_input = False
                        
                        elif event.key == pygame.K_n:
                            pygame.quit()
                            sys.exit()

if __name__ == "__main__":
    Game()
