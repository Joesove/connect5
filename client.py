#!/usr/bin/env python3

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
		msg = json.loads( client.recv(buf_size).decode("utf8") )
		if msg["cmd"] == "INFO":
			# Get the player name form the user
			name = input("Please input your name and press enter: ")
			logging.info("Name: %s" % name)

			response = {"done": True, "data": name}
			send_msg(client, response)

		elif msg["cmd"] == "WAIT":
			pass
		elif msg["cmd"] == "PRINT":
			print (msg["data"])
		elif msg["cmd"] == "TURN":
			turn = input("It’s your turn %s, please enter column (1-9): " % msg["data"])
			logging.info("Name: %s" % name)

			response = {"done": True, "data": turn}
			send_msg(client, response)
		else:
			logging.error("Unkown command")

if __name__ == "__main__":
	main()