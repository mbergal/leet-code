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


@dataclass(order=True, frozen=True)
class Card:
    value: Value
    suit: Suit

    @staticmethod
    def from_string(str: str):
        return Card(suit=Suit(str[-1]), value=Value(str[0:-1]))

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
    def make(rank: Rank, *, hand: List[Card], matched: Optional[List[Card]] = None):
        if matched is not None:
            assert hand is not None
            return Score(rank, Cards.values(matched + Cards.diff(hand, matched)))
        return Score(rank, Cards.values(hand))





class Cards:
    @staticmethod
    def from_string(str: str) -> List[Card]:
        return [Card.from_string(x.strip()) for x in str.split(" ")]

    @staticmethod
    def values(hand: Union[Sequence[Card], Iterator[Card]]) -> List[Value]:
        return [x.value for x in hand]

    @staticmethod
    def group_by(hand: List[Card], key: Callable[[Card], T]) -> List[Tuple[T, List[Card]]]:
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


def score(hand: List[Card]) -> Score:
    """
    >>> score(Cards.from_string("TH JH QH KH AH"))
    ROYAL_FLUSH,['T', 'J', 'Q', 'K', 'A']

    >>> score(Cards.from_string("9H TH JH QH KH"))
    STRAIGHT_FLUSH,['9', 'T', 'J', 'Q', 'K']

    >>> score(Cards.from_string("TS TH TD TC AH"))
    FOUR_OF_A_KIND,['T', 'T', 'T', 'T', 'A']

    >>> score(Cards.from_string("7C 7H TS TH TD"))
    FULL_HOUSE,['T', 'T', 'T', '7', '7']

    >>> score(Cards.from_string("7C 2C 4C 8C KC"))
    FLUSH,['K', '8', '7', '4', '2']

    >>> score(Cards.from_string("TS TH TD KC AH"))
    THREE_OF_A_KIND,['T', 'T', 'T', 'A', 'K']

    >>> score(Cards.from_string("TS TH 9D 9C AH"))
    TWO_PAIRS,['T', 'T', '9', '9', 'A']

    >>> score(Cards.from_string("TS TH 7D 9C AH"))
    ONE_PAIR,['T', 'T', 'A', '9', '7']

    >>> score(Cards.from_string("QS TH 7D 9C AH"))
    HIGH_CARD,['A', 'Q', 'T', '9', '7']


    """
    hand = list(sorted(hand))
    sorted_by_suit = Cards.group_by(list(sorted(hand)), lambda card: card.suit)
    sorted_by_value = Cards.group_by(list(sorted(hand)), lambda card: card.value)

    def match_royal_flush() -> Optional[Score]:
        if len(sorted_by_suit) == 1 and Cards.values(sorted_by_suit[0][1]) == [
            Value.TEN,
            Value.JACK,
            Value.QUEEN,
            Value.KING,
            Value.ACE,
        ]:
            return Score.make(Rank.ROYAL_FLUSH, hand=hand)

    def match_straight_flush() -> Optional[Score]:
        if len(sorted_by_suit) == 1:
            for _suit, cards in sorted_by_suit:
                if all(
                    [
                        cards[i - 1].value == prev_value(cards[i].value)
                        for i in range(1, len(cards))
                    ]
                ):
                    return Score.make(Rank.STRAIGHT_FLUSH, matched=cards, hand=hand)

    def match_four_of_a_kind() -> Optional[Score]:
        if m := next((x for x in sorted_by_value if len(x[1]) == 4), None):
            return Score.make(Rank.FOUR_OF_A_KIND, matched=m[1], hand=hand)

    def match_full_house() -> Optional[Score]:
        if three := next((x for x in sorted_by_value if len(x[1]) == 3), None):
            if pair := next((x for x in sorted_by_value if len(x[1]) == 2), None):
                return Score.make(Rank.FULL_HOUSE, matched=three[1] + pair[1], hand=hand)
        return None

    def match_flush() -> Optional[Score]:
        if len(sorted_by_suit) == 1:
            return Score.make(Rank.FLUSH, matched=list(reversed(hand)), hand=hand)

    def match_straight() -> Optional[Score]:
        if all(
            [
                hand[i].value == prev_value(hand[i - 1].value)
                for i in range(1, len(hand))
            ]
        ):
            return Score.make(Rank.STRAIGHT, matched=hand, hand=hand)

    def match_three_of_a_kind() -> Optional[Score]:
        if three := next((x for x in sorted_by_value if len(x[1]) == 3), None):
            return Score.make(Rank.THREE_OF_A_KIND, matched=three[1], hand=hand)

    def match_two_pairs() -> Optional[Score]:
        if pair_one := next((x for x in sorted_by_value if len(x[1]) == 2), None):
            if pair_two := next(
                (x for x in sorted_by_value if len(x[1]) == 2 and x != pair_one), None
            ):
                return Score.make(
                    Rank.TWO_PAIRS,
                    matched=list(reversed(sorted(list(pair_one[1] + pair_two[1])))),
                    hand=hand,
                )

        return None

    def match_one_pair() -> Optional[Score]:
        if pair_one := next((x for x in sorted_by_value if len(x[1]) == 2), None):
            return Score.make(Rank.ONE_PAIR, matched=pair_one[1], hand=hand)

    def match_high_card() -> Score:
        return Score.make(Rank.HIGH_CARD, matched=list(reversed(hand)), hand=hand)

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
        m = match()
        if m is not None:
            return m

    return match_high_card()


def winner(str: str):
    """
    >>> winner("5H 5C 6S 7S KD 2C 3S 8S 8D TD")
    2

    >>> winner("5D 8C 9S JS AC 2C 5C 7D 8S QH")
    1

    >>> winner("2D 9C AS AH AC 3D 6D 7D TD QD")
    2

    >>> winner("4D 6S 9H QH QC 3D 6D 7H QD QS")
    1

    >>> winner("4D 6S 9H QH QC 3D 6D 7H QD QS")
    1

    >>> winner("2H 2D 4C 4D 4S 3C 3D 3S 9S 9D")
    1

    """
    score1, score2 = score(Cards.from_string(str)[0:5]), score(Cards.from_string(str)[5:])
    if score1 == score2:
        return 0
    elif score1 < score2:
        return 2
    else:
        return 1


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    results = [0,0,0]
    with open("poker.txt", "rt") as f:
        for line in f.readlines():
            
            # s = score(Cards.from_string(line)[0:5])
            # print(line[0:15].strip(), "-", s)
            # s = score(Cards.from_string(line)[5:])
            # print(line[15:].strip(), "-", s)
            results[winner(line)] += 1
        print(results[1])
