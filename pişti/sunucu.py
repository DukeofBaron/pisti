import game
import socket
import threading
import pickle
import time


class GameServer:
    def __init__(self, host='127.0.0.1', port=12345):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen(5)
        self.players = []
        print(f"Server started on {host}:{port}")
        self.Game=game.Game()

    def handle_client(self, client_socket, addr, player_id):
        print(f"Player {player_id} connected from {addr}")
        client_socket.send(f"Welcome Player {player_id}".encode())
        initial_game_data = pickle.dumps(self.Game)
        client_socket.sendall(initial_game_data)

        while True:
            try:
                data = client_socket.recv(4096)
                if not data:
                    break
                self.Game = pickle.loads(data)

                for player in self.players:
                    if player != client_socket: 
                        game_data = pickle.dumps(self.Game)
                        player.sendall(game_data)
            except:
                pass
            time.sleep(1)

    def start(self):
        while True:
            client_socket, addr = self.server.accept()
            player_id = len(self.players) + 1
            self.Game.add_player()
            self.players.append(client_socket)
            for player in self.players:
                if player != client_socket: 
                    game_data = pickle.dumps(self.Game)
                    player.sendall(game_data)
            threading.Thread(target=self.handle_client, args=(client_socket, addr, player_id)).start()

if __name__ == "__main__":
    server = GameServer()
    server.start()

