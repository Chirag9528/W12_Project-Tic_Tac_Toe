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
def dia1():
  dia = []
  i =0
  for row in boxes:
    dia.append(row[i])
    i += 1
  return dia  
def dia2():
  dia = []
  i =2
  for row in boxes:
    dia.append(row[i])
    i -= 1
  return dia
def get_all():
  get = []
  for row in boxes:
    get.append(row)
  for i in range(3):
    column =[row[i] for row in boxes]
    get.append(column)
  get.append(dia2())
  get.append(dia1())
  return get
def check():
  get =get_all()
  x_ct =0
  o_ct =0
  for RC in get:
    for box in RC:
      if box['value']=='X':
        x_ct +=1
      elif box['value']=='O':
        o_ct +=1
    if x_ct==3:
      print('X wins')
      return True
    elif o_ct==3:
      print('O wins')
      return True
    x_ct =0
    o_ct =0  
def Clearboard(board):
    for x, rows in enumerate(board):
        for y, col in enumerate(rows):
            board[x][y] = 0 
def Win(board, play):
    comb = [[board[0][0], board[0][1], board[0][2]],
                     [board[1][0], board[1][1], board[1][2]],
                     [board[2][0], board[2][1], board[2][2]],
                     [board[0][0], board[1][0], board[2][0]],
                     [board[0][1], board[1][1], board[2][1]],
                     [board[0][2], board[1][2], board[2][2]],
                     [board[0][0], board[1][1], board[2][2]],
                     [board[0][2], board[1][1], board[2][0]]]

    if [play,play,play] in comb:
        return True

    return False #asdf
def Won(board):
    return Win(board, 1) or Win(board, -1)
def empty(board):
    blanks = []
    for x, rows in enumerate(board):
        for y, col in enumerate(rows):
            if board[x][y] == 0:
                blanks.append([x, y])
    return blanks
    
def boardFull(board):
    if len(empty(board)) == 0:
        return True
    return False
def Score(board):
    if Win(board, 1):
        return 10
    elif Win(board, -1):
        return -10
    else:
        return 0
        
def Move(board, x, y, player):
    board[x][y] = player
def Moved(board, x, y, player):
    board[x][y] = player
    box =boxes[x][y]
    box['value'] ='O'
def match():
  for i in range(3):
    for j in range(3):
      box =boxes[i][j]
      if box['value']=='X':
        board[i][j] =1
      elif box['value']=='O':
        board[i][j] =-1
      else:
        board[i][j] =0
def abminimax(board, depth, alpha, beta, player):
    row = -1
    col = -1
    if depth == 0 or Won(board):
        return [row, col, Score(board)]
    else:
        for box in empty(board):
            Move(board, box[0], box[1], player)
            score = abminimax(board, depth - 1, alpha, beta, -player)
            if player == 1:
                if score[2] > alpha:
                    alpha = score[2]
                    row = box[0]
                    col = box[1]
            else:
                if score[2] < beta:
                    beta = score[2]
                    row = box[0]
                    col = box[1]
            Move(board, box[0],box[1], 0)
            if alpha >= beta:
                break
        if player == 1:
            return [row, col, alpha]
        else:
            return [row, col, beta]
def com(board):
    if len(empty(board)) == 9:
        x = choice([0, 1, 2])
        y = choice([0, 1, 2])
        Moved(board, x, y, -1)
        update_screen()
    else:
        moves = abminimax(board, len(empty(board)), -inf, inf, -1)
        Moved(board, moves[0], moves[1], -1)
        update_screen()

    
