import socket
from threading import Thread, Lock
import json
import time
import random


fligths = [
            {'id': 1, 'status': 'Departure', 'time': '10:10'},
            {'id': 2, 'status': 'Departure', 'time': '00:00'},
            {'id': 3, 'status': 'Arrival', 'time': '21:00'},
			{'id': 4, 'status': 'Arrival', 'time': '21:50'},
            {'id': 5, 'status': 'Departure', 'time': '00:50'},
            {'id': 6, 'status': 'Arrival', 'time': '13:30'},
			{'id': 7, 'status': 'Arrival', 'time': '12:00'},
            {'id': 8, 'status': 'Departure', 'time': '15:30'},
            {'id': 9, 'status': 'Arrival', 'time': '19:30'},
			{'id': 10, 'status': 'Arrival', 'time': '07:00'}
        ]

class Server(object):
    def __init__(self):
        self.lock = Lock()
        self.Lock = Lock()
        self.address = '127.0.0.1'
        self.port = 10000
        self.flights = fligths
        self.max_read_time = 3
        self.max_write_time = 5

    def read_flight(self, flight_id):

        found_flight = None
        time.sleep(random.randrange(0, self.max_read_time))
        self.Lock.acquire() 
        for flight in self.flights:
            if flight_id == flight['id']:
                found_flight = flight
                self.Lock.release() 
                break

        return found_flight
    
    def write_flight(self, id, status, flight_time):
        self.lock.acquire()
        for flight in self.flights:
            if int(id) == flight['id']:
                self.lock.release()
                return False

        time.sleep(random.randrange(0, self.max_write_time))  # delay the write
        new_flight = {
            'id': int(id),
            'status': status,
            'time': flight_time
            }
        self.flights.append(new_flight)
        self.lock.release()
        return True

    def delete_flight(self, id):
        for flight in self.flights:
            if int(id) == flight[id]:
                self.remove.flight[flight_id]
                break


    def handle_client_request(self, connection):
        while True:
            client_request_message = connection.recv(1024).decode ('utf-8')

            if 'exit' in client_request_message:
                print('Client exited')
                break
            elif 'read' in client_request_message:
                _, flight_id = client_request_message.split()
                flight = self.read_flight(int(flight_id))

                if flight is not None:
                    response = 'ROK ' + str(flight['id']) + ' ' + flight['status'] + ' ' + flight['time'] 
                    connection.sendall(response.encode('utf-8')) 
                else:
                    connection.sendall('RERR Flight not found'.encode('utf-8'))

            elif 'write' in client_request_message:
                _, id, status, flight_time = client_request_message.split()
                not_exists = self.write_flight(id, status, flight_time) 
                if not_exists:
                    connection.sendall('WOK Flight added'.encode('utf-8')) 
                else:
                    connection.sendall('WERR Flight already exists'.encode('utf-8'))

            elif 'delete' in client_request_message:
                _, flight_id = client_request_message.split()
                flight = self.read_flight(int(flight_id))

                if flight is not None:
                    self.delete_flight(flight_id)
                    connection.sendall('Flight deleted'.encode('utf-8'))
                else:
                    connection.sendall('Flight not found'.encode('utf-8'))

            else:
                connection.sendall('RERR Wrong choice'.encode('utf-8')) 

    def start_listening(self):
        connection_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connection_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        connection_sock.bind((self.address, self.port))
        connection_sock.listen(1)
        print('Server started')

        while True:
            connection, address = connection_sock.accept()
            print('Connection oppened from client : ', address)
            thread = Thread( target=self.handle_client_request, args=(connection,))
            thread.start()    
        connection_sock.close()



if __name__ == "__main__":
    server = Server()
    server.start_listening()
