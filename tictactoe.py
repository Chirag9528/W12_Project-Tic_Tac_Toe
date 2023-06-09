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
        
#getting diagonal 1 
def dia1():
  
  dia = []
  i =0
  for row in boxes:
    dia.append(row[i])
    i += 1
  return dia
  
#getting diagonal 2
def dia2():
  
  dia = []
  i =4
  for row in boxes:
    dia.append(row[i])
    i -= 1
  return dia

#getting all the rows/colums/diagonals in a list
def get_all():
  
  get = []
  for row in boxes:
    get.append(row)     #getting rows

  for i in range(5):
    column =[row[i] for row in boxes]
    get.append(column)   #getting columns

  get.append(dia2())     #getting diagonal 2
  get.append(dia1())     #getting diagonal 1

  return get

#checking the win or lose
def check():
  get =get_all()
  x_ct =0
  o_ct =0

  #counting the number of elements get list
  
  for RC in get:
    for box in RC:
      
      if box['value']=='X':
        x_ct +=1
      elif box['value']=='O':
        o_ct +=1

    if x_ct==5: #if x wins
      line(RC)
      end('X')  

    elif o_ct==5: #if o wins
      line(RC)
      end('O')
    
    x_ct =0
    o_ct =0  

#to fill the box with the value for the computer

def fill(sent):
  
  temp =[]
  global level
  ran =random.random()

  if sent==[] or (level==1 and ran<0.5):    #randomizing the fill if level 1 is chosen
    for row in boxes:
      for box in row:
        if box['value']=='':
          temp.append(box)
  else:
    if type(sent[0])==list:     #checking if there are multiple boxes in the list
      for RC in sent:
        for box in RC:
          if box['value']=='':
            temp.append(box)
    else:
        for box in sent:           #else filling the single box to be filled
            if box['value']=='':
                temp.append(box)
  if temp==[]:
     for row in boxes:
        for box in row:
           if box['value']=='':
              temp.append(box)
  box =random.choice(temp)   #randomly filling the boxes of equal outcomes
  box['value'] ='X'
  return
    
#finding the common boxes of favourable rows/columns/diagonals

def common(send):
  
  box_occurrences = {}
  new_send =[]
  maximum =0

  #finding the common box with maximum overlapping

  for RC in send:
    for box in RC:
      
      box_key = (box['rect'].x, box['rect'].y)
      if box['value']=='':
        if box_key in box_occurrences:
          box_occurrences[box_key] += 1
          if box_occurrences[box_key]>maximum:
            maximum =box_occurrences[box_key]
            new_send =[]
          new_send.append(box)
        else:
          box_occurrences[box_key] = 1
          
  if new_send==[]:  #if there are no overlaaping sending the bare list
    fill(send)
  else:
    fill(new_send)  #else sending the new list with common boxes
    
#algorithm for the computer mode

def com():
  
  x_ct =0
  o_ct =0
  space =0
  maximum =0
  get =get_all()
  send = []
  
  for RC in get:
    for box in RC:
      #checking the count of x and o count
      if box['value']=='X':                         
        x_ct +=1
      elif box['value']=='O':
        o_ct +=1
      else:
        space +=1
        
    #blocking the win of the player
    if o_ct==4 and space==1:
      if maximum!=4: 
        send = []
        send.append(RC)
        maximum =4
    
    if x_ct>maximum and space+x_ct==5:
      send = []
      maximum =x_ct
    
    #checking the empty rows/colums/diagonals
    if x_ct==maximum and space+x_ct==5:
      if x_ct==4: #checking the win
        send =[]
        send.append(RC)
      send.append(RC)
      
    x_ct =0
    o_ct =0
    space =0
    
  common(send)

#resetting the values of all the boxes
def reset():
  for row in boxes:
    for box in row:
      box['value']=''
running =True


def mode():
  
  global running
  #initializing node window
  mode=pygame.image.load('nmode_bg.jpg')
  mode=pygame.transform.scale(mode,(560,560))
  screen.blit(mode,(0,0))


  #setting the position of coordinates of modes button
  rectangle1_x = 25
  rectangle1_y = 300
  rectangle2_x = 370
  rectangle2_y = 300

  #defining dimensions of the level buttons
  rectangle_width1 = 190
  rectangle_width2=170
  rectangle_height = 200

  pygame.display.flip()
  while running:
    for event in pygame.event.get():
      if event.type==pygame.QUIT:
        #if player clicked the closed button
        running =False
      elif event.type == pygame.MOUSEBUTTONUP:
        global computer
        mouse_x, mouse_y = pygame.mouse.get_pos()


        if (rectangle1_x <= mouse_x and mouse_x <= rectangle1_x + rectangle_width1) and (rectangle1_y <= mouse_y and mouse_y <= rectangle1_y + rectangle_height):
          #if player clicked 'Multiplayer'
          computer =False
          gameloop()
          


        if (rectangle2_x <= mouse_x and mouse_x<= rectangle2_x + rectangle_width2) and (rectangle2_y<=mouse_y and mouse_y<=(rectangle2_y+rectangle_height)):
          #if player clicked 'V/S Computer'
          computer =True
          level_set()

    pygame.display.update()
      
def level_set():
  global running
  #initializing level window
  lable=pygame.image.load('nlevel_bg.jpg')
  lable=pygame.transform.scale(lable,(560,560))
  screen.blit(lable,(0,0))


  #setting the position of coordinates of levels button
  rectangle1_x = 60               
  rectangle1_y = 300               
  rectangle2_x = 350             
  rectangle2_y = 290 

  #defining dimensions of the level buttons
  rectangle_width1 = 165
  rectangle_width2=175
  rectangle_height = 175



  while running:
    for event in pygame.event.get():

      if event.type==pygame.QUIT:
        running =False
      elif event.type == pygame.MOUSEBUTTONUP:
        global level
        mouse_x, mouse_y = pygame.mouse.get_pos()


        if (rectangle1_x <= mouse_x and mouse_x <= rectangle1_x + rectangle_width1) and (rectangle1_y <= mouse_y and mouse_y<= rectangle1_y + rectangle_height):
          #if player clicked level1
          level =1
          gameloop()


        if (rectangle2_x <= mouse_x and mouse_x<= rectangle2_x + rectangle_width2) and (rectangle2_y <= mouse_y and mouse_y<= rectangle2_y + rectangle_height):
          #if player clicked level2
          level =2
          gameloop()
    pygame.display.update()
      
def welcome():
    #loading music and playing it
    pygame.mixer.music.load('welcome_music.wav')
    pygame.mixer.music.play()
    

    global running
    while running:
        

        #loading the background image
        background = pygame.image.load("nwelcome_new.jpg")
        background = pygame.transform.scale(background, (560,560))
        screen.blit(background, (0,0))

        #defining coordinates of start button
        rectangle_x = 190
        rectangle_y = 315
        rectangle_width = 183
        rectangle_height = 185

        

        for event in pygame.event.get():
                
                if event.type==pygame.QUIT:
                    running =False

                elif event.type == pygame.MOUSEBUTTONUP:
                  mouse_x, mouse_y = pygame.mouse.get_pos()
                  if (rectangle_x <= mouse_x and mouse_x <= rectangle_x + rectangle_width) and (rectangle_y <= mouse_y and mouse_y <= rectangle_y + rectangle_height):
                    #if player clicked start button
                    mode()
        pygame.display.update()
        
def end(s):
  pygame.mixer.music.load('win_music.wav')
  pygame.mixer.music.play()


  global running
  global count
  count =0
  while running:

    if s=='O':
      screen.fill((100,200,0))

      if computer:
        #if player won the game V/S computer
        background1 = pygame.image.load("O_win.jpg")
        background1 = pygame.transform.scale(background1, (560,560))
        screen.blit(background1, (0,0))

        #adding text to screen
        text = textfont.render("Press enter to continue...", True, BLUE)
        screen.blit(text, (180,520))


      else:
        #if player1 won the game
        background2 = pygame.image.load("O_win.jpg")
        background2 = pygame.transform.scale(background2, (560,560))
        screen.blit(background2, (0,0))

        #adding text to screen
        text = textfont.render("Press enter to continue...", True, BLUE)
        screen.blit(text, (180,520))


    elif s=='X':
      screen.fill((0,255,0))

      if computer:
        #if player lose the game V/S computer

        background3 = pygame.image.load("X_win.jpg")
        background3 = pygame.transform.scale(background3, (560,560))
        screen.blit(background3, (0,0))

        #adding text to screen
        text = textfont.render("Press enter to continue...", True, BLUE)
        screen.blit(text, (180,520))

      else:
        #if player2 won the game

        background4 = pygame.image.load("X_win.jpg")
        background4 = pygame.transform.scale(background4, (560,560))
        screen.blit(background4, (0,0))

        #adding text to screen
        text = textfont.render("Press enter to continue...", True, BLUE)
        screen.blit(text, (180,520))


    else:
      #if the game is draw

      screen.fill((200,200,200))
      background5 = pygame.image.load("Draw.jpg")
      background5 = pygame.transform.scale(background5, (560,560))
      screen.blit(background5, (0,0))

      #adding text to screen
      text = textfont.render("Press enter to continue...", True, BLUE)
      screen.blit(text, (180,520))
      
    for event in pygame.event.get():
      if event.type==pygame.QUIT:
        running =False
      if event.type==pygame.KEYDOWN:
        if event.key==pygame.K_RETURN:
          welcome()
    pygame.display.update()
    
def gameloop():
  #stoping the music after entering into gameloop
  pygame.mixer.music.stop()

  reset()          #resetting the matrix
  global running
  while running:
      
      global count
      for event in pygame.event.get():
        
          if event.type == pygame.QUIT:        
              running =False
          elif event.type ==pygame.KEYDOWN:
            if event.key ==pygame.K_SPACE:
                reset()
          elif event.type == pygame.MOUSEMOTION:        #adding the hovering effect
              for row in boxes:
                  for box in row:
                      
                      if box['rect'].collidepoint(event.pos):  #if hovered ,box margin color is changed
                          box['color'] = BLACK
                      else:
                          box['color'] = GRAY
              
              update_screen()

          elif event.type == pygame.MOUSEBUTTONUP:
              for row in boxes:
                  for box in row:
                      
                      if box['rect'].collidepoint(event.pos):     #if clicked in a box
                          
                          if count==0:
                            reset()

                          if box['value'] == '':   #if only box is empty ,fill the box
                              
                              if count%2==0:
                                box['value'] = 'O'
                              else:
                                box['value'] ='X'
                              update_screen()
                              check()
                              
                              count +=1                              
                              if count==25:
                                end('D')
                                break

                              if computer:
                                com()
                                update_screen()
                                check()
                              else:
                                break
                              count+=1



welcome()
pygame.quit()
