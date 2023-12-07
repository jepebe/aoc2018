import typing
from collections import Counter

import aoc

tester = aoc.Tester("Camel Cards")

hand_order = ["five of a kind", "four of a kind", "full house", "three of a kind", "two pair",
              "one pair", "high card"]
card_order = "AKQJT98765432"
joker_card_order = "AKQT98765432J"


class Hand:
    def __init__(self, cards: str):
        self._cards = cards
        self._type = None
        self._joker_mode = False

    def type(self) -> str:
        if self._type is not None:
            return self._type

        hand_type = self._identify_type(self._cards)

        self._type = hand_type
        return hand_type

    @staticmethod
    def _identify_type(cards: str) -> str:
        num_distinct_cards = len(set(cards))
        card_counts = Counter(cards)
        if num_distinct_cards == 1:
            hand_type = "five of a kind"
        elif num_distinct_cards == 2:
            if 4 in card_counts.values():
                hand_type = "four of a kind"
            else:
                hand_type = "full house"
        elif num_distinct_cards == 3:
            if 3 in card_counts.values():
                hand_type = "three of a kind"
            else:
                hand_type = "two pair"
        elif num_distinct_cards == 4:
            hand_type = "one pair"
        elif num_distinct_cards == 5:
            hand_type = "high card"
        else:
            raise ValueError(f"Unexpected number of distinct cards: {num_distinct_cards}")
        return hand_type

    def __repr__(self):
        return f"Hand({self._cards})"

    def __str__(self):
        return str(self._cards)

    def __lt__(self, other: typing.Self) -> bool:
        if self.type() != other.type():
            return hand_order.index(self.type()) > hand_order.index(other.type())
        else:
            indexer = card_order if not self._joker_mode else joker_card_order
            for c1, c2 in zip(self._cards, other._cards):
                if c1 != c2:
                    return indexer.index(c1) > indexer.index(c2)
            return False

    def __eq__(self, other: typing.Self) -> bool:
        if isinstance(other, str):
            return self._cards == other
        return self._cards == other._cards

    def __hash__(self) -> int:
        return hash(self._cards)

    def set_joker_mode(self):
        if "J" in self._cards:
            best_hand_type = self.type()
            # best_replacement = "J"
            for card in card_order:
                if card == "J":
                    continue
                cards = self._cards.replace("J", card)
                hand_type = self._identify_type(cards)
                if hand_order.index(hand_type) < hand_order.index(best_hand_type):
                    best_hand_type = hand_type
                    # best_replacement = card
            # print(f"Joker hand: {self._cards} {best_hand_type} {best_replacement}")
            self._type = best_hand_type
        self._joker_mode = True


def parse(data: str) -> dict[Hand, int]:
    hands_bids = {}
    for line in data.splitlines():
        cards, bid = line.split(" ")
        hand = Hand(cards)
        if hand in hands_bids:
            raise ValueError(f"Duplicate hand: {hand}")
        hands_bids[hand] = int(bid)

    return hands_bids


def score_hands(hands: dict[Hand, int], joker_mode: bool = False) -> int:
    total_winnings = 0
    if joker_mode:
        for hand in hands:
            hand.set_joker_mode()
    for index, hand in enumerate(sorted(hands.keys()), start=1):
        bid = hands[hand]
        total_winnings += bid * index
    return total_winnings


def run_tests(t: aoc.Tester):
    t.test_section("Tests")

    data = aoc.read_input("input_test")
    hands = parse(data)

    t.test_value(Hand("AAAAA").type(), "five of a kind")
    t.test_value(Hand("77737").type(), "four of a kind")
    t.test_value(Hand("3TTT3").type(), "full house")
    t.test_value(Hand("74737").type(), "three of a kind")
    t.test_value(Hand("74437").type(), "two pair")
    t.test_value(Hand("97647").type(), "one pair")
    t.test_value(Hand("AKQJT").type(), "high card")

    sorted_hands = list(sorted(hands.keys()))
    t.test_value(sorted_hands, ["32T3K", "KTJJT", "KK677", "T55J5", "QQQJA"])

    total_winnings = score_hands(hands)
    t.test_value(total_winnings, 6440)

    total_winnings = score_hands(hands, joker_mode=True)
    sorted_hands = list(sorted(hands.keys()))
    t.test_value(sorted_hands, ["32T3K", "KK677", "T55J5", "QQQJA", "KTJJT"])
    t.test_greater_than(Hand("22222"), Hand("22J22"))
    t.test_value(total_winnings, 5905)


run_tests(tester)

data = aoc.read_input()
hands = parse(data)

tester.test_section("Part 1")
solution_1 = score_hands(hands)
tester.test_solution(solution_1, 251927063)

tester.test_section("Part 2")
solution_2 = score_hands(hands, joker_mode=True)
tester.test_less_than(solution_2, 255783389)
tester.test_solution(solution_2, 255632664)
