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


class Category(OrderedEnum):
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
        super().__init__(f'Invalid card "{invalid_card}"')
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
        if len(str) != 2:
            raise InvalidCard(str)
        suit_str = str[1]
        if suit_str not in Suit:
            raise InvalidCard(str)
        value_str = str[0]
        if value_str not in Value:
            raise InvalidCard(str)

        return Card(suit=Suit(suit_str), value=Value(value_str))

    def __repr__(self) -> str:
        suit_str = self.suit.value
        value_str = self.value.value
        return f"{value_str}{suit_str}"


@dataclass(order=True, frozen=True)
class Score:
    """
    >>> score(Hand.from_string("AH KH QH JH TH")) == score(Hand.from_string("AS KS QS JS TS"))
    True
    >>> score(Hand.from_string("KH QH JH TH 9H")) == score(Hand.from_string("KS QS JS TS 9S"))
    True
    >>> score(Hand.from_string("KH QH JH TH 9H")) > score(Hand.from_string("QS JS TS 9S 8S"))
    True

    # >>> Score(Category.STRAIGHT_FLUSH, Cards.from_string("QH JH TH 9H 8H")) < Score(Category.ROYAL_FLUSH, [])
    # True
    # >>> Score(Category.STRAIGHT_FLUSH, Cards.from_string("QH JH TH 9H 8H")) < Score(Category.STRAIGHT_FLUSH, Cards.from_string("JH TH 9H 8H 7H"))
    # False
    # >>> Score(Category.STRAIGHT_FLUSH, []) < Score(Category.ROYAL_FLUSH, [])
    # True
    # >>> Score(Category.ONE_PAIR, []) < Score(Category.TWO_PAIRS, [])
    # True
    # >>> Score(Category.ONE_PAIR, []) > Score(Category.TWO_PAIRS, [])
    # False
    # >>> Score(Category.ONE_PAIR, []) == Score(Category.ONE_PAIR, [])
    # True
    """

    category: Category
    highest_cards: List[Value]

        




    
    
    def __repr__(self) -> str:
        return f"{self.category.value},{[x.value for x in self.highest_cards]}"


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
        return (
            [Card.from_string(x.strip()) for x in str.split(" ")]
            if str.strip() != ""
            else []
        )

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
    """
    >>> Hand.from_string("")
    []

    >>> Hand.from_string("3C 3S 3D 6C 6H")
    [3C, 3D, 3S, 6C, 6H]
    """

    class Has:
        def __init__(self, hand: "Hand", num: int) -> None:
            self.hand = hand
            self.num = num

        def cards_of_same_value(self) -> Optional[Tuple[Value, List[Card]]]:
            return next(
                (x for x in self.hand.sorted_by_value if len(x[1]) == self.num), None
            )

    def __init__(self, cards: List[Card]):
        self.cards = list(sorted(cards))

        self.sorted_by_suit = Cards.group_by(
            list(sorted(self.cards)), lambda card: card.suit
        )
        self.sorted_by_value = Cards.group_by(
            list(sorted(self.cards)), lambda card: card.value
        )

    def __repr__(self) -> str:
        return str(self.cards)

    @property
    def values(self):
        return sorted(Cards.values(self.cards))

    @property
    def is_single_suit(self) -> bool:
        return len(self.sorted_by_suit) == 1

    def has(self, num: int) -> "Hand.Has":
        return Hand.Has(self, num)

    @property
    def are_consequitive(self) -> bool:
        return all(
            [
                self.cards[i - 1].value == prev_value(self.cards[i].value)
                for i in range(1, len(self.cards))
            ]
        )

    @property
    def highest_card(self) -> Card:
        return self.sorted_by_value[0][1][0]

    @staticmethod
    def from_string(str: str):
        return Hand(Cards.from_string(str))

    def score(self, rank: Category, rank_cards: Optional[Sequence[Card]] = None):
        if rank_cards is not None:
            return Score(rank, Cards.values(list(rank_cards) + Cards.diff(self.cards, list(rank_cards))))
        return Score(rank, [])

class Rank:
    def __init__(self, rank_cards: List[Card], hand: Hand) -> None:
        self.hand = hand
        self.rank_cards = rank_cards

        
def score_from_rank(rank:Rank):
    if isinstance(rank, RoyalFlush):
        return rank.hand.score(Category.ROYAL_FLUSH)
    elif isinstance(rank, StraightFlush):
        return rank.hand.score(Category.STRAIGHT_FLUSH, rank_cards=[rank.rank])
    elif isinstance(rank, FourOfAKind):
        return rank.hand.score(Category.FOUR_OF_A_KIND, rank.rank_cards)
    elif isinstance(rank, FullHouse):
        return rank.hand.score(Category.FULL_HOUSE, rank.three + rank.pair)
    elif isinstance(rank, Flush):
        return rank.hand.score(Category.FLUSH, list(reversed(rank.hand.cards)))
    elif isinstance(rank, Straight):
        return rank.hand.score(Category.STRAIGHT, rank.hand.cards)
    elif isinstance(rank, ThreeOfAKind):
        return rank.hand.score(Category.THREE_OF_A_KIND, rank.three)
    elif isinstance(rank, TwoPairs):
        return rank.hand.score(
                    Category.TWO_PAIRS,
                    list(reversed(sorted(list(rank.pair_one + rank.pair_two)))),
                )
    elif isinstance(rank, OnePair):
        return rank.hand.score(Category.ONE_PAIR, rank.pair)
    elif isinstance(rank, HighCard):
        return rank.hand.score(Category.HIGH_CARD, list(reversed(sorted(rank.highest_cards))))
    else:
        raise Exception(f"Unknown rank {rank}")
        

@dataclass
class RoyalFlush(Rank):
    @staticmethod
    def match(hand: Hand) -> Optional["RoyalFlush"]:
        """
        >>> RoyalFlush.match(Hand.from_string("TH JH QH KH AH"))
        RoyalFlush()

        >>> RoyalFlush.match(Hand(Cards.from_string("AH TH JH QH KH")))
        RoyalFlush()

        >>> RoyalFlush.match(Hand(Cards.from_string("9H JH QH KH AH")))
        """
        if hand.is_single_suit and hand.values == [
            Value.TEN,
            Value.JACK,
            Value.QUEEN,
            Value.KING,
            Value.ACE,
        ]:
            return RoyalFlush(hand)
        
    def __init__(self, hand: Hand) -> None:
        super().__init__([], hand)


@dataclass
class StraightFlush(Rank):
    rank: Card

    @staticmethod
    def match(hand: Hand) -> Optional["StraightFlush"]:
        """
        >>> StraightFlush.match(Hand(Cards.from_string("QH JH TH 9H 8H")))
        StraightFlush(rank=8H)

        >>> StraightFlush.match(Hand(Cards.from_string("QH JH TH 9H 7H")))
        """
        if hand.is_single_suit and hand.are_consequitive:
            return StraightFlush(rank=hand.highest_card, rank_cards = hand.cards, hand=hand)
    
    def __init__(self, rank: Card, rank_cards: List[Card], hand: Hand) -> None:
        super().__init__(rank_cards, hand)
        self.rank = rank
    
@dataclass
class FourOfAKind(Rank):
    four: List[Card]
    
    @staticmethod
    def match(hand: Hand) -> Optional["FourOfAKind"]:
        """
        >>> match_four_of_a_kind(Hand(Cards.from_string("9C 9S 9D 9H JH")))
        FOUR_OF_A_KIND,['9', '9', '9', '9', 'J']

        >>> match_four_of_a_kind(Hand(Cards.from_string("9C 9S 9D 7H JH")))
        """
        if four := hand.has(4).cards_of_same_value():
            return FourOfAKind(hand, four=four[1])
        
    def __init__(self, hand: Hand, *, four: List[Card]) -> None:
        super().__init__(four, hand)
        self.four = four


@dataclass        
class FullHouse(Rank):
    three: List[Card]
    pair: List[Card]

    @staticmethod
    def match(hand: Hand) -> Optional["FullHouse"]:
        """
        >>> match_full_house(Hand.from_string("3C 3S 3D 6C 6H"))
        FULL_HOUSE,['3', '3', '3', '6', '6']

        >>> match_full_house(Hand.from_string("6C 6H 3C 3S 3D"))
        FULL_HOUSE,['3', '3', '3', '6', '6']

        >>> match_full_house(Hand.from_string("6C 6H 3C 3S 5D"))
        """
        if three := hand.has(3).cards_of_same_value():
            if pair := hand.has(2).cards_of_same_value():
                return FullHouse(three[1], pair[1], hand)
        return None
    
    def __init__(self, three: List[Card], pair: List[Card], hand: Hand) -> None:
        super().__init__(three + pair, hand)
        self.three = three
        self.pair = pair


@dataclass
class Flush(Rank):    
    flush: List[Card]

    @staticmethod
    def match(hand: Hand) -> Optional["Flush"]:
        """
        >>> match_flush(Hand.from_string("KC TC 7C 6C 4C"))
        FLUSH,['K', 'T', '7', '6', '4']
        """
        if hand.is_single_suit:
            return Flush(list(reversed(hand.cards)), hand)
        
    def __init__(self, rank_cards: List[Card], hand: Hand) -> None:
        super().__init__(rank_cards, hand)
        self.flush = rank_cards

@dataclass
class Straight(Rank):
    rank_cards: List[Card]
    @staticmethod
    def match(hand: Hand) -> Optional["Straight"]:
        """
        >>> Straight.match(Hand.from_string("7C 6S 5S 4H 3H"))
        Straight(rank_cards=[3H, 4H, 5S, 6S, 7C])
        
        >>> Straight.match(Hand.from_string("7C 6S 5S 4H 2H"))
        """
        if hand.are_consequitive:
            return Straight(hand.cards, hand)

    def __init__(self, rank_cards: List[Card], hand: Hand) -> None:
        super().__init__(rank_cards, hand)
        self.rank_cards = sorted(rank_cards)
    

@dataclass
class ThreeOfAKind(Rank):
    three: List[Card]
     
    @staticmethod
    def match(hand: Hand) -> Optional["ThreeOfAKind"]:
        """
        >>> ThreeOfAKind.match(Hand.from_string("2D 2H 2C KS 6H"))
        ThreeOfAKind(three=[2C, 2D, 2H])

        >>> ThreeOfAKind.match(Hand.from_string("3D 2H 2C KS 6H"))
        """

        if three := hand.has(3).cards_of_same_value():
            return ThreeOfAKind(three[1], hand)
        
    def __init__(self, three: List[Card], hand: Hand) -> None:
        super().__init__(three, hand)
        self.three = three

@dataclass
class TwoPairs(Rank):
    pair_one: List[Card]
    pair_two: List[Card]

    @staticmethod
    def match(hand: Hand) -> Optional["TwoPairs"]:
        """
        >>> TwoPairs.match(Hand.from_string("TD TH 2S 2C KC"))
        TwoPairs(pair_one=[2C, 2S], pair_two=[TD, TH])

        """
        """
        >>> match_two_pairs(Hand.from_string("2S 2C TD TH KC"))
        TWO_PAIRS,['T', 'T', '2', '2', 'K']
        >>> match_two_pairs(Hand.from_string("3S 2C TD TH KC"))
        """
        if pair_one := hand.has(2).cards_of_same_value():
            if (
                pair_two := Hand(Cards.diff(hand.cards, pair_one[1]))
                .has(2)
                .cards_of_same_value()
            ):
                return TwoPairs(pair_one[1], pair_two[1], hand)

    def __init__(self, pair_one: List[Card], pair_two: List[Card], hand: Hand) -> None:
        super().__init__(pair_one + pair_two, hand)
        self.pair_one = pair_one
        self.pair_two = pair_two
    

@dataclass
class OnePair(Rank):
    pair: List[Card]

    @staticmethod
    def match(hand: Hand) -> Optional["OnePair"]:
        """
        >>> match_one_pair(Hand.from_string("9C 9D QS JH 5H"))
        ONE_PAIR,['9', '9', 'Q', 'J', '5']

        # >>> match_one_pair ranks higher than 6♦ 6♥ K♠ 7♥ 4♣,
        """
        if pair_one := hand.has(2).cards_of_same_value():
            return OnePair(pair=pair_one[1], hand=hand)
        
    def __init__(self, pair: List[Card], hand: Hand) -> None:
        super().__init__(pair, hand)
        self.pair = pair


@dataclass  
class HighCard(Rank):
    highest_cards: List[Card]

    @staticmethod
    def match(hand: Hand) -> "HighCard":
        """
        >>> match_high_card(Hand.from_string("KH JH 8C 7D 4S"))
        HIGH_CARD,['K', 'J', '8', '7', '4']
        """
        return HighCard(highest_cards=list(reversed(sorted(hand.cards))), hand=hand)
    
    def __init__(self, highest_cards: List[Card], hand: Hand) -> None:
        super().__init__(highest_cards, hand)
        self.highest_cards = highest_cards
    


def rank(hand: Hand) -> Rank:
    """
    >>> rank(Hand.from_string("TH JH QH KH AH"))
    RoyalFlush()

    >>> rank(Hand.from_string("AH TH JH QH KH"))
    RoyalFlush()

    >>> rank(Hand.from_string("9H TH JH QH KH"))
    StraightFlush(rank=9H)

    >>> rank(Hand.from_string("TH JH QH KH 9H"))
    StraightFlush(rank=9H)

    >>> rank(Hand.from_string("TS TH TD TC AH"))
    FourOfAKind(four=[TC, TD, TS, TH])

    >>> rank(Hand.from_string("AH TS TH TD TC"))
    FourOfAKind(four=[TC, TD, TS, TH])

    >>> rank(Hand.from_string("7C 7H TS TH TD"))
    FullHouse(three=[TD, TS, TH], pair=[7C, 7H])

    >>> rank(Hand.from_string("7C 2C 4C 8C KC"))
    Flush(flush=[KC, 8C, 7C, 4C, 2C])

    >>> rank(Hand.from_string("TS TH TD KC AH"))
    ThreeOfAKind(three=[TD, TS, TH])

    >>> rank(Hand.from_string("TS TH 9D 9C AH"))
    TwoPairs(pair_one=[9C, 9D], pair_two=[TS, TH])

    >>> rank(Hand.from_string("9D 9C TS TH AH"))
    TwoPairs(pair_one=[9C, 9D], pair_two=[TS, TH])

    >>> rank(Hand.from_string("TS TH 7D 9C AH"))
    OnePair(pair=[TS, TH])

    >>> rank(Hand.from_string("QS TH 7D 9C AH"))
    HighCard(highest_cards=[AH, QS, TH, 9C, 7D])

    """

    matches: List[Callable[[Hand],Optional[Rank]]] = [
        RoyalFlush.match,
        StraightFlush.match,
        FourOfAKind.match,
        FullHouse.match,
        Flush.match,
        Straight.match,
        ThreeOfAKind.match,
        TwoPairs.match,
        OnePair.match,
        HighCard.match
    ]

    m = None
    for match in matches:
        m = match(hand)
        if m is not None:
            break
    m = m or HighCard.match(hand)
    return m


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
    score1, score2 = rank(Hand(Cards.from_string(str)[0:5])), rank(
        Hand(Cards.from_string(str)[5:])
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
    results = [0, 0, 0]
    with open("poker.txt", "rt") as f:
        for line in f.readlines():

            # s = score(Cards.from_string(line)[0:5])
            # print(line[0:15].strip(), "-", s)
            # s = score(Cards.from_string(line)[5:])
            # print(line[15:].strip(), "-", s)
            results[winner(line)] += 1
        print(results[1])
