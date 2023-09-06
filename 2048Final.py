import pygame as pg
import time
import random

WINDOW_WIDTH = WINDOW_HEIGHT = 480
board = [[None, None, None, None], [None, None, None, None], [None, None, None, None], [None, None, None, None]]

class Square:
    def __init__(self, x_pos, y_pos, value = 0):
        self.x = x_pos
        self.y = y_pos
        if value == 0:
            self.value = self.value()
        else:
            self.value = value
        
    def value(self):
        rand = random.random()
        if(rand <= 0.9):
            return 2
        else:
            return 4
    
    def change_position(self, x, y):
        self.x = x
        self.y = y

    def get_X_pos(self):
        return self.x
    
    def get_Y_pos(self):
        return self.y
    
    def get_value(self):
        return self.value
    
    def __add__(self, other):
        return Square(self.x, self.y, self.value + other.value)
      
    def __str__(self):
        return f"{self.value}"

def main():
    pg.init()
    global SCREEN
    SCREEN = pg.display.set_mode((WINDOW_HEIGHT, WINDOW_WIDTH))     
    
    generate_box()
    generate_box()
    while True:
        SCREEN.fill((210,205,200,255))
        
        draw_grid()
        draw_box()
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            get_key_press()
        pg.display.update()

def get_key_press():
    keys = pg.key.get_pressed()
    if keys[pg.K_UP]:
        vertical_update('u')
        generate_box()            
        printBoard()
    elif keys[pg.K_DOWN]:
        vertical_update('d')
        generate_box()            
        printBoard()
    elif keys[pg.K_RIGHT]:
        horizontal_update('r')
        generate_box()            
        printBoard()
    elif keys[pg.K_LEFT]:
        horizontal_update('l')
        generate_box()            
        printBoard()

def vertical_update(direction):
    if direction == 'u':
        for col in range(len(board)):
            limit = 0
            previousVal = 0
            for row in range(len(board[col])):
                if(isinstance(board[row][col], Square)):
                    temp = board[row][col]
                    
                    board[row][col] = None
                    board[limit][col] = temp
                    board[limit][col].change_position(col, limit)

                    if previousVal == board[limit][col].get_value():
                        temp2 = board[limit - 1][col] + board[limit][col]
                        board[limit - 1][col] = temp2
                        board[limit][col] = None
                        previousVal = 0
                        limit -= 1
                    else:
                        previousVal = board[limit][col].get_value()
                        print(f"[{limit}, {col}], Previous Val = {previousVal}")
                    
                    limit += 1
    elif direction == 'd':
        for col in range(len(board)):
            limit = 3
            previousVal = 0
            for row in range(len(board)-1, -1, -1):
                if(isinstance(board[row][col], Square)):
                    temp = board[row][col]

                    board[row][col] = None
                    board[limit][col] = temp
                    board[limit][col].change_position(col, limit)

                    if previousVal == board[limit][col].get_value():
                        temp2 = board[limit + 1][col] + board[limit][col]
                        board[limit + 1][col] = temp2
                        board[limit][col] = None
                        previousVal = 0
                        limit += 1
                    else:
                        previousVal = board[limit][col].get_value()

                    limit -= 1  

def horizontal_update(direction):
    if direction == 'l':
        for row in range(len(board[0])):
            limit = 0
            previousVal = 0
            for col in range(len(board)):
                if(isinstance(board[row][col], Square)):
                    temp = board[row][col]

                    board[row][col] = None
                    board[row][limit] = temp
                    board[row][limit].change_position(limit, row)

                    if previousVal == board[row][limit].get_value():
                        print('test')
                        print(f'Row: {row}, Col: {limit}')
                        temp2 = board[row][limit - 1] + board[row][limit]
                        board[row][limit-1] = temp2
                        board[row][limit] = None
                        previousVal = 0
                        limit -= 1
                    else:
                        previousVal = board[row][limit].get_value()
                        print(previousVal)
                    limit += 1

    elif direction == 'r':
        for row in range(len(board[0])):
            limit = 3
            previousVal = 0
            for col in range(len(board)-1, -1, -1):
                if(isinstance(board[row][col], Square)):
                    temp = board[row][col]
                    
                    board[row][col] = None
                    board[row][limit] = temp
                    board[row][limit].change_position(limit, row)

                    if previousVal == board[row][limit].get_value():
                        temp2 = board[row][limit + 1] + board[row][limit]
                        board[row][limit + 1] = temp2
                        board[row][limit] = None
                        previousVal = 0
                        limit += 1
                    else:
                        previousVal = board[row][limit].get_value()

                    limit -= 1
    # generate_box()            
    # printBoard()

def draw_grid():
    block_size = 120
    for x in range(0, WINDOW_WIDTH, block_size):
        for y in range(0, WINDOW_HEIGHT, block_size):
            rect = pg.Rect(x, y, block_size, block_size)
            pg.draw.rect(SCREEN, (188, 178, 156, 255), rect, 3)

def generate_box():
    count = 0
    for r in range(len(board[0])):
        for c in range(len(board)):
            if board[r][c] == None:
                break
            else:
                count += 1
    if count == 16:
        gameover()


    x_box = random.randint(0,3)
    y_box = random.randint(0,3)

    while(board[y_box][x_box] != None):
        x_box = random.randint(0,3)
        y_box = random.randint(0,3)
    
    board[y_box][x_box] = Square(x_box, y_box)
    for r in range(len(board[0])):
        for c in range(len(board)):
            if board[r][c] == 2048:
                youwin()

def draw_box():
    font = pg.font.Font('freesansbold.ttf', 25)
    for row in range(len(board[0])):
        for col in range(len(board)):
            if isinstance(board[row][col], Square):
                box_color, text_color = setColor(board[row][col].get_value())

                rect = pg.Rect(board[row][col].get_X_pos() * 120 + 3, board[row][col].get_Y_pos() * 120 + 3, 114, 114)
                pg.draw.rect(SCREEN, box_color, rect)

                text = font.render(f"{board[row][col]}", True, text_color, None)
                textRect = text.get_rect()
                textRect.center = (board[row][col].get_X_pos() * 120 + 3 + 58.5, board[row][col].get_Y_pos() * 120 + 3 + 58.5)
                
                SCREEN.blit(text, textRect)
                
def printBoard():
    for row in range(len(board[0])):
        print()
        for col in range(len(board)):
            if(board[row][col] == None):
                print(0, end = ' ')
            else:
                print(board[row][col], end = ' ')
    print()

def setColor(value):
    colors = {2: [(234,228,219, 255), (116,110,102, 255)],
              4: [(233,225,203,255), (116, 110, 102,255)],
              8: [(223, 180, 128,255), (248, 246, 242,255)],
              16: [(219, 154, 107,255), (248, 246, 242, 255)],
              32: [(215, 130, 101, 255), (248, 246, 242, 255)],
              64: [(211, 105, 70, 255), (248, 246, 242, 255)],
              128: [(226, 208, 124, 255), (248, 246, 242, 255)],
              256: [(225, 204, 110, 255), (248, 246, 242, 255)],
              512: [(225, 204, 110, 255), (248, 246, 242, 255)],
              1024: [(225, 204, 110, 255), (248, 246, 242, 255)],
              2048: [(225, 204, 110, 255), (248, 246, 242, 255)]}
    return colors[value][0], colors[value][1]

def gameover():
    s = pg.Surface((480,480))
    s.set_alpha(175)
    s.fill((255, 255, 255))
    SCREEN.blit(s, (0,0))
    
    font = pg.font.Font('freesansbold.ttf', 50)
    
    text = font.render("GAME OVER", True, 'black', None)
    textRect = text.get_rect()
    textRect.center = (240, 240)
    SCREEN.blit(text, textRect)
    pg.display.update()
    time.sleep(5)
    pg.quit()

def youwin():
    s = pg.Surface((480,480))
    s.set_alpha(175)
    s.fill((255, 255, 255))
    SCREEN.blit(s, (0,0))
    
    font = pg.font.Font('freesansbold.ttf', 50)
    
    text = font.render("YOU WIN!!", True, 'black', None)
    textRect = text.get_rect()
    textRect.center = (240, 240)
    SCREEN.blit(text, textRect)
    pg.display.update()
    time.sleep(60)
    pg.quit()

main()
