import card
import player
import time
class Game():
    def __init__(self):
        self.playercount = 0
        self.players=[]
        self.deck = card.Deck()
        self.queue=0
        self.deck.create_cards()
        self.deck.shuffle()

        self.middle = []
        for i in range(3):
            self.deck.cards[i].reveal = False


        if self.deck.cards[3].value == "jack":
            for i in range(4,len(self.deck.cards)):
                if self.deck.cards[i].value != "jack":
                    self.deck.cards[3] , self.deck.cards[i] = self.deck.cards[i] , self.deck.cards[3]

        for i in range(4):
            self.middle.append(self.deck.cards[i])
        del self.deck.cards[0:4]
    
    def add_player(self):
        self.playercount+=1
        temp = player.Player(self.playercount)
        for i in range(0,4):
            temp.hand.append(self.deck.cards[i])
        del self.deck.cards[0:4]
        self.players.append(temp)
        

    def show_middle(self):
        print(self.middle)
    
    def show_players_hands(self):
        a = 1
        for player in self.players:
            print(f"{a}.Player's Hand:{player.hand}")
            a+=1
    
    def amount_of_cards(self):
        return len(self.deck.cards)

    def play_a_card(self,details,id):
        self.queue+=1
        self.middle.append(details)
        self.players[id-1].hand.remove(details)
        if self.check_is_same(details) or details.value == "jack":
            if self.is_pişti(details):
                self.middle[0].pisti = True
            time.sleep(0.5)
            self.players[id-1].obtained_cards += self.middle
            self.middle.clear()
        
    def check_is_same(self,details):
        if self.middle[-2].value == details.value:
            return True
        return False

    def is_pişti(self,details): 
        if (len(self.middle) == 2) and self.check_is_same(details):
            return True
        return False

    def calculate_points(self,id):
        for card in self.players[id-1].obtained_cards:
            if card.calculated:
                continue
            if card.pisti:  
                self.players[id-1].point += 10
                if card.value =="jack":
                    self.players[id-1].point += 10
            if card.value == 10 and card.name == "♦":
                self.players[id-1].point += 3
            elif card.value == 2 and card.name == "♣":
                self.players[id-1].point += 2
            elif card.value == "jack":
                self.players[id-1].point += 1
            elif card.value == "ace":
                self.players[id-1].point += 1
            card.calculated = True

    def give_card_all_players(self):
        finished = True
        for player in self.players:
            if len(player.hand) == 0:
                pass
            else:
                finished = False

        if finished:
            for player in self.players:
                for i in range(0,4):  #gave the cards
                    player.hand.append(self.deck.cards[i])
                del self.deck.cards[0:4]
