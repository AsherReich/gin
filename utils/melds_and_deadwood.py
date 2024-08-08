from collections import defaultdict
import itertools
import logging
from models.card import Card  # Adjust the import path as necessary
import time

class MeldNode:
    def __init__(self, cards, parent=None):
        self.cards = cards
        self.parent = parent
        self.value = sum(card.value for card in cards)
        if parent:
            self.value += parent.value

def clean_meld_group(melds, meld_avoid):
    clean_melds = []
    for meld in melds:
        if not any(card in meld_avoid for card in meld):
            clean_melds.append(meld)
    #logging.debug(f"clean_meld_group: Avoiding {meld_avoid}, result: {clean_melds}")
    return clean_melds

def get_best_node(melds, root_node, depth=0, max_depth=[0]):
    if depth > 1000:  # Prevent infinite recursion
        logging.error("Max recursion depth reached in get_best_node")
        return root_node

    # Update max depth
    if depth > max_depth[0]:
        max_depth[0] = depth

    best = root_node
    for i, meld in enumerate(melds):
        remaining_melds = melds[i+1:]  # Exclude already considered melds
        node = MeldNode(meld, root_node)
        new_tree = get_best_node(clean_meld_group(remaining_melds, meld), node, depth + 1, max_depth)
        
        # This comparison inherently considers the option of not including the current meld
        if best is None or new_tree.value > best.value:
            best = new_tree
        elif new_tree.value == best.value:
            best = tie_breaker(best, new_tree)
    return best

def tie_breaker(node1, node2):
    # Prefer runs over sets
    if is_run(node1.cards) and not is_run(node2.cards):
        return node1
    if is_run(node2.cards) and not is_run(node1.cards):
        return node2

    # Compare the minimum rank values
    if node1.cards[0].rank_value < node2.cards[0].rank_value:
        return node1
    if node2.cards[0].rank_value < node1.cards[0].rank_value:
        return node2

    # For runs, compare by the minimum suit values
    if is_run(node1.cards):
        for card1, card2 in zip(node1.cards, node2.cards):
            if Card.suits[card1.suit] < Card.suits[card2.suit]:
                return node1
            if Card.suits[card1.suit] > Card.suits[card2.suit]:
                return node2
        return node1  # If all suits are equal, return node1 by default

    # For sets, compare by the minimum suit values
    for card1, card2 in zip(sorted(node1.cards, key=lambda c: c.suit), sorted(node2.cards, key=lambda c: c.suit)):
        if Card.suits[card1.suit] < Card.suits[card2.suit]:
            return node1
        if Card.suits[card1.suit] > Card.suits[card2.suit]:
            return node2

    return node1  # If all criteria are equal, return node1 by default

def is_run(cards):
    return len(set(card.rank for card in cards)) != 1

def get_optimal_melding(hand):
    possible_melds = []

    # Find all possible runs
    sorted_hand = sorted(hand, key=lambda card: (card.suit, card.rank_value))
    run_length = 1
    for i in range(1, len(sorted_hand)):
        if sorted_hand[i].suit == sorted_hand[i - 1].suit and sorted_hand[i].rank == sorted_hand[i - 1].rank + 1:
            run_length += 1
        else:
            if run_length >= 3:
                for size in range(3, run_length + 1):
                    for start in range(run_length - size + 1):
                        run = sorted_hand[i - run_length + start:i - run_length + start + size]
                        possible_melds.append(run)
            run_length = 1
    if run_length >= 3:
        for size in range(3, run_length + 1):
            for start in range(run_length - size + 1):
                run = sorted_hand[-run_length + start:-run_length + start + size]
                possible_melds.append(run)

    # Find all possible sets
    ranks = defaultdict(list)
    for card in hand:
        ranks[card.rank].append(card)
    for rank, cards in ranks.items():
        if len(cards) >= 3:
            possible_melds.append(cards)
            if len(cards) == 4:
                for combination in itertools.combinations(cards, 3):
                    possible_melds.append(list(combination))

    # Track the maximum recursion depth
    max_depth = [0]

    # Find Optimal Melding Combination
    best_node = get_best_node(possible_melds, None, max_depth=max_depth)

    optimal_melds = []
    while best_node:
        if best_node.cards:  # Ensure no empty melds
            optimal_melds.append(best_node.cards)
        best_node = best_node.parent

    logging.debug(f"[Melds and Deadwood] Maximum recursion depth: {max_depth[0]}")

    return optimal_melds

def get_deadwood(hand, optimal_melds):
    meld_cards = set(card for meld in optimal_melds for card in meld)
    return [card for card in hand if card not in meld_cards]

def meld_sort_key(meld):
    lowest_rank = min(card.rank for card in meld)
    is_set = not is_run(meld)
    suits = sorted(Card.suits[card.suit] for card in meld)
    return (lowest_rank, is_set, suits)

def calculate_optimal_melds_and_deadwood(hand):
    start_time = time.time()
    
    optimal_melds = get_optimal_melding(hand)
    deadwood = get_deadwood(hand, optimal_melds)
    
    # Sort deadwood by rank then by suit
    deadwood.sort(key=lambda card: (card.rank, card.suit))
    
    # Sort optimal melds and ensure cards within melds are sorted
    optimal_melds.sort(key=meld_sort_key)
    for meld in optimal_melds:
        meld.sort(key=lambda card: (card.rank, card.suit))
    
    end_time = time.time()
    execution_time = end_time - start_time
    #logging.debug(f"Execution time for calculate_optimal_melds_and_deadwood: {execution_time:.4f} seconds")
    
    #logging.debug(f"Sorted optimal melds: {optimal_melds}")
    #logging.debug(f"Sorted deadwood: {deadwood}")
    
    return optimal_melds, deadwood