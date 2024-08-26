import socket
import threading


clients = []
nicknames = {}


class Server:
    def __init__(self, host="127.0.0.1", port=55555):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen()

    def broadcast(self, message):
        for client in clients:
            client.send(message)

    def set_client(self, client, nickname):
        nicknames[client] = nickname
        welcome_message = f"!users {len(nicknames)} " + " ".join(
            nicknames.values()
        )
        client.send(welcome_message.encode("utf-8"))

    def change_nickname(self, client, old_nick, new_nick):
        nicknames[client] = new_nick
        self.broadcast(
            f"!changenickname {old_nick} {new_nick}".encode("utf-8")
        )
    
    def poke_user(self, client, target_nick):
        if target_nick in nicknames.values():
            poker_nick = nicknames[client]
            self.broadcast(
                f"!poke {poker_nick} {target_nick}".encode("utf-8")
            )
        else:
            client.send("User not found!".encode("utf-8"))

    def handle_client(self, client):
        while True:
            try:
                message = client.recv(1024).decode("utf-8")

                match message.split(" ")[0]:
                    case "!nick":
                        nickname = message.split(" ")[1]
                        self.set_client(client, nickname)  
                    case "!sendmsg":
                        msg_content = message.split(" ", 1)[1]
                        self.broadcast(
                            f"!msg {nicknames[client]} {msg_content}".encode("utf-8")
                        )
                    case "!changenickname":
                        old_nick = nicknames[client]
                        new_nick = message.split(" ")[1]
                        self.change_nickname(client, old_nick, new_nick)
                    case "!poke":
                        target_nick = message.split(" ")[1]
                        self.poke_user(client, target_nick)
                    case _:
                        client.send("Invalid command!".encode("utf-8"))
            except:
                clients.remove(client)
                client.close()
                del nicknames[client]
                break

    def start(self):
        print("Server is listening...")

        while True:
            try:
                client, address = self.server.accept()
                print(f"Connected with {str(address)}")

                clients.append(client)
                thread = threading.Thread(target=self.handle_client, args=(client,))
                thread.start()
            except:
                print("An error occurred!")
                self.server.close()


if __name__ == "__main__":
    server = Server()
    server.start()
