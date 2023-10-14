import pygame
import sys
import random
import tkinter as tk
import tkinter.ttk as ttk
import time
import configparser

screen_width = 600
screen_height = 600

gridsize = 20
grid_width = screen_width // gridsize
grid_height = screen_height // gridsize

input_box = pygame.Rect(200,200,300,36)

text_color = (255, 255, 255)
light_green = (0, 170, 140)
dark_green = (0, 140, 120)
food_color = (250, 200, 0)
snake_color = (34, 34, 34)

up = (0, -1)
down = (0, 1)
right = (1, 0)
left = (-1, 0)
stop = (0, 0)

parser = configparser.ConfigParser ()
parser.read ("Snake_Game/Settings.cfg")

gamespeed = parser["Settings"].getint("gamespeed")
helpp = parser["Settings"].getint("helpp")

class Snake:
    def __init__(self):
        self.positions = [(screen_width // 2, screen_height // 2)]
        self.length = 1
        self.direction = stop
        self.color = snake_color
        self.score = 0

    def draw(self, surface):
        for p in self.positions:
            rect = pygame.Rect((int(p[0]), int(p[1])), (gridsize, gridsize))
            pygame.draw.rect(surface, self.color, rect)

    def move(self):
        current = self.positions[0]
        x, y = self.direction
        global new
        new = ((current[0] + (x * gridsize)) % screen_width, (current[1] + (y * gridsize)) % screen_height)

        if not new in self.positions[2:]:

            self.positions.insert(0, new)
            
            if len(self.positions) > self.length:
                self.positions.pop()

    def reset(self):
        self.length = 1
        self.positions = [(screen_width // 2, screen_height // 2)]
        self.direction = stop
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
    
    if new in snake.positions[2:] :
        return True

    return False

def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    window.geometry(f"{width}x{height}+{x}+{y}")

def Menu () :
    def update_speed_info_label():
        if gamespeed == 3:
            speedinfo = "easy"
        elif gamespeed == 10:
            speedinfo = "normal"
        elif gamespeed == 20:
            speedinfo = "hard"
        
        setting_info_s.config(text=f"gamespeed = {speedinfo}")
    
    def update_sf_info_label():   
        if helpp == 0 :
            fixedinfo = "no"
        elif helpp == 1 :
            fixedinfo = "yes"
        
        setting_info_sf.config(text=f"speedfixed = {fixedinfo}")

    def Gamespeed_easy () :
        global gamespeed
        gamespeed = 3
        
        parser.set ("Settings", "gamespeed", "3")
        with open ("Settings.cfg", "w") as dosya :
            parser.write (dosya)
        menu.update ()

    def Gamespeed_normal () :
        global gamespeed
        gamespeed = 10
        
        parser.set ("Settings", "gamespeed", "10")
        with open ("Settings.cfg", "w") as dosya :
            parser.write (dosya)

    def Gamespeed_hard () :
        global gamespeed
        gamespeed = 20
        
        parser.set ("Settings", "gamespeed", "20")
        with open ("Settings.cfg", "w") as dosya :
            parser.write (dosya)

    def speedfixed () :
        global helpp
        helpp = 1
        
        parser.set ("Settings", "helpp", "1")
        with open ("Settings.cfg", "w") as dosya :
            parser.write (dosya)

    def speedup () :
        global gamespeed
        global helpp
        helpp = 0 
        gamespeed += 1
        
        parser.set ("Settings", "helpp", "0")
        with open ("Settings.cfg", "w") as dosya :
            parser.write (dosya)

        return
    def close_window():
        menu.destroy ()

    def quit_window():
        pygame.quit ()
        sys.exit ()

    menu = tk.Tk()
    menu.title("Game Menu")
    menu.resizable (width=False, height=False)

    window_width = 250
    window_height = 260

    center_window(menu, window_width, window_height)

    frame = tk.Frame(menu)
    frame.pack()

    title = ttk.Label(frame, text="Snake Games", font='arial')
    title.pack()
    title = ttk.Label(frame, text="------------------------", font='arial')
    title.pack()
    title = ttk.Label(frame, text="Game Difficulty", font='arial')
    title.pack()

    difficulty_frame = tk.Frame(frame)
    difficulty_frame.pack()

    button_easy = ttk.Button(difficulty_frame, text="Easy", command=lambda: [Gamespeed_easy(), update_speed_info_label()])
    button_normal = ttk.Button(difficulty_frame, text="Normal", command=lambda: [Gamespeed_normal(), update_speed_info_label()])
    button_hard = ttk.Button(difficulty_frame, text="Hard", command=lambda: [Gamespeed_hard(), update_speed_info_label()])

    button_easy.pack(side="left")
    button_normal.pack(side="left")
    button_hard.pack(side="left")

    title = tk.Label(frame, text="------------------------", font='arial')
    title.pack()

    title = tk.Label(frame, text="Speed Fixed", font='arial')
    title.pack()

    play_frame = tk.Frame(frame) 
    play_frame.pack() 

    button_yes = ttk.Button(play_frame, text="yes", command=lambda: [speedfixed(), update_sf_info_label()])
    button_no = ttk.Button(play_frame, text="no", command=lambda: [speedup(), update_sf_info_label()])

    button_yes.pack(side="left")
    button_no.pack(side="left")

    title = tk.Label(frame, text="------------------------", font='arial')
    title.pack()

    window_frame = tk.Frame ()
    window_frame.pack ()

    close_button = ttk.Button(window_frame, text="Game Start", command=close_window)
    close_button.pack(side="left")
    quit_button = ttk.Button(window_frame, text="Quit Game", command=quit_window)
    quit_button.pack(side="right")

    global speedinfo
    global fixedinfo
    
    if gamespeed == 3:
        speedinfo = "easy"
    elif gamespeed == 10:
        speedinfo = "normal"
    elif gamespeed == 20:
        speedinfo = "hard"
        
    if helpp == 1 :
        fixedinfo = "yes"
    elif helpp == 0 :
        fixedinfo = "no"

    setting_info_s = tk.Label (menu, text = f"gamespeed = {speedinfo}")
    setting_info_s.pack()
    setting_info_sf = tk.Label (menu, text = f"speedfixed = {fixedinfo}")
    setting_info_sf.pack()

    menu.mainloop()

def Game():
    Menu ()
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
            time.sleep (0.3)
            pygame.display.update()
            Menu ()
            snake.reset()
            food.random_position()

if __name__ == "__main__":
    Game()
