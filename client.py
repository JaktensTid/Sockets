import socket
import logging
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton

app = None
BUTTON_ZERO = '0'
BUTTON_ONE = '1'
BUTTON_TWO = '2'
BUTTON_THREE = '3'

class Client():
	def __init__(self, address, port):
		self.address = address
		self.port = port
		self.s = None

	def start(self):
		self.s = socket.socket()
		self.s.connect((self.address, self.port))

	def press_button(self, btn):
		print(btn)
		self.s.send(btn.encode())

	def close(self):
		self.s.close()

	#Implemening disposable object to use with 'with'
	def __enter__(self):
		self.start()
		return self

	def __exit__(self, exc_type, exc_value, traceback):
		if exc_type is not None:
			logging.error('Type: ' + str(exc_type) + 
				'. Value: ' + str(exc_value) + '. Traceback: ' + str(traceback))
		self.close()


class Window():
	def _place_button(text, x,y, widget, press_event):
		button = QPushButton(text, widget)
		button.resize(60,40)
		button.move(x,y)
		button.clicked.connect(press_event)

	def create(self, handler):
		def press_button(flag):
			handler.press_button(flag)

		app = QApplication(sys.argv)
		w = QWidget()
		w.resize(180, 110)
		self._place_button('Button 1', 20, 10, w, lambda: handler.press_button(BUTTON_ZERO))
		self._place_button('Button 2', 90, 10, w, lambda: handler.press_button(BUTTON_ONE))
		self._place_button('Button 3', 20, 60, w, lambda: handler.press_button(BUTTON_TWO))
		self._place_button('Button 4', 90, 60, w, lambda: handler.press_button(BUTTON_THREE))
		w.setWindowTitle('Client')
		w.show()
		try:
			sys.exit(app.exec_())
		except KeyboardInterrupt:
			#Exit application
			pass

def main():
	with Client('localhost',9090) as client:
		window = Window()
		window.create(client)

if __name__ == '__main__':
	main()