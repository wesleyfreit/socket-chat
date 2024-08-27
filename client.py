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
                    self.display_message(message)
                else:
                    break
            except:
                client.close()
                break

    def display_message(self, message):
        # Here can be used to change the displayed message format
        match message.split(" ")[0]:
            case "!users":
                # _, users_count, users = message.split(" ", 2)
                # print(f"Users online: {users_count} - {users.replace(' ', ', ')}")
                print(message)
            case "!msg":
                # _, sender, msg_content = message.split(" ", 2)
                # print(f"{sender}: {msg_content}")
                print(message)
            case "!changenickname":
                # _, old_nick, new_nick = message.split(" ", 2)
                # print(f"{old_nick} changed nickname to {new_nick}")
                print(message)
            case "!poke":
                # _, poker_nick, target_nick = message.split(" ", 2)
                # print(f"{poker_nick} poked {target_nick}")
                print(message)
            case _:
                print(message)

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
