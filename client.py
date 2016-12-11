import socket
import logging
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit

app = None
BUTTON_ZERO = '0'
BUTTON_ONE = '1'
BUTTON_TWO = '2'
BUTTON_THREE = '3'


class Client():
    def __init__(self):
        self.s = None
        self.running = False

    def start(self, address):
        if not self.running:
            self.s = socket.socket()
            self.s.connect((address, 9090))
            self.running = True

    def press_button(self, btn):
        self.s.send(btn.encode())

    def close(self):
        self.running = False
        self.s.close()


class Window():
    def _place_button(self, text, x, y, widget, flag):
        button = QPushButton(text, widget)
        button.resize(60, 40)
        button.move(x, y)
        button.clicked.connect(lambda: self.server.press_button(flag))

    def create(self, server):
        def press_button(flag):
            server.press_button(flag)

        self.server = server
        app = QApplication(sys.argv)
        w = QWidget()
        w.resize(180, 160)
        self._place_button('Button 1', 20, 60, w, BUTTON_ZERO)
        self._place_button('Button 2', 90, 60, w, BUTTON_ONE)
        self._place_button('Button 3', 20, 110, w, BUTTON_TWO)
        self._place_button('Button 4', 90, 110, w, BUTTON_THREE)
        self.textbox = QLineEdit(w)
        self.textbox.move(10, 10)
        self.textbox.resize(120, 40)  # 160
        change_address_btn = QPushButton('OK', w)
        change_address_btn.resize(30, 40)
        change_address_btn.move(140, 10)
        change_address_btn.clicked.connect(self.change_ip())
        w.setWindowTitle('Client')
        w.show()
        try:
            sys.exit(app.exec_())
        except KeyboardInterrupt:
            # Exit application
            pass

    def change_ip(self):
        def click():
            textbox_value = self.textbox.text().replace(' connected', '')
            self.textbox.setText('Wait . . .')
            if self.server.running:
                self.server.close()
            try:
                self.server.start(textbox_value)
                self.textbox.setText(textbox_value + ' connected')
            except socket.gaierror:
                self.textbox.setText('Invalid address')
            except ConnectionRefusedError:
                self.textbox.setText('Connection refused')

        return click


def main():
    window = Window()
    window.create(Client())


if __name__ == '__main__':
    main()
