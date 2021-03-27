import numpy as np
import pygame
import sys
import math

BOARD_SIZE = {'width':7, 'height':6}
BLUE = (0,0,139)
WHITE = (240, 250, 250)
RED = (255, 0, 0)
BLACK = (51, 47, 48)

def create_board():
  board = np.zeros((BOARD_SIZE['height'], BOARD_SIZE['width']))
  return board


def drop_piece(board, row, column, piece):
  board[row][column] = piece


def is_valid_location(board, column):
  return board[BOARD_SIZE['height'] - 1][column] == 0
  
  
def get_next_open_row(board, column):
  for r in range(BOARD_SIZE['width']):
    if board[r][column] == 0:
      return r


def print_board(board):
  print(np.flip(board, 0))


def winning_move(board, piece):
  # Check horizontal locations
  for c in range(BOARD_SIZE['width'] - 3):
    for r in range(BOARD_SIZE['height']):
      if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
        return True
  # Check vertical locations
  for c in range(BOARD_SIZE['width']):
    for r in range(BOARD_SIZE['height'] - 3):
      if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
        return True

  # Check for positive slopes
  for c in range(BOARD_SIZE['width'] - 3):
    for r in range(BOARD_SIZE['height'] - 3):
      if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
        return True

  # Check for negative slopes
  for c in range(BOARD_SIZE['width'] - 3):
    for r in range(3, BOARD_SIZE['height']):
      if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
        return True


def draw_board(board):
  for c in range(BOARD_SIZE['width']):
    for r in range(BOARD_SIZE['height']):
      pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE) )
      pos = ((c*SQUARESIZE+SQUARESIZE/2), (r*SQUARESIZE + SQUARESIZE+SQUARESIZE/2))
      pygame.draw.circle(screen, WHITE, pos, RADIUS)
      
  for c in range(BOARD_SIZE['width']):
    for r in range(BOARD_SIZE['height']):
      pos = ((c*SQUARESIZE+SQUARESIZE/2), height - (r*SQUARESIZE +SQUARESIZE/2))
      if board[r][c] == 1:
        pygame.draw.circle(screen, BLACK, pos, RADIUS)
      elif board[r][c] == 2:
        pygame.draw.circle(screen, RED, pos, RADIUS)
  pygame.display.update()


def change_turn(turn):
  turn = (turn + 1) % 2
  change_piece_color(turn)

  return turn


def change_piece_color(turn):
  pygame.draw.rect(screen, WHITE, (0,0, width, SQUARESIZE))
  if turn == 0:
    pygame.draw.circle(screen, BLACK, (posx, int(SQUARESIZE/2)), RADIUS)
  else:
    pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
  
  pygame.display.update()


board = create_board()
game_over = False
turn = 0

pygame.init()

print(pygame.font.get_fonts())

SQUARESIZE = 100
RADIUS = int(SQUARESIZE/(2 + 0.25))

width = BOARD_SIZE['width'] * SQUARESIZE
height = (BOARD_SIZE['height'] + 1)* SQUARESIZE

size = (width, height)

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.draw.rect(screen, WHITE, (0,0, width, SQUARESIZE))
pygame.display.update()

myfont = pygame.font.SysFont("cambria", 90)

while not game_over:

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      sys.exit() 
    
    if event.type == pygame.MOUSEMOTION:
      posx = event.pos[0]
      change_piece_color(turn)

    if event.type == pygame.MOUSEBUTTONDOWN:
      # Get Player 1 Input
      if turn == 0:
        posx = event.pos[0]
        column = int(math.floor(posx / SQUARESIZE))

        if is_valid_location(board, column):       
          row = get_next_open_row(board, column)
          drop_piece(board, row, column, 1)
          print_board(board)
          draw_board(board)

          if winning_move(board, 1):
            game_over = True
          else:
            turn = change_turn(turn)
        else:
          print("Column is full, choose agin")

      # Get Player 2 Input
      else:
        posx = event.pos[0]
        column = int(math.floor(posx / SQUARESIZE))

        if is_valid_location(board, column):       
          row = get_next_open_row(board, column)
          drop_piece(board, row, column, 2)
          print_board(board)
          draw_board(board)

          if winning_move(board, 2):
            game_over = True
          else:
            turn = change_turn(turn)
        else:
          print("Column is full, choose agin")

  if game_over:
    pygame.draw.rect(screen, WHITE, (0,0, width, SQUARESIZE))
    if turn == 0:
      font_color = BLACK
    else:
      font_color = RED
    label = myfont.render("Player {} WINS!".format(turn + 1), 1, font_color)
    screen.blit(label, (40,10))
    pygame.display.update()

    pygame.time.wait(3000)