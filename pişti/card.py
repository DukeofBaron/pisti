import random

BLACK = "\033[30m"
RED = "\033[31m"
RESET = "\033[0m"


class Card():
    def __init__(self,name,color,value):
        self.name = name
        self.color=color
        self.value=value
        self.pisti = False
        self.reveal=True
        self.calculated = False
    
    def __repr__(self):
        return f"{self.value}{self.name}"

class Deck():
    def __init__(self):
        self.cards =[]
    def create_cards(self):
        for _color in ["red","black"]:
            if _color =="red":
                for _name in ["♦","♥"]:
                    for _value in range(2,11):
                        card=Card(_name,_color,_value)
                        self.cards.append(card)
                    for word in ["ace","jack","queen","king"]:
                        card = card=Card(_name,_color,word)
                        self.cards.append(card)
            else:
                for _name in ["♣","♠"]:
                    for _value in range(2,11):
                        card=Card(_name,_color,_value)
                        self.cards.append(card)
                    for word in ["ace","jack","queen","king"]:
                        card = card=Card(_name,_color,word)
                        self.cards.append(card)
    def shuffle(self):
        random.shuffle(self.cards)