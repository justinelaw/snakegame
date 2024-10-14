from tkinter import *
#from tkinter import messagebox
import random

ROWS = 25
COLUMNS = 25
TILE_SIZE = 25

WIN_WIDTH = TILE_SIZE * COLUMNS
WIN_HEIGHT = TILE_SIZE * ROWS

SNAKE_COLOR = "#008000"
FOOD_COLOR = "#DE3163"


class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        canvas.create_rectangle(x, y, x+TILE_SIZE, y+TILE_SIZE, fill=SNAKE_COLOR)


class Food:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        canvas.create_oval(x, y, x+TILE_SIZE, y+TILE_SIZE, fill=FOOD_COLOR)

def move():
    global snake, snake_body, food, snake_x, snake_y, food_x, food_y, score, game_over

    if (snake_x < 0 or snake_y < 0 or snake_x >= WIN_WIDTH or snake_y >= WIN_HEIGHT):
        game_over = True
        return

    if (snake_x == food_x and snake_y == food_y):
        snake_body.append(Tile(food_x, food_y))
        food_x, food_y = getPosition()
        food = Food(food_x,food_y)
        score += 1


    for i in range(len(snake_body)-1, -1, -1):
        tile = snake_body[i]
        if (i==0):
            tile.x = snake.x
            tile.y = snake.y
        else:
            prev_tile = snake_body[i-1]
            tile.x = prev_tile.x
            tile.y = prev_tile.y

    snake_x += vel_x * TILE_SIZE
    snake_y += vel_y * TILE_SIZE
    



def getPosition():
        rand_x = random.randrange(0, ROWS-1) * TILE_SIZE
        rand_y = random.randrange(0, COLUMNS-1) * TILE_SIZE
        return rand_x, rand_y

#e = event
def change_direction(e):
    global vel_x, vel_y
    if (e.keysym == "Up" and vel_y != 1):
        vel_x, vel_y = 0, -1
    elif (e.keysym == "Down" and vel_y != -1):
        vel_x = 0
        vel_y = 1
    elif (e.keysym == "Left" and vel_x != 1):
        vel_x = -1
        vel_y = 0
    elif (e.keysym == "Right" and vel_x != -1):
        vel_x, vel_y = 1, 0

if __name__ == "__main__":
    window = Tk()
    window.title("Snake")
    window.resizable(False, False)

    #Canvas(master, width, height, background)
    global canvas
    canvas = Canvas(window, width=WIN_WIDTH, height=WIN_HEIGHT, bg="black", borderwidth=0, highlightthickness=0)
    canvas.pack()
    window.update()

    #we have an issue where the window keeps popping up in a different place 
    # (or in my case with the macOS it pops up on the left side)
    #I want the window to pop up in the middle of the screen
    #current geometry is 625x625+5+30

    window_width = window.winfo_width()
    window_height = window.winfo_height()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    window.geometry(newGeometry="625x625-5+30")

    window_x = int((screen_width/2) - (window_width/2))
    window_y = int((screen_height/2) - (window_height/2))

    window.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")

    #initialize snake
    snake_x, snake_y = getPosition()
    snake_body = []

    #initialize food
    food_x, food_y = getPosition()
    #check that food is not where the snake head is
    while ((food_x==snake_x) & (food_y==snake_y)):
        food_x, food_y = getPosition()
    food = Food(food_x, food_y)

    vel_x = 0
    vel_y = 0

    score = 0
    game_over = False


    def draw():
        global snake, score, game_over
        move()
        canvas.delete("all")
        snake = Tile(snake_x, snake_y)
        Food(food_x, food_y)
        for tile in snake_body:
            canvas.create_rectangle(tile.x, tile.y, tile.x + TILE_SIZE, tile.y + TILE_SIZE, fill =  SNAKE_COLOR)
        if game_over == True:
            canvas.create_rectangle(WIN_WIDTH/4, WIN_HEIGHT/4, WIN_WIDTH*3 /4, WIN_HEIGHT*3 /4, fill= 'red')
            canvas.create_text(WIN_WIDTH/2, WIN_HEIGHT/2, font = "Arial 30", text = f"Game Over. Score: {score}", fill= "black")
            exit
        canvas.create_text(50, 30, font = "Arial 20", text = f"Score: {score}", fill = "white")
        window.after(100, draw)


    draw() 

    window.bind("<KeyRelease>", change_direction)


    window.mainloop()

    

