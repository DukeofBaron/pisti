import socket
import threading
import pygame
import game
import time
import pickle

class GameClient:
    def __init__(self, server_ip='127.0.0.1', server_port=12345):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((server_ip, server_port))
        self.id = None
        self.running = True
        self.game = None
        print(f"Connected to Server {server_ip}:{server_port}")
    

    def send_message(self, message):
        self.client.send(message.encode())

    def receive_message(self):
        return self.client.recv(1024).decode()
    
    def receive_data(self):
        try:
            data = self.client.recv(4096)
            if data:
                self.game = pickle.loads(data)
                print("Game data received successfully")
            else:
                print("No data received.")
        except Exception as e:
            print(f"Error receiving data: {e}")


    def send_data(self, data):
        try:
            serialized_data = pickle.dumps(data)
            self.client.sendall(serialized_data)
        except Exception as e:
            print(f"Data send error: {e}")

    def listen(self):
            response = self.receive_message()
            self.id = int(response.split(" ")[2].strip())
            print(f"İD: {self.id}")

    def receive_data_thread(self):
        """Thread function to receive data from the server continuously."""
        while self.running:
            self.receive_data()

    def send_data_thread(self):
        while self.running:
            self.send_data(self.game)

    def all_game(self):
        threading.Thread(target=self.receive_data_thread, daemon=True).start(),
        while not self.game: 
            time.sleep(0.1)



        while len(self.game.players) != 2:
            pass

        pygame.init()
        font = pygame.font.Font(None, 74)
        font2 = pygame.font.Font(None, 30)
        notyourturn = font.render("Not Your Turn!", True, (255,0,0))
        nytb = False
        nytt =""
        saat = pygame.time.Clock()
        screen = pygame.display.set_mode((1900, 1000))
        boşluk = 20
        x = 625
        y = 700
        class çerçeve():
            def __init__(self,x,y,image,details):
                self.x = x
                self.y = y
                self.image = pygame.transform.scale(image, (220, 220))
                self.details = details
                self.rect = pygame.Rect(self.x, self.y, 220, 220)

            def is_clicked(self, pos):
                return self.rect.collidepoint(pos)

            def draw(self):
                screen.blit(self.image,(self.x,self.y))  

            def draw_large(self):
                enlarged_image = pygame.transform.scale(self.image, (260, 260))
                screen.blit(enlarged_image, (self.x - 20, self.y - 20))

        def draw_player_cards():
            çerçeveler = []
            cards = self.game.players[self.id-1].hand
            for i in range(len(cards)):
                resim = pygame.image.load(f"pişti\\cards\\{self.game.players[self.id-1].hand[i]}.png")
                a = çerçeve(x+(i*135),y,resim,cards[i])
                a.draw()
                çerçeveler.append(a)
            return çerçeveler

        class middle():
            def __init__(self,x,y,image,details):
                self.x = x
                self.y = y
                self.image = pygame.transform.scale(image, (175, 175))
                self.details = details
            def draw(self):
                screen.blit(self.image,(self.x,self.y))

        def draw_middle(orta_):
            temp = 0
            orta_ = orta_[-4:]
            for i in orta_:
                if i.reveal == False:
                    resim = pygame.image.load("pişti\\cards\\back.png")
                else:
                    resim = pygame.image.load(f"pişti\\cards\\{i}.png")
                a = middle(730+temp*30,1080/2-150,resim,i)
                a.draw()
                temp+=1

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            screen.fill((0, 150, 0)) 

            çerçeveler = draw_player_cards()
            draw_middle(self.game.middle)
            mouse_pos = pygame.mouse.get_pos()
            büyütülen_kart = None

            for cerceve in çerçeveler:
                if cerceve.rect.collidepoint(mouse_pos):
                    büyütülen_kart = cerceve

            for cerceve in çerçeveler:
                cerceve.draw()

            if büyütülen_kart:
                büyütülen_kart.draw_large()
            if event.type == pygame.MOUSEBUTTONDOWN:   #if it click the selected 
                try:
                    if self.game.queue %2==self.id-1:
                        büyütülen_kart.is_clicked(event.pos)
                        self.game.play_a_card(büyütülen_kart.details,self.id)
                    else :
                        nytb = True
                        nytt = time.time()
                except:
                    pass
                self.send_data(self.game)
                self.game.give_card_all_players()
            if nytb:
                screen.blit(notyourturn, (750, 650))
                if time.time() - nytt > 0.5:
                    nytb = False

            self.game.calculate_points(self.id-1)

            point = font.render(f"Point : {self.game.players[self.id-1].point}",True,(255,0,0))
            screen.blit(point,(1400,870))

            remained_Cards = font.render(f"{self.game.amount_of_cards()}",True,(255,0,0))
            screen.blit(remained_Cards,(1120,320))

            screen.blit(pygame.transform.scale(pygame.image.load(f"pişti\\cards\\back.png"),(180,180)),(1920/2+100,1080/2-150))#middle deck remained cards amount
            pygame.display.flip()
            saat.tick(60)

        pygame.quit()


if __name__ == "__main__":
    game = GameClient()
    game.listen()
    game.all_game()
