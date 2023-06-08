import pygame
import random

#initializing pygame

pygame.init()     


pygame.mixer.init()

#defining colors

WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
BROWN = (150,75,0)
MAROON =(175,50,0)

#creating interface

screen = pygame.display.set_mode((560, 560))
background_color = MAROON
screen.fill(background_color)
font = pygame.font.SysFont(None, 100)
textfont = pygame.font.SysFont(None,25)
clock=pygame.time.Clock()

#declaring global variables
level =0
computer =None
count =0

#defining the box objects

box_size = 100
box_padding = 10
box_color = GRAY
boxes = []

for row in range(5):

    row_boxes = []    #declaring rows
    for col in range(5):

        box_x = col * (box_size + box_padding) + box_padding     #getting the x-coordinate
        box_y = row * (box_size + box_padding) + box_padding     #getting the y-coordinate
        box_rect = pygame.Rect(box_x, box_y, box_size, box_size)    #drawing the rectangle
        row_boxes.append({'rect': box_rect, 'color': box_color, 'value': ''})   #appending the initialized box objects in the row  

    boxes.append(row_boxes)    #appending the rows in the boxes

#updating the screen

def update_screen():

    screen.fill(background_color)

    #drawing the screen
    for i in range(5):
      for j in range(5):
        x = box_padding + j * (box_size + box_padding)
        y = box_padding + i * (box_size + box_padding)
        pygame.draw.rect(screen, WHITE, pygame.Rect(x, y, box_size,box_size))
        
    for row in boxes:
        for box in row:

            pygame.draw.rect(screen, box['color'], box['rect'], 5)
            #filling the boxes on the value they are stored
            if box['value'] == 'O':                                      
                text = font.render("O", True, BLUE)
                text_rect = text.get_rect(center=box['rect'].center)
                screen.blit(text, text_rect)
            elif box['value'] == 'X':
                text = font.render("X", True, BLUE)
                text_rect = text.get_rect(center=box['rect'].center)
                screen.blit(text, text_rect)

            #if hovered ,mark is shown
            elif box['color'] == BLACK:
                global count
                if count%2==0:
                  text = font.render("O", True, GRAY)
                  text_rect = text.get_rect(center=box['rect'].center)
                  screen.blit(text, text_rect)
                else:
                  text = font.render("X", True, GRAY)
                  text_rect = text.get_rect(center=box['rect'].center)
                  screen.blit(text, text_rect)

    pygame.display.flip()


def line(RC):   #drawing a line across the filled row/column/diagonal
      
      box1 =RC[0]
      box2 =RC[4]
      x1 ,y1 =box1['rect'].x,box1['rect'].y
      x2 ,y2 =box2['rect'].x,box2['rect'].y
      x1+=50 ;y1+=50 ;x2+=50 ;y2+=50

      pygame.draw.line(screen,BLACK,(x1,y1),(x2,y2),10)
      pygame.display.update()
      pygame.time.delay(2000)      #delay to show the result
