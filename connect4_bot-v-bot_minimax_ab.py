#!/usr/bin/env python3

import numpy as np
import pygame
import sys
import math
import random


ROW_COUNT = 6
COLUMN_COUNT = 7

BLUE = (0,0,139)
WHITE = (240, 250, 250)
RED = (255, 0, 0)
BLACK = (51, 47, 48)

RED_BOT = 0
BLACK_BOT = 1

EMPTY = 0
RED_BOT_PIECE = 1
BLACK_BOT_PIECE = 2

WINDOW_LENGTH = 4

GAME_DEPTH = 5
TURN_DELAY = 500


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
  opp_piece = RED_BOT_PIECE
  if piece == RED_BOT_PIECE:
    opp_piece = BLACK_BOT_PIECE

  score = 0

  if window.count(piece) == 4:
    score += 50 
  elif window.count(piece) == 3 and window.count(EMPTY) == 1:
    score += 25
  elif window.count(piece) == 2 and window.count(EMPTY) == 2:
    score += 10

  if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
    score -= 1000
  elif window.count(opp_piece) == 2 and window.count(EMPTY) == 2:
    score -= 50

  return score

def score_position(board, piece):
  score = 0

  # Center Column Score
  center_array = [i for i in list(board[:, COLUMN_COUNT//2])]
  center_count = center_array.count(piece)
  score += center_count * 10
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


def is_terminal_node(board):
  return winning_move(board, RED_BOT_PIECE) or winning_move(board, BLACK_BOT_PIECE) or len(get_valid_locations(board)) == 0


def minimax(board, depth, alpha, beta, maximizingPlayer):
  column_score_list = []
  valid_locations = get_valid_locations(board)
  is_terminal = is_terminal_node(board)

  if depth == 0 or is_terminal:
    if is_terminal:
      if winning_move(board, BLACK_BOT_PIECE):
        return (None, 10000, None)
      elif winning_move(board, RED_BOT_PIECE):
        return (None, -10000, None)
      else: # Game is over
        return (None, 0, None)
    else: #Depth is zero
      return (None, score_position(board, BLACK_BOT_PIECE), None)
  
  if maximizingPlayer:
    value = -math.inf
    [column_score_list.append(value) for i in range(COLUMN_COUNT)]
    best_column = random.choice(valid_locations)

    for column in valid_locations:
      row = get_next_open_row(board, column)
      temp_board = board.copy()
      drop_piece(temp_board, row, column, BLACK_BOT_PIECE)
      new_score = minimax(temp_board, depth -1, alpha, beta, False)[1]
      
      if new_score > value:
        value = new_score
        best_column = column
        column_score_list[column] = format(value, '.2f')
      alpha = max(alpha, value)
      if alpha >= beta:
        break

    return best_column, value, column_score_list

  else:
    value = math.inf
    [column_score_list.append(value) for i in range(COLUMN_COUNT)]
    best_column = random.choice(valid_locations)

    for column in valid_locations:
      row = get_next_open_row(board, column)
      temp_board = board.copy()
      drop_piece(temp_board, row, column, RED_BOT_PIECE)
      new_score = minimax(temp_board, depth -1, alpha, beta, True)[1]

      if new_score < value:
        value = new_score
        best_column = column
        column_score_list[column] = format(value, '.2f')
      beta = min(beta, value)
      if alpha >= beta:
        break

    return best_column, value, column_score_list


def get_valid_locations(board):
  valid_locations = []
  for col in range(COLUMN_COUNT):
    if is_valid_location(board, col):
      valid_locations.append(col)
  return valid_locations


def draw_board(board):
  for c in range(COLUMN_COUNT):
    for r in range(ROW_COUNT):
      pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE) )
      pos = ((c*SQUARESIZE+SQUARESIZE/2), (r*SQUARESIZE + SQUARESIZE+SQUARESIZE/2))
      pygame.draw.circle(screen, WHITE, pos, RADIUS)
      
  for c in range(COLUMN_COUNT):
    for r in range(ROW_COUNT):
      pos = ((c*SQUARESIZE+SQUARESIZE/2), height - (r*SQUARESIZE +SQUARESIZE/2))
      if board[r][c] == RED_BOT_PIECE:
        pygame.draw.circle(screen, RED, pos, RADIUS)
      elif board[r][c] == BLACK_BOT_PIECE:
        pygame.draw.circle(screen, BLACK, pos, RADIUS)
  pygame.display.update()


board = create_board()
game_over = False
turn = random.randint(RED_BOT, BLACK_BOT)

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
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_ESCAPE:
        pygame.quit()

  if turn == RED_BOT and not game_over:
    column, column_score, column_score_list = minimax(board, GAME_DEPTH, -math.inf, math.inf, True)

    if is_valid_location(board, column):   
      pygame.time.wait(TURN_DELAY) 

      row = get_next_open_row(board, column)
      drop_piece(board, row, column, RED_BOT_PIECE)
      
      draw_board(board)

      print_board(board)
      print(column_score_list)

      if winning_move(board, RED_BOT_PIECE):
        game_over = True
      else:
        turn = (turn + 1) % 2

  if turn == BLACK_BOT and not game_over:
    column, column_score, column_score_list = minimax(board, GAME_DEPTH, -math.inf, math.inf, True)
    

    if is_valid_location(board, column):  
      pygame.time.wait(TURN_DELAY) 
       
      row = get_next_open_row(board, column)
      drop_piece(board, row, column, BLACK_BOT_PIECE)

      draw_board(board)
      
      print_board(board)
      print(column_score_list)

      if winning_move(board, BLACK_BOT_PIECE):
        game_over = True
      else:
        turn = (turn + 1) % 2

  if game_over:
    pygame.draw.rect(screen, WHITE, (0,0, width, SQUARESIZE))
    if turn == RED_BOT:
      label = myfont.render("RED WINS!", 1, RED)
    else:
      label = myfont.render("BLACK WINS!", 1, BLACK)
    screen.blit(label, (40,10))

    pygame.display.update()

while game_over:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      sys.exit() 
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_ESCAPE:
        pygame.quit()
  draw_board(board)