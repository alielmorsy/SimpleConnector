import selectors
import  socket
from time import sleep
from exceptions import ConnectionAlreadyAcceptedError
class ConnectionHandler:

    def __init__(self,oneToOneConnection,conn,addr):
        self.conn = conn
        self.addr = addr
        
        self.accepted=False
        self.connected=True
        self.oneToOneConnection=oneToOneConnection
        if oneToOneConnection:
            self.selection=selectors.DefaultSelector()

    def getAddr(self):
        return self.addr

    def  acceptConnection(self):
        if self.accepted:
            raise ConnectionAlreadyAcceptedError("Connection Accepted already")
        pass
        self.conn.sendall(b'{"status":"accepted"}')
    
    def disconnect(self):
        if self.registered:
            self.selection.unregister(self.conn)

        self.conn.sendall(b'{"action":"disconnect"}')
        sleep(50)
        self.conn.close()
    
    def sendMessage(self, message):
        if type(message) is str:
            self.conn.sendall(str.encode(message))
        elif type(message) is bytes:
            self.conn.sendall(message)
        else:
            raise ValueError("Message Should be string or bytes only")


    def readNessage(self,buffSize=1024):
        data= self.conn.recv(buffSize)

        if data:
            return str(data.decode())
        else:
            self.connected=False
            return None
    
    def isConnected(self):
        return self.connected