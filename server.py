import socket
import signal
import sys
import threading
from PyQt5.QtWidgets import QApplication, QWidget, QFrame, QLineEdit, QPushButton

BUTTON_ZERO = '0'
BUTTON_ONE = '1'
BUTTON_TWO = '2'
BUTTON_THREE = '3'

server_thread = None


def signal_handler(signal, frame):
    print('Signal')
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)


class Server():
    def __init__(self, handler):
        self.s = None
        self.handler = handler
        self.running = False

    def start(self):
        self.s = socket.socket()
        self.s.bind(('0.0.0.0', 9090))
        self._listen()

    def _listen(self):
        self.s.listen(10)
        print('Listening')
        self.running = True
        connection, address = self.s.accept()
        self.handler.connected(address)
        while True:
            try:
                data = connection.recv(1).decode('utf-8')
                if not data:
                    break
                print(data)
                self.handler.get(data)
            except ConnectionResetError:
                print('Connection closed')
                self.handler.reset()
                self._listen()

    def close(self):
        self.s.close()


class Window():
    def set_white(self, square):
        square.setStyleSheet('QWidget { background-color: #FFFFFF}')

    def set_black(self, square):
        square.setStyleSheet('QWidget { background-color: #000000}')

    def reset_color(self, square):
        square.setStyleSheet('QWidget { background-color: #F0FFF0}')

    def create(self, thread):
        app = QApplication(sys.argv)
        w = QWidget()
        self.textbox = QLineEdit(w)
        self.textbox.move(10, 10)
        self.textbox.resize(120, 40)
        self.textbox.setText('Not connected')
        self.textbox.setReadOnly(True)
        self.square1 = QFrame(w)
        self.square1.setGeometry(10, 60, 192, 192)
        self.square2 = QFrame(w)
        self.square2.setGeometry(212, 60, 192, 192)
        self.reset_color(self.square1)
        self.reset_color(self.square2)
        w.resize(414, 262)
        w.setWindowTitle('Server')
        print('Showing')
        w.show()
        try:
            sys.exit(app.exec_())
        except KeyboardInterrupt:
            thread.exit()

    def connected(self, address):
        self.textbox.setText('Connected: ' + address[0])

    def get(self, data):
        if data == BUTTON_ZERO:
            self.set_black(self.square1)
            self.set_black(self.square2)
        if data == BUTTON_ONE:
            self.set_black(self.square1)
            self.set_white(self.square2)
        if data == BUTTON_TWO:
            self.set_white(self.square1)
            self.set_black(self.square2)
        if data == BUTTON_THREE:
            self.set_white(self.square1)
            self.set_white(self.square2)

    def reset(self):
        self.reset_color(self.square1)
        self.reset_color(self.square2)
        self.textbox.setText('Not connected')


def main():
    window = Window()
    server = Server(window)
    server_thread = threading.Thread(target=server.start)
    server_thread.start()
    window.create(server_thread)
    server_thread.join()


if __name__ == "__main__":
    main()
