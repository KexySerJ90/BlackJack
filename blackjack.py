from art import logo
from random import shuffle


class Card:

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f'{self.suit}{self.rank}'

    def __getitem__(self, key):
        return self.rank


class Deck:
    '''Класс колоды и всего игрового процесса'''
    __suits = ("♣️", "♢", "♡", "♠️")
    __ranks = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10, "J": 10, "Q": 10, "K": 10,
               "A": 11}

    def __init__(self, player=[], comp=[]):
        self.d = [Card(s, r) for s in self.__suits for r in self.__ranks]
        self.player = player
        self.comp = comp

    def shuffle(self):
        print(Deck.cards_in_deck(self))
        if len(self.d) == 52:
            shuffle(self.d)
        else:
            self.d = [Card(s, r) for s in self.__suits for r in self.__ranks]
            shuffle(self.d)

    def _check_type(func):
        def wrapper(self, *args):
            if not self.d:
                raise ValueError('Все карты разыграны')
            return func(self, *args)

        return wrapper

    def do_twice(func):
        def wrapper(*args, **kwargs):
            func(*args, **kwargs)
            return func(*args, **kwargs)

        return wrapper

    @do_twice
    @_check_type
    def deal(self, to):
        if to == 'player':
            self.player.append(self.d.pop())
            return Deck(self.player)
        elif to == 'comp':
            self.comp.append(self.d.pop())
            return Deck(self.comp)

    def say(self):
        a = input("Берем еще?(если нажмежь 'y', то продолжаем: ")
        while a == 'y' and Deck.summa_player(self) < 22:
            self.player.append(self.d.pop())
            print(Deck.cards_in_deck(self))
            print(f'Карты игрока: {Deck(self.player)}', f'Количество очков:{Deck.summa_player(self)}', sep='\n')

            if Deck.summa_player(self) < 22:
                a = input("Берем еще?(если нажмежь 'y', то продолжаем: ")
            else:
                print('Вы Перебрали')
        return Deck(self.player)

    def cards_in_deck(self):
        return f'Карт в колоде: {len(self.d)}'

    def __str__(self):
        return ', '.join([str(card) for card in self.player])

    def __getitem__(self, key):
        if isinstance(key, slice):
            return Deck(self.player[key])
        return self.player[key]

    def summa_player(self):
        k = 0
        for i in self.player:
            if i[1:] in self.__ranks and i[1:] != 'A':
                k += self.__ranks[i[1:]]
            if i[1:] == 'A' and k < 11:
                k += 11
            elif i[1:] == 'A' and k > 11:
                k += 1
        return k

    def summa_comp(self):
        return sum(self.__ranks[card.rank] for card in self.comp if card.rank in self.__ranks)

    def win(self):
        if Deck.summa_player(self) > Deck.summa_comp(self) and Deck.summa_player(self) < 22:
            print('Вы победили')
        elif Deck.summa_player(self) == Deck.summa_comp(self):
            print('Ничья')
        else:
            print('Вы проиграли')

    def com(self):
        return ', '.join([str(card) for card in self.comp])


def let_play(game=Deck()):
    print(logo)
    game.shuffle()
    print(f'Карты игрока {game.deal("player")}')
    print(f'Карты компьютера {game.deal("comp")[0]} и ?')
    print(f'Количество очков: {game.summa_player()}')
    game.say()
    game.win()
    print(f'Карты компьютера {game.com()}')
    a = input("Играем еще раз(нажмите 'y')")
    if a == 'y':
        let_play(game=Deck(player=[], comp=[]))


let_play()
