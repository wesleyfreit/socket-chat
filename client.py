import socket
import threading


class Client:
    def __init__(self, host="127.0.0.1", port=55555):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))

    def send_message(self, message):
        self.client.send(message.encode("utf-8"))

    def receive_messages(self, client):
        while True:
            try:
                message = client.recv(1024).decode("utf-8")
                if message:
                    print(message)
                else:
                    break
            except:
                print("Connection lost!")
                client.close()
                break

    def connect(self):
        nickname = input("Choose your nickname: ")

        if not nickname:
            print("Invalid nickname, connection lost!")
            self.client.close()
            return

        try:
            self.client.send(f"!nick {nickname}".encode("utf-8"))

            thread = threading.Thread(target=self.receive_messages, args=(self.client,))
            thread.start()
        except:
            print("Connection lost!")
            self.client.close()
            return

        while True:
            try:
                message = input()

                match message.split(" ")[0]:
                    case "!sendmsg":
                        self.send_message(message)
                    case "!changenickname":
                        self.send_message(message)
                    case "!poke":
                        self.send_message(message)
                    case _:
                        print("Invalid command!")
            except:
                print("Connection lost!")
                self.client.close()
                break


if __name__ == "__main__":
    client = Client()
    client.connect()
