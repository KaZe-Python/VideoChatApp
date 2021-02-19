import socket, sys, threading
from uuid import uuid4

def uuid_assign(user_list : list) -> str:
    while True:
        uuid = uuid4()
        if(not(uuid in user_list)):
            break
    return uuid

class Server:
    def __init__(self, destination, port):
        self.addr = destination
        self.port : int = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.addr, self.port))
        self.user_list = {}
        self.k, self.v = list(self.user_list.keys()), tuple(self.user_list.values())
        #self.recv_thread : threading.Thread = threading.Thread(target=self.recv_video)
        #self.send_thread : threading.Thread = threading.Thread(target=self.send_video)

    def on_connection_handler(self, conn, addr):
        def send_video(data) -> None:
            while True:
                for client in self.v:
                    if client == conn:
                        continue
                    client.send(data)
        while True:
            data = conn.recv(5120)
            data = data.decode("utf-8")
            if data:
                send_video(data)
                continue
            break
    
    def start(self):
        run = True
        self.sock.listen(5)
        try:
            while run:          
                #Accepting every new connection, and binding them with a thread
                conn, addr = self.sock.accept()
                threading.Thread(target=self.on_connection_handler, args=(conn,addr))

                #Storing clients IPs
                try:
                    self.user_list.update({uuid_assign(self.user_list) : conn})
                except Exception as e:
                    pass

                print("Data Coming")
        except KeyboardInterrupt:
            run = False

if __name__ == "__main__":
    s = Server("localhost", 5555)
    s.start()
