from msilib.schema import Error
import selectors
import socket
import threading
import connectionHandler
from exceptions import InitilizationError

class Server:

    ACCEPT_CONNECTION = 0

    READ_FROM_CLIENT = 1

    def __init__(self, port):
        self.port = port
        self.selector = selectors.DefaultSelector()
        self.initlized = False
        self.oneToOneConnection=True

    def bind(self):
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocket.bind(('127.0.0.1', self.port))
        self.serverSocket.listen(100)
        self.serverSocket.setblocking(False)
        self.selector.register(
            self.serverSocket, selectors.EVENT_READ, data=(self.ACCEPT_CONNECTION))
        self.initlized = True
        self.__selectHandler()
        

    def registerInComingClients(self, onNewClientComming):
        if onNewClientComming is None:
            raise ValueError("New Client Coming Method Can't be None")
        if self.initlized:
            raise InitilizationError("Server  Is Binded")

        self.newClientFunc = onNewClientComming

    

    def __acceptConnection(self):
        clientSocket,addr=self.serverSocket.accept()
        clientSocket.setblocking(True)
        return clientSocket,addr
    
    def __selectHandler(self):
        while True:
            selection = self.selector.select()
            print("selection")
            for key, mask in selection:
                data = key.data
                print(data)
                if data == self.ACCEPT_CONNECTION:
                    print("data")
                    conn,addr=self.__acceptConnection()
                    client=connectionHandler.ConnectionHandler(self.oneToOneConnection,conn,addr)
                    
                    thread=threading.Thread(target=self.newClientFunc,args=(client,))
                    thread.start()
                
def a(a):
    print(a.getAddr())
    a.acceptConnection()
    print(a.readNessage())
s=Server(1111)
s.registerInComingClients(a)
s.bind()