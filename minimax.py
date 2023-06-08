import pygame
import random
from math import inf

pygame.init()

screen = pygame.display.set_mode((340,340))
background_color = (175,50, 0)
screen.fill(background_color)

textfont=pygame.font.SysFont(None,25)
font = pygame.font.SysFont(None, 100)
clock=pygame.time.Clock()

WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
BROWN = (150,75,0)
RED =(255,0,0)

box_size = 100
box_padding = 10
box_color = GRAY
count =0
boxes = []
board = [[0, 0, 0],
         [0, 0, 0],
         [0, 0, 0]]
for row in range(3):
    row_boxes = []
    for col in range(3):
        box_x = col * (box_size + box_padding) + box_padding
        box_y = row * (box_size + box_padding) + box_padding
        box_rect = pygame.Rect(box_x, box_y, box_size, box_size)
        row_boxes.append({'rect': box_rect, 'color': box_color, 'value': ''})
    boxes.append(row_boxes)
def update_screen():
    screen.fill(background_color)
    for i in range(3):
      for j in range(3):
        x = box_padding + j * (box_size + box_padding)
        y = box_padding + i * (box_size + box_padding)
        pygame.draw.rect(screen, WHITE, pygame.Rect(x, y, box_size,box_size))
    for row in boxes:
        for box in row:
            pygame.draw.rect(screen, box['color'], box['rect'], 4)
            if box['value'] == 'O':
                text = font.render("O", True, BLUE)
                text_rect = text.get_rect(center=box['rect'].center)
                screen.blit(text, text_rect)
            elif box['value'] == 'X':
                text = font.render("X", True, BLUE)
                text_rect = text.get_rect(center=box['rect'].center)
                screen.blit(text, text_rect)
            elif box['color'] == BLACK:
                text = font.render("X", True, GRAY)
                text_rect = text.get_rect(center=box['rect'].center)
                screen.blit(text, text_rect)
    pygame.display.flip()
    
