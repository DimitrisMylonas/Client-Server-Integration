import socket
import json


class Client(object):
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_adress = ''
        self.server_port = 10000
        self.connect_with_server()
        
		
    def connect_with_server(self):
        print('For read: read <id>')
        print('For write: write <id> <status> <time>')
        print('For delete: delete <id>')
        print('For exit: exit')
		
        self.socket.connect(('127.0.0.1', 10000))

        while True:
            msg = input('Enter your message: ')
            if msg == 'exit':
                print('Exit')
                self.socket.sendall('{}'.format('exit').encode('utf-8'))
                self.socket.close()
                break

            self.socket.sendall('{}'.format(msg).encode('utf-8'))
            data = self.socket.recv(1024).decode('utf-8')
            print(data)

        self.socket.close()


if __name__ == "__main__":
    client = Client()