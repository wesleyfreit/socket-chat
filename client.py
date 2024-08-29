import socket
import threading


class Client:
    def __init__(self, host="127.0.0.1", port=55555):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))
        self.nickname = None
        self.running = True

    def send_message(self, message):
        self.client.send(message.encode("utf-8"))

    def display_message(self, message):
        # Here can be used to change the displayed message format
        match message.split(" ")[0]:
            case _:
                print(message)

    def receive_messages(self, client):
        while self.running:
            message = client.recv(1024).decode("utf-8")
            if message == "!nick":
                nickname = input(f"{message} ")
                self.client.send(f"!nick {nickname}".encode("utf-8"))
                self.nickname = nickname
            elif message.split(" ")[0] == "!exit":
                self.display_message(message)
                self.running = False
                break
            elif message:
                self.display_message(message)

    def connect(self):
        try:
            thread = threading.Thread(target=self.receive_messages, args=(self.client,))
            thread.start()

            while self.running:
                if self.nickname:
                    message = input()
                    self.send_message(message)
        except:
            self.client.close()
            return


if __name__ == "__main__":
    client = Client()
    client.connect()
