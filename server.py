#!/usr/bin/env python3

# Created by : Joseph Harte
#       Date : March 2019
#    Version : 1.0

from socket import AF_INET, socket, SOCK_STREAM, gethostname
import json
import logging
import sys

class Game:
	# Size of the game board
	cols = 9
	rows = 6

	def __init__(self):
		# False for player one, True for player two
		self.turn = False

		# Turn counter
		self.counter = 0

		# Matrix that holds the state of the board
		self.board = []

		# Creates empty board
		for x in range(self.rows):
			self.board.append([0] * self.cols)

	def __str__(self):
		result = ""
		for r in range(self.rows):
			for c in range(self.cols):
				result += "["
				if self.board[r][c] == 1:
					result += "x"
				elif self.board[r][c] == 2:
					result += "o"
				else:
					result += " "
				result += "]"
			result += "\n"
		return result

	def add(self, column, player_num):
		# Check if its a valid move
		if column < 0 or column >= self.cols:
			return False

		if player_num not in [1, 2]:
			return False

		# Get the lowest empty cell
		for row in range(self.rows - 1, -1, -1):
			if self.board[row][column] is 0:
				self.board[row][column] = player_num
				logging.info("Successful turn by player %s" % player_num)
				self.counter += 1
				return True

		# Column is full and disc can't fit
		return False

	def check_win(self, player_num):
		# There cannot be a winner until at least turn 9
		if self.counter < 9:
			return False

		b = self.board
		# Check vertical win
		for r in range(self.rows - 4):
			for c in range(self.cols):
				if b[r][c] == player_num and b[r+1][c] == player_num and b[r+2][c] == player_num and b[r+3][c] == player_num and b[r+4][c] == player_num:
					return True
		# Check horizontal win
		for r in range(self.rows):
			for c in range(self.cols - 4):
				if b[r][c] == player_num and b[r][c+1] == player_num and b[r][c+2] == player_num and b[r][c+3] == player_num and b[r][c+4] == player_num:
					return True
		# Check / diagonal win
		for r in range(4, self.rows):
			for c in range(self.cols - 4):
				if b[r][c] == player_num and b[r-1][c+1] == player_num and b[r-2][c+2] == player_num and b[r-3][c+3] == player_num and b[r-4][c+4] == player_num:
					return True
		# Check  \ diagonal win
		for r in range(self.rows - 4):
			for c in range(self.cols - 4):
				if b[r][c] == player_num and b[r+1][c+1] == player_num and b[r+2][c+2] == player_num and b[r+3][c+3] == player_num and b[r+4][c+4] == player_num:
					return True
		return False

	def check_draw(self):
		return self.counter >= (self.rows * self.cols)
			

class Player:
	def __init__(self, client, client_addr, name, player_num):
		self.client = client
		self.client_addr = client_addr
		self.name = name
		self.player_num = player_num

def send_recv(client, msg):
	response = ""
	try:
		client.send(bytes(json.dumps(msg), "utf8"))
	except:
		logging.error("Cannot send msg to client")
		sys.exit(1)
	try:
		response = json.loads( client.recv(buf_size).decode("utf8") )
	except:
		logging.error("No response from client")
		sys.exit(1)
	return response


def main():
	logging.basicConfig(level=logging.INFO)
	
	players = {}
	game = Game()

	host = gethostname()
	port = 8000

	server = socket(AF_INET, SOCK_STREAM)
	server.bind((host, port))

	server.listen(2)
	logging.info("Starting server, waiting for connection")

	# Loop waiting for both clients to connect
	while len(players) < 2:
		# wait for a client 
		client, client_addr = server.accept()
		logging.info("%s:%s has connected." % client_addr)
		client.settimeout(timeout)

		# Send msg
		msg = {"cmd":"INFO", "data": ""}
		response = send_recv(client, msg)

		logging.info("%s joined." % response["data"])

		# Add player to the players
		p = Player(client, client_addr, response["data"], len(players) + 1)
		players[p.player_num] = p
	
		logging.debug("Player added.")

		# Notify players if they need to wait for a second player or they can begin
		if len(players) == 1:
			msg = {"cmd":"PRINT", "data": "Waiting for second player."}
			response = send_recv(p.client, msg)
		# Or that the game can start
		else:
			msg = {"cmd":"PRINT", "data": "Starting game."}
			for pnum, plyr in players.items():
				response = send_recv(plyr.client, msg)

	# Start game loop
	while True:
		logging.debug("Game started")

		# Get the player for this turn
		player = players[game.turn + 1]
		idle_player = players[(not game.turn) + 1]

		# Show the player the board and ask for their move
		msg = {"cmd": "PRINT", "data": str(game)}
		response = send_recv(player.client, msg)

		msg = {"cmd": "TURN", "data": player.name}
		response = send_recv(player.client, msg)

		# Enter the players move in the board
		result = game.add(response["data"], player.player_num)

		# Check for valid turn and win condition
		if (result):
			if game.check_win(player.player_num):
				logging.info("Game won by %s." % player.name)

				msg = {"cmd": "PRINT", "data": "Final board: \n" + str(game)}
				response = send_recv(player.client, msg)

				msg = {"cmd": "PRINT", "data": "Congratulations %s! You win." % player.name}
				response = send_recv(player.client, msg)

				msg = {"cmd": "PRINT", "data": "Final board: \n" + str(game)}
				response = send_recv(player.client, msg)

				msg = {"cmd": "PRINT", "data": "Sorry %s! You lose." % idle_player.name}
				response = send_recv(idle_player.client, msg)

				# Tell the clients to stop
				msg = {"cmd": "QUIT", "data": ""}
				response = send_recv(player.client, msg)
				response = send_recv(idle_player.client, msg)

				# End game
				player.client.close()
				idle_player.client.close()
				server.close()

				sys.exit(0)
			# Check if the board is full
			if game.check_draw():
				logging.info("Game drawn.")

				msg = {"cmd": "PRINT", "data": "The game ends in a draw."}
				response = send_recv(player.client, msg)
				response = send_recv(idle_player.client, msg)

				# End game
				player.client.close()
				idle_player.client.close()
				server.close()

				sys.exit(0)

			logging.debug("Successful turn by %s" % player.name)

			# Switch the turn to the other player
			game.turn = not game.turn
		else:
			logging.debug("Bad turn by %s" % player.name)

			msg = {"cmd": "PRINT", "data": "Invalid turn, try again."}
			response = send_recv(player.client, msg)

timeout = 60
buf_size = 2048

if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		sys.exit(0)
