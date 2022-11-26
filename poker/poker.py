from itertools import groupby
from dataclasses import dataclass
from typing import (
    Callable,
    Iterator,
    List,
    Optional,
    Sequence,
    Tuple,
    TypeVar,
    Union,
)

T = TypeVar("T", bound="OrderedEnum")

from ordered_enum import OrderedEnum, prev_value


class Suit(OrderedEnum):
    C = "C"
    D = "D"
    S = "S"
    H = "H"

class Value(OrderedEnum):
    def __str__(self):
        return self.value

    TWO = "2"
    THREE = "3"
    FOUR = "4"
    FIVE = "5"
    SIX = "6"
    SEVEN = "7"
    EIGHT = "8"
    NINE = "9"
    TEN = "T"
    JACK = "J"
    QUEEN = "Q"
    KING = "K"
    ACE = "A"




class Rank(OrderedEnum):
    HIGH_CARD = "HIGH_CARD"
    ONE_PAIR = "ONE_PAIR"
    TWO_PAIRS = "TWO_PAIRS"
    THREE_OF_A_KIND = "THREE_OF_A_KIND"
    FOUR_OF_A_KIND = "FOUR_OF_A_KIND"
    FLUSH = "FLUSH"
    FULL_HOUSE = "FULL_HOUSE"
    STRAIGHT = "STRAIGHT"
    STRAIGHT_FLUSH = "STRAIGHT_FLUSH"
    ROYAL_FLUSH = "ROYAL_FLUSH"


class InvalidCard(Exception):
    def __init__(self, invalid_card: str):
        super().__init__(f"Invalid card \"{invalid_card}\"")
        self.invalid_card = invalid_card 

@dataclass(order=True, frozen=True)
class Card:
    value: Value
    suit: Suit

    @staticmethod
    def from_string(str: str):
        """
        >>> Card.from_string("")
        Traceback (most recent call last):
        ...
        InvalidCard: Invalid card ""

        >>> Card.from_string("9HA")
        Traceback (most recent call last):
        ...
        InvalidCard: Invalid card "9HA"

        >>> Card.from_string("RH")
        Traceback (most recent call last):
        ...
        InvalidCard: Invalid card "RH"

        >>> Card.from_string("7R")
        Traceback (most recent call last):
        ...
        InvalidCard: Invalid card "7R"
                
        >>> Card.from_string("TH")
        TH
        """
        if len(str) != 2: raise InvalidCard(str)
        suit_str = str[1]
        if suit_str not in Suit: raise InvalidCard(str)
        value_str = str[0]
        if value_str not in Value: raise InvalidCard(str)

        return Card(suit=Suit(suit_str), value=Value(value_str))

    def __repr__(self) -> str:
        suit_str = self.suit.value
        value_str = self.value.value
        return f"{value_str}{suit_str}"


@dataclass(order=True, frozen=True)
class Score:
    """
    >>> Score(Rank.ONE_PAIR, []) < Score(Rank.TWO_PAIRS, [])
    True
    >>> Score(Rank.ONE_PAIR, []) > Score(Rank.TWO_PAIRS, [])
    False
    >>> Score(Rank.ONE_PAIR, []) == Score(Rank.ONE_PAIR, [])
    True
    """

    rank: Rank
    highest_cards: List[Value]

    
    def __repr__(self) -> str:
        return f"{self.rank.value},{[x.value for x in self.highest_cards]}"

    
    @staticmethod
    def make(rank: Rank, *, hand: List[Card] = [], matched: Optional[List[Card]] = None):
        if matched is not None:
            assert hand is not None
            return Score(rank, Cards.values(matched + Cards.diff(hand, matched)))
        return Score(rank, Cards.values(hand))


class Cards:
    @staticmethod
    def from_string(str: str) -> List[Card]:
        """
        >>> Cards.from_string("")
        []

        >>> Cards.from_string("7H")
        [7H]

        >>> Cards.from_string("7H TD")
        [7H, TD]
        
        """
        return [Card.from_string(x.strip()) for x in str.split(" ")] if str.strip() != "" else []

    @staticmethod
    def values(hand: Union[Sequence[Card], Iterator[Card]]) -> List[Value]:
        """
        >>> Cards.values([])
        []

        >>> Cards.values([Card(Value.SEVEN, Suit.H), Card(Value.ACE, Suit.D)])
        [<Value.SEVEN: '7'>, <Value.ACE: 'A'>]

        """
        return [x.value for x in hand]

    @staticmethod
    def group_by(
        hand: List[Card], key: Callable[[Card], T]
    ) -> List[Tuple[T, List[Card]]]:
        """
        >>> Cards.group_by(Cards.from_string("7H"), lambda card: card.value)
        [(<Value.SEVEN: '7'>, [7H])]

        >>> Cards.group_by(Cards.from_string("7H 7D 7S"), lambda card: card.value)
        [(<Value.SEVEN: '7'>, [7D, 7S, 7H])]

        >>> Cards.group_by(Cards.from_string("7H 7D 7S 8H"), lambda card: card.value)
        [(<Value.SEVEN: '7'>, [7D, 7S, 7H]), (<Value.EIGHT: '8'>, [8H])]

        >>> Cards.group_by(Cards.from_string("7H"), lambda card: card.suit)
        [(<Suit.H: 'H'>, [7H])]

        >>> Cards.group_by(Cards.from_string("7H 7D 7S 8H"), lambda card: card.suit)
        [(<Suit.D: 'D'>, [7D]), (<Suit.S: 'S'>, [7S]), (<Suit.H: 'H'>, [7H, 8H])]
        """
        return [
            (k, list(sorted(g)))
            for k, g in groupby(
                sorted(hand),
                key,
            )
        ]

    @staticmethod
    def diff(hand1: List[Card], hand2: List[Card]) -> List[Card]:
        """
        >>> Cards.diff(Cards.from_string("TH"), [])
        [TH]
        >>> Cards.diff(Cards.from_string("TH 9H"), Cards.from_string("9H"))
        [TH]
        """
        r = list(reversed(sorted(set(hand1) - set(hand2))))
        return r


class Hand:
    @staticmethod
    def from_string(str: str):
        return Hand(Cards.from_string(str))
    class Has:
        def __init__(self, hand: "Hand", num: int) -> None:
            self.hand = hand
            self.num = num

        def cards_of_same_value(self)->Optional[Tuple[Value, List[Card]]]:
            return next((x for x in self.hand.sorted_by_value if len(x[1]) == self.num), None)

    def __init__(self, cards: List[Card]):
        self.cards = list(sorted(cards))

        self.sorted_by_suit = Cards.group_by(
            list(sorted(self.cards)), lambda card: card.suit
        )
        self.sorted_by_value = Cards.group_by(
            list(sorted(self.cards)), lambda card: card.value
        )

    @property
    def values(self):
            return sorted(Cards.values(self.cards))

    @property
    def is_single_suit(self) -> bool:
        return len(self.sorted_by_suit) == 1

    def has(self, num: int ) ->"Hand.Has": 
        return Hand.Has(self, num)

    @property
    def are_consequitive(self) -> bool:
        return all(
            [
                self.cards[i - 1].value == prev_value(self.cards[i].value)
                for i in range(1, len(self.cards))
            ]
        )


def match_royal_flush(hand: Hand) -> Optional[Score]:
    """
    >>> match_royal_flush(Hand.from_string("TH JH QH KH AH"))
    ROYAL_FLUSH,[]

    >>> match_royal_flush(Hand(Cards.from_string("AH TH JH QH KH")))
    ROYAL_FLUSH,[]

    >>> match_royal_flush(Hand(Cards.from_string("9H JH QH KH AH")))
    """
    if hand.is_single_suit and hand.values == [
        Value.TEN,
        Value.JACK,
        Value.QUEEN,
        Value.KING,
        Value.ACE,
    ]:
        return Score.make(Rank.ROYAL_FLUSH)

def match_straight_flush(hand: Hand) -> Optional[Score]:
    """
    >>> match_straight_flush(Hand(Cards.from_string("QH JH TH 9H 8H")))
    STRAIGHT_FLUSH,['8', '9', 'T', 'J', 'Q']

    >>> match_straight_flush(Hand(Cards.from_string("QH JH TH 9H 7H")))
    """
    if hand.is_single_suit and hand.are_consequitive:
        return Score.make(Rank.STRAIGHT_FLUSH, matched=hand.cards, hand=hand.cards)
    
def match_four_of_a_kind(hand: Hand) -> Optional[Score]:
    """
    >>> match_four_of_a_kind(Hand(Cards.from_string("9C 9S 9D 9H JH")))
    FOUR_OF_A_KIND,['9', '9', '9', '9', 'J']

    >>> match_four_of_a_kind(Hand(Cards.from_string("9C 9S 9D 7H JH")))
    """
    if m := hand.has(4).cards_of_same_value():
        return Score.make(Rank.FOUR_OF_A_KIND, matched=m[1], hand=hand.cards)

def match_full_house(hand: Hand) -> Optional[Score]:
    """
    >>> match_full_house(Hand.from_string("3C 3S 3D 6C 6H"))
    FULL_HOUSE,['3', '3', '3', '6', '6']

    >>> match_full_house(Hand.from_string("6C 6H 3C 3S 3D"))
    FULL_HOUSE,['3', '3', '3', '6', '6']

    >>> match_full_house(Hand.from_string("6C 6H 3C 3S 5D"))
    """
    if three := hand.has(3).cards_of_same_value():
        if pair := hand.has(2).cards_of_same_value():
            return Score.make(
                Rank.FULL_HOUSE, matched=three[1] + pair[1], hand=hand.cards
            )
    return None

def match_flush(hand: Hand) -> Optional[Score]:
    if hand.is_single_suit:
        return Score.make(Rank.FLUSH, matched=list(reversed(hand.cards)), hand=hand.cards)

def match_straight(hand: Hand) -> Optional[Score]:
    if hand.are_consequitive:
        return Score.make(Rank.STRAIGHT, matched=hand.cards, hand=hand.cards)

def match_three_of_a_kind(hand: Hand) -> Optional[Score]:
    if three := hand.has(3).cards_of_same_value():
        return Score.make(Rank.THREE_OF_A_KIND, matched=three[1], hand=hand.cards)

def match_two_pairs(hand: Hand) -> Optional[Score]:
    if pair_one := hand.has(2).cards_of_same_value():
        if pair_two := next(
            (x for x in hand.sorted_by_value if len(x[1]) == 2 and x != pair_one), None
        ):
            return Score.make(
                Rank.TWO_PAIRS,
                matched=list(reversed(sorted(list(pair_one[1] + pair_two[1])))),
                hand=hand.cards,
            )

    return None

def match_one_pair(hand: Hand) -> Optional[Score]:
    if pair_one := hand.has(2).cards_of_same_value():
        return Score.make(Rank.ONE_PAIR, matched=pair_one[1], hand=hand.cards)

def match_high_card(hand: Hand) -> Score:
    return Score.make(Rank.HIGH_CARD, matched=list(reversed(hand.cards)), hand=hand.cards)
    
def score(cards: List[Card]) -> Score:
    """
    >>> score(Cards.from_string("TH JH QH KH AH"))
    ROYAL_FLUSH,[]

    >>> score(Cards.from_string("AH TH JH QH KH"))
    ROYAL_FLUSH,[]

    >>> score(Cards.from_string("9H TH JH QH KH"))
    STRAIGHT_FLUSH,['9', 'T', 'J', 'Q', 'K']

    >>> score(Cards.from_string("TH JH QH KH 9H"))
    STRAIGHT_FLUSH,['9', 'T', 'J', 'Q', 'K']

    >>> score(Cards.from_string("TS TH TD TC AH"))
    FOUR_OF_A_KIND,['T', 'T', 'T', 'T', 'A']

    >>> score(Cards.from_string("AH TS TH TD TC"))
    FOUR_OF_A_KIND,['T', 'T', 'T', 'T', 'A']

    ????
    >>> score(Cards.from_string("7C 7H TS TH TD"))
    FULL_HOUSE,['T', 'T', 'T', '7', '7']

    >>> score(Cards.from_string("7C 2C 4C 8C KC"))
    FLUSH,['K', '8', '7', '4', '2']

    >>> score(Cards.from_string("TS TH TD KC AH"))
    THREE_OF_A_KIND,['T', 'T', 'T', 'A', 'K']

    >>> score(Cards.from_string("TS TH 9D 9C AH"))
    TWO_PAIRS,['T', 'T', '9', '9', 'A']

    >>> score(Cards.from_string("9D 9C TS TH AH"))
    TWO_PAIRS,['T', 'T', '9', '9', 'A']

    >>> score(Cards.from_string("TS TH 7D 9C AH"))
    ONE_PAIR,['T', 'T', 'A', '9', '7']

    >>> score(Cards.from_string("QS TH 7D 9C AH"))
    HIGH_CARD,['A', 'Q', 'T', '9', '7']

    """
    hand = Hand(cards)


    matches = [
        match_royal_flush,
        match_straight_flush,
        match_four_of_a_kind,
        match_full_house,
        match_flush,
        match_straight,
        match_three_of_a_kind,
        match_two_pairs,
        match_one_pair,
        match_high_card,
    ]

    for match in matches:
        m = match(hand)
        if m is not None:
            return m

    return match_high_card(hand)


def winner(str: str):
    """
    # >>> winner("5H 5C 6S 7S KD 2C 3S 8S 8D TD")
    # 2

    # >>> winner("5D 8C 9S JS AC 2C 5C 7D 8S QH")
    # 1

    # >>> winner("2D 9C AS AH AC 3D 6D 7D TD QD")
    # 2

    # >>> winner("4D 6S 9H QH QC 3D 6D 7H QD QS")
    # 1

    # >>> winner("4D 6S 9H QH QC 3D 6D 7H QD QS")
    # 1

    # >>> winner("2H 2D 4C 4D 4S 3C 3D 3S 9S 9D")
    # 1

    """
    score1, score2 = score(Cards.from_string(str)[0:5]), score(
        Cards.from_string(str)[5:]
    )
    if score1 == score2:
        return 0
    elif score1 < score2:
        return 2
    else:
        return 1


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    # results = [0, 0, 0]
    # with open("poker.txt", "rt") as f:
    #     for line in f.readlines():

    #         # s = score(Cards.from_string(line)[0:5])
    #         # print(line[0:15].strip(), "-", s)
    #         # s = score(Cards.from_string(line)[5:])
    #         # print(line[15:].strip(), "-", s)
    #         results[winner(line)] += 1
    #     print(results[1])
