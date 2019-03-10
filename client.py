#!/usr/bin/env python3

# Created by : Joseph Harte
#       Date : March 2019
#    Version : 1.0

from socket import AF_INET, socket, SOCK_STREAM, gethostname
import json
import logging
import sys

def send_msg(client, message):
	try:
		client.send(bytes(json.dumps(message), "utf-8"))
		logging.debug("Message send successfully")
	except:
		logging.error("Cannot send to server")
		client.close()
		sys.exit(1)


def main():
	client = socket(AF_INET, SOCK_STREAM)
	host = gethostname()
	port = 8000
	buf_size = 2048

	# Connect to the server
	try:
		client.connect((host, port))
		logging.info("Connected to server.")
	except:
		logging.error("Cannot connect to server")
		client.close()
		sys.exit(1)
	
	# Start the main client loop
	while True:
		try:
			msg = json.loads( client.recv(buf_size).decode("utf8") )
		except:
			print ("Disconnected from the server.")
			logging.error("Disconnected from the server")
			sys.exit(1)

		if msg["cmd"] == "INFO":
			# Get the player name form the user
			name = input("Please input your name and press enter: ")
			logging.info("Name: %s" % name)

			response = {"done": True, "data": name}
			send_msg(client, response)

		elif msg["cmd"] == "QUIT":
			# Quit the game
			print ("Quitting game.")
			logging.info("Quitting game.")

			response = {"done": True, "data": ""}
			send_msg(client, response)

			client.close()
			sys.exit(0)
		elif msg["cmd"] == "PRINT":
			# Print a message from the server
			print (msg["data"])

			response = {"done": True, "data": ""}
			send_msg(client, response)
		elif msg["cmd"] == "TURN":
			# Prompt the player for their turn
			while True:
				turn = input("It’s your turn %s, please enter column (1-9): " % msg["data"])
				try:
					int(turn)
					break
				except:
					print("You did not enter a number, try again.")

			response = {"done": True, "data": int(turn) - 1}
			send_msg(client, response)
		else:
			logging.error("Unkown command")

if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		sys.exit(0)