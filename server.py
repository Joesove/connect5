#!/usr/bin/env python3

from socket import AF_INET, socket, SOCK_STREAM, gethostname
import json
import logging
# import numpy

class Player:
	def __init__(self, client, client_addr, name, player_num):
		self.client = client
		self.client_addr = client_addr
		self.name = name
		self.player_num = player_num

def main():
	logging.basicConfig(level=logging.DEBUG)
	
	players = {}

	host = gethostname()
	port = 8000
	buf_size = 2048

	server = socket(AF_INET, SOCK_STREAM)
	server.bind((host, port))

	server.listen(2)
	logging.info("Starting server, waiting for connection")

	# Loop waiting for both clients to connect
	while len(players) < 2:
		# wait for a client 
		client, client_addr = server.accept()
		logging.info("%s:%s has connected." % client_addr)

		# Send msg
		msg = {"cmd":"INFO", "data": ""}
		client.send(bytes(json.dumps(msg), "utf8"))

		response = json.loads( client.recv(buf_size).decode("utf8") )
		logging.info("%s joined." % response["data"])

		p = Player(client, client_addr, response["data"], len(players) + 1)
		players[p.player_num] = p
	
		logging.debug("Player added")

	print("2 players joined")

	# Start game loop
	while True:
		pass


if __name__ == "__main__":
	main()