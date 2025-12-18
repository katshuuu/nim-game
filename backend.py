# backend.py
import random
from typing import List, Tuple, Optional

def calculate_nim_sum(piles: List[int]) -> int:
    nim_sum = 0
    for pile in piles:
        nim_sum ^= pile
    return nim_sum

def find_winning_move(piles: List[int]) -> Optional[Tuple[int, int]]:
    nim_sum = calculate_nim_sum(piles)
    if nim_sum == 0:
        return None

    for i, pile in enumerate(piles):
        target = pile ^ nim_sum
        if target < pile:
            return i, pile - target
    return None

def computer_move(piles: List[int]) -> Tuple[List[int], str]:
    move = find_winning_move(piles)

    if move:
        i, take = move
        message = f"🤖 Компьютер берет {take} камней из кучки {i + 1}"
    else:
        non_empty = [i for i, p in enumerate(piles) if p > 0]
        i = random.choice(non_empty)
        take = random.randint(1, piles[i])
        message = f"🤖 Компьютер делает случайный ход: берет {take} камней из кучки {i + 1}"

    piles[i] -= take
    return piles, message

def is_game_over(piles: List[int]) -> bool:
    return all(p == 0 for p in piles)

def initialize_game(mode: str, num_piles: int = 3) -> List[int]:
    if mode == "random":
        return [random.randint(1, 8) for _ in range(num_piles)]
    return [3, 4, 5]
