#!/usr/bin/env python3

# Created by : Joseph Harte
#       Date : March 2019
#    Version : 1.0

from socket import AF_INET, socket, SOCK_STREAM, gethostname
import json
import logging
import sys

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
	
	# Setup
	host = gethostname()
	port = 8000

	server = socket(AF_INET, SOCK_STREAM)
	server.bind((host, port))

	server.listen(1)
	logging.info("Starting test server")

	client, client_addr = server.accept()
	client.settimeout(timeout)

	fail = False

	# Test the PRINT cmd
	msg = {"cmd": "PRINT", "data": "Enter name as tester"}
	response = send_recv(client, msg)

	try:
		assert response["done"] == True
	except AssertionError:
		logging.error("PRINT test failed. Response: %s" % json.dumps(response))
		fail = True
	else:
		logging.info("PRINT test successful.")

	# Test the INFO cmd
	msg = {"cmd": "INFO", "data": ""}
	response = send_recv(client, msg)

	try:
		assert response["done"] == True
		assert response["data"] == "tester"
	except AssertionError:
		logging.error("INFO test failed. Response: %s" % json.dumps(response))
		fail = True
	else:
		logging.info("INFO test successful.")

	# Test the TURN command
	msg = {"cmd": "PRINT", "data": "On first prompt enter tester, on second prompt enter 1"}
	response = send_recv(client, msg)

	msg = {"cmd": "TURN", "data": "tester"}
	response = send_recv(client, msg)

	try:
		assert response["done"] == True
		assert response["data"] == 0
	except AssertionError:
		logging.error("TURN test failed. Response: %s" % json.dumps(response))
		fail = True
	else:
		logging.info("TURN test successful.")

	# Test the QUIT command
	msg = {"cmd": "QUIT", "data": ""}
	response = send_recv(client, msg)

	try:
		assert response["done"] == True
	except AssertionError:
		logging.error("QUIT test failed. Response: %s" % json.dumps(response))
		fail = True
	else:
		logging.info("QUIT test successful.")

	# Teardown
	if fail:
		logging.info("Some tests failed.")
		print ("Test failed.")
	else:
		logging.info("All tests successful.")
		print ("Test successful.")
	client.close()
	server.close()
	sys.exit(0)

buf_size = 2048
timeout = 60

if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		sys.exit(0)