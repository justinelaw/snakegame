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

class Snake:
    def __init__(self, x, y):
        body = []
        head = Tile(x, y)
        self.head = head
        self.body = body.append(self.head)
    def add():
        pass
    def move():
        pass

class Food:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        canvas.create_oval(x, y, x+TILE_SIZE, y+TILE_SIZE, fill=FOOD_COLOR)


def getPosition():
        rand_x = random.randrange(0, ROWS-1) * TILE_SIZE
        rand_y = random.randrange(0, COLUMNS-1) * TILE_SIZE
        return rand_x, rand_y

def change_direction(e):
    print(e.keysym)

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
    snake = Snake(snake_x, snake_y)

    #initialize food
    food_x, food_y = getPosition()
    #check that food is not where the snake head is
    while ((food_x==snake_x) & (food_y==snake_y)):
        food_x, food_y = getPosition()
    food = Food(food_x, food_y)

    #set velocities for keyListener
    vel_x = ""
    vel_y = ""

    window.bind("<KeyRelease>", change_direction)


    window.mainloop()

    #messagebox.showinfo(message='Have a good day')

