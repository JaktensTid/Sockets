import socket
import logging
import sys
from PyQt5.QtWidgets import QApplication, QWidget

BUTTON_ZERO = '0'
BUTTON_ONE = '1'
BUTTON_TWO = '2'
BUTTON_THREE = '3'

class Server():
	def __init__(self, port, handler=None):
		self.handler = handler
		self.port = port
		self.s = None

	def start(self):
		self.s = socket.socket()
		self.s.bind(('0.0.0.0',9090))

	def listen(self):
		self.s.listen(10)
		connection, address = self.s.accept()
		while True:
			data = connection.recv(1).decode('utf-8')
			if not data:
				break
			print(data)
			#self.handler.get(data)

	def close(self):
		self.s.close()

	#Implemening disposable object to use with 'with'
	def __enter__(self):
		self.start()
		return self

	def __exit__(self, exc_type, exc_value, traceback):
		if exc_type is not None:
			print('Type: ' + str(exc_type) + 
				'. Value: ' + str(exc_value) + '. Traceback: ' + str(traceback))
		self.close()
		

def main():
	with Server(9090) as server:
		server.listen()


if __name__ == "__main__":
	main()