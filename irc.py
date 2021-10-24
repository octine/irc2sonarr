import socket
import time
import re


class IRC:
    def __init__(self):
        self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, server, port, nick):
        # Connect to server
        self.irc.connect((server, port))
        self.irc.send(bytes('PASS {a} \n'.format(a=nick), 'UTF-8'))
        self.irc.send(bytes('NICK {a} \n'.format(a=nick), 'UTF-8'))
        self.irc.send(bytes('USER {a} {a} {a} {a} \n'.format(a=nick), 'UTF-8'))

        # Wait for PING and respond with PONG
        self.pong(self.irc.recv(2048).decode("UTF-8").strip('\n\r'))
        print("{}: Connected to server {} as {}".format(time.asctime(), server, nick))

    def pong(self, msg):
        self.irc.send(bytes(msg.replace('PING', 'PONG') + '\n', "UTF-8"))

    def join(self, channel):
        # Join Channel
        self.irc.send(bytes('JOIN {} \n'.format(channel), 'UTF-8'))
        while (msg := self.irc.recv(2048).decode('UTF-8').strip('\n\r')).find("End of /NAMES list.") == -1:
            pass
        print("{}: Joined channel {}".format(time.asctime(), channel))

    def receive(self):
        ret = []
        for msg in self.irc.recv(4096).decode("UTF-8", "ignore").replace('\r', '').split('\n'):
            if msg.find("PING :") != -1:
                self.pong(msg)
            elif msg.find("PRIVMSG") >= 0:
                ret.append(re.findall("(?<=:)(.*)(?=!)(?:.*)(?<=PRIVMSG)(?:.* :)(.*)", msg)[0])
        return ret

    def quit(self, msg):
        self.irc.send(bytes('QUIT :{} \n'.format(msg), 'UTF-8'))
