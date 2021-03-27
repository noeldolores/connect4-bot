#!/usr/bin/env python3

import numpy as np
import pygame
import sys
import math
import random

BOARD_SIZE = {'width':7, 'height':6}

ROW_COUNT = BOARD_SIZE['height']
COLUMN_COUNT = BOARD_SIZE['width']

BLUE = (0,0,139)
WHITE = (240, 250, 250)
RED = (255, 0, 0)
BLACK = (51, 47, 48)

PLAYER = 0
BOT = 1

EMPTY = 0
PLAYER_PIECE = 1
BOT_PIECE = 2

WINDOW_LENGTH = 4

def create_board():
  board = np.zeros((ROW_COUNT, COLUMN_COUNT))
  return board


def drop_piece(board, row, column, piece):
  board[row][column] = piece


def is_valid_location(board, column):
  return board[ROW_COUNT - 1][column] == 0
  
  
def get_next_open_row(board, column):
  for r in range(COLUMN_COUNT):
    if board[r][column] == 0:
      return r


def print_board(board):
  print(np.flip(board, 0))


def winning_move(board, piece):
  # Check horizontal locations
  for c in range(COLUMN_COUNT - 3):
    for r in range(ROW_COUNT):
      if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
        return True
  # Check vertical locations
  for c in range(COLUMN_COUNT):
    for r in range(ROW_COUNT - 3):
      if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
        return True

  # Check for positive slopes
  for c in range(COLUMN_COUNT - 3):
    for r in range(ROW_COUNT - 3):
      if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
        return True

  # Check for negative slopes
  for c in range(COLUMN_COUNT - 3):
    for r in range(3, ROW_COUNT):
      if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
        return True

def evaluate_window(window, piece):
  opp_piece = PLAYER_PIECE
  if piece == PLAYER_PIECE:
    opp_piece = BOT_PIECE

  score = 0
  if window.count(piece) == 4:
    score += 100
  elif window.count(piece) == 3 and window.count(EMPTY) == 1:
    score += 10
  elif window.count(piece) == 2 and window.count(EMPTY) == 2:
    score += 5

  if window.count(opp_piece) == 4:
    score -= 100
  elif window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
    score -= 10
  elif window.count(opp_piece) == 2 and window.count(EMPTY) == 2:
    score -= 5

  return score

def score_position(board, piece):
  score = 0

  # Center Column Score
  center_array = [i for i in list(board[:, COLUMN_COUNT//2])]
  center_count = center_array.count(piece)
  score += center_count * 6

  # Horizontal Score
  for r in range(ROW_COUNT):
    row_array = [i for i in list(board[r,:])]
    for c in range(COLUMN_COUNT - 3):
      window = row_array[c:c+WINDOW_LENGTH]
      score += evaluate_window(window, piece)

  # Vertical Score
  for c in range(COLUMN_COUNT):
    column_array = [i for i in list(board[:,c])]
    for r in range(ROW_COUNT - 3):
      window = column_array[r:r+WINDOW_LENGTH]
      score += evaluate_window(window, piece)

  # Positive Slopes
  for r in range(ROW_COUNT - 3):
    for c in range(COLUMN_COUNT - 3):
      window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
      score += evaluate_window(window, piece)

  # Negative Slopes
  for r in range(ROW_COUNT - 3):
    for c in range(COLUMN_COUNT - 3):
      window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
      score += evaluate_window(window, piece)

  return score

def get_valid_locations(board):
  valid_locations = []
  for col in range(COLUMN_COUNT):
    if is_valid_location(board, col):
      valid_locations.append(col)
  return valid_locations

def pick_best_move(board, piece):
  best_score = -100
  valid_locations = get_valid_locations(board)
  best_column = random.choice(valid_locations)
  for column in valid_locations:
    row = get_next_open_row(board, column)
    temp_board = board.copy()
    drop_piece(temp_board, row, column, piece)
    score = score_position(temp_board, piece)
    if score > best_score:
      best_score = score
      best_column = column
  return best_column, best_score
  




def draw_board(board):
  for c in range(COLUMN_COUNT):
    for r in range(ROW_COUNT):
      pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE) )
      pos = ((c*SQUARESIZE+SQUARESIZE/2), (r*SQUARESIZE + SQUARESIZE+SQUARESIZE/2))
      pygame.draw.circle(screen, WHITE, pos, RADIUS)
      
  for c in range(COLUMN_COUNT):
    for r in range(ROW_COUNT):
      pos = ((c*SQUARESIZE+SQUARESIZE/2), height - (r*SQUARESIZE +SQUARESIZE/2))
      if board[r][c] == PLAYER_PIECE:
        pygame.draw.circle(screen, RED, pos, RADIUS)
      elif board[r][c] == BOT_PIECE:
        pygame.draw.circle(screen, BLACK, pos, RADIUS)
  pygame.display.update()


def change_turn(turn):
  turn = (turn + 1) % 2
  change_piece_color(turn)

  return turn


def change_piece_color(turn):
  pygame.draw.rect(screen, WHITE, (0,0, width, SQUARESIZE))
  try:
    if turn == PLAYER:
      pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
  except:
    pass
  
  pygame.display.update()


board = create_board()
game_over = False
turn = random.randint(PLAYER, BOT)

pygame.init()

SQUARESIZE = 100
RADIUS = int(SQUARESIZE/(2 + 0.25))

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT + 1)* SQUARESIZE

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
      # Get Player Input
      if turn == PLAYER:
        posx = event.pos[0]
        column = int(math.floor(posx / SQUARESIZE))

        if is_valid_location(board, column):       
          row = get_next_open_row(board, column)
          drop_piece(board, row, column, PLAYER_PIECE)
          print_board(board)
          draw_board(board)

          if winning_move(board, PLAYER_PIECE):
            game_over = True
          else:
            turn = change_turn(turn)
        else:
          print("Column is full, choose agin")

  # Get Bot Input
  if turn == BOT and not game_over:
    #column = random.randint(0, COLUMN_COUNT - 1)
    bot_choice = pick_best_move(board, BOT_PIECE)
    column = bot_choice[0]
    column_score = bot_choice[1]
    print(column_score)

    if is_valid_location(board, column):   
      pygame.time.wait(750)    

      row = get_next_open_row(board, column)
      drop_piece(board, row, column, BOT_PIECE)
      print_board(board)
      draw_board(board)

      if winning_move(board, BOT_PIECE):
        game_over = True
      else:
        turn = change_turn(turn)
    else:
      print("Column is full, choose agin")

  if game_over:
    pygame.draw.rect(screen, WHITE, (0,0, width, SQUARESIZE))
    if turn == PLAYER:
      label = myfont.render("Player WINS!", 1, RED)
    else:
      label = myfont.render("BOT WINS!", 1, BLACK)

    screen.blit(label, (40,10))
    pygame.display.update()

    pygame.time.wait(3000)