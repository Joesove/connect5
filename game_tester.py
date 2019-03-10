#!/usr/bin/env python3

# Created by : Joseph Harte
#       Date : March 2019
#    Version : 1.0

from server import Game
import pytest

def test_add_bad_column_range():
	game = Game()

	# Test out of out of bounds turn (0-8)
	assert game.add(9, 1) == False
	assert game.add(-1, 1) == False

def test_add_bad_player_number():
	game = Game()

	# Test vaild player number (can only be 1 or 2)
	assert game.add(0, 0) == False
	assert game.add(0, 3) == False

def test_add_to_full_column():
	game = Game()

	# Test adding to a full column
	game.add(0, 1)
	game.add(0, 2)
	game.add(0, 1)
	game.add(0, 2)
	game.add(0, 1)
	game.add(0, 2)
	assert game.add(0, 1) == False

def test_add_to_each_column():
	game = Game()

	# Test adding to each column
	assert game.add(0, 1) == True
	assert game.add(1, 1) == True
	assert game.add(2, 1) == True
	assert game.add(3, 1) == True
	assert game.add(4, 1) == True
	assert game.add(5, 1) == True
	assert game.add(6, 1) == True
	assert game.add(7, 1) == True
	assert game.add(8, 1) == True

def test_vertical_win():
	game = Game()

	moves = [0, 1, 0, 1, 0, 1, 0, 1]

	for move in moves:
		game.add(move, game.turn + 1)
		assert game.check_win(game.turn + 1) == False
		game.turn = not game.turn

	# winning move
	game.add(0, game.turn + 1)

	# Player one should win
	assert game.check_win(1) == True

def test_horizontal_win():
	game = Game()

	moves = [0, 0, 1, 1, 2, 2, 3, 3]

	for move in moves:
		game.add(move, game.turn + 1)
		assert game.check_win(game.turn + 1) == False
		game.turn = not game.turn

	# winning move
	game.add(4, game.turn + 1)

	# Player one should win
	assert game.check_win(1) == True

def test_diagonal_forward_win():
	game = Game()

	moves = [0, 1, 1, 2, 2, 3, 2, 3, 4, 3, 4, 4, 3, 4]

	for move in moves:
		game.add(move, game.turn + 1)
		assert game.check_win(game.turn + 1) == False
		game.turn = not game.turn

	# winning move
	game.add(4, game.turn + 1)

	""" final board
	[ ][ ][ ][ ][ ][ ][ ][ ][ ]
	[ ][ ][ ][ ][x][ ][ ][ ][ ]
	[ ][ ][ ][x][o][ ][ ][ ][ ]
	[ ][ ][x][o][x][ ][ ][ ][ ]
	[ ][x][x][o][o][ ][ ][ ][ ]
	[x][o][o][o][x][ ][ ][ ][ ]
	"""

	# Player one should win
	assert game.check_win(1) == True

def test_diagonal_back_win():
	game = Game()

	moves = [4, 4, 4, 4, 4, 5, 8, 7, 7, 6, 6 ,5, 6, 5]

	for move in moves:
		game.add(move, game.turn + 1)
		assert game.check_win(game.turn + 1) == False
		game.turn = not game.turn

	# winning move
	game.add(5, game.turn + 1)

	""" final board
	[ ][ ][ ][ ][ ][ ][ ][ ][ ]
	[ ][ ][ ][ ][x][ ][ ][ ][ ]
	[ ][ ][ ][ ][o][x][ ][ ][ ]
	[ ][ ][ ][ ][x][o][x][ ][ ]
	[ ][ ][ ][ ][o][o][x][x][ ]
	[ ][ ][ ][ ][x][o][o][o][x]
	"""

	# Player one should win
	assert game.check_win(1) == True

def test_draw():
	game = Game()

	moves = [0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 2, 3, 2, 3, 2, 3, 3, 2, 3, 2, 3, 2, 4, 5, 4, 5, 4, 5, 5, 4, 5, 4, 5, 4, 6, 7, 6, 7, 6, 7, 7, 6, 7, 6, 7, 6, 8, 8, 8, 8, 8, 8]

	for move in moves:
		game.add(move, game.turn + 1)
		assert game.check_win(game.turn + 1) == False
		game.turn = not game.turn

	# No more moves available
	assert game.add(0, game.turn + 1) == False

	# No player should win
	assert game.check_win(1) == False
	assert game.check_win(2) == False

	assert game.check_draw() == True

def test_p2_win():
	game = Game()

	moves = [0, 1, 0, 1, 0, 1, 0, 1, 2]

	for move in moves:
		game.add(move, game.turn + 1)
		assert game.check_win(game.turn + 1) == False
		game.turn = not game.turn

	# winning move
	game.add(1, game.turn + 1)

	# Player two should win
	assert game.check_win(2) == True