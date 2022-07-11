from random import choice, seed, shuffle
from typing import Generator

def generate_new_bag():
    'Generates a 14-long sequence of two bags'
    output_list = []
    for _ in range(2):
        piece_list = list("IJLOSZT")
        for _ in range(7):
            # If there is only one piece left, output it and break
            if len(piece_list) == 1:
                output_list.append(piece_list[0])
                break
            a = choice(piece_list)
            # Add a random piece to the output list
            output_list.append(a)
            # Remove that piece from the current bag
            piece_list.remove(a)
    return "".join(output_list)

def produce_bag_generator(generator_seed: str = "") -> Generator[str, None, None]:
    # sourcery skip: simplify-empty-collection-comparison
    'Creates a generator for bags, which will return seeded bags\nIf generator seed is kept as default (empty str), it will produce random, unseeded bags'
    if generator_seed == "":
        yield generate_new_bag()
    else:
        seed(generator_seed)
    while True:
        pieces = list("IJLOSZT")
        shuffle(pieces)
        yield "".join(pieces)

class Bag():
    def __init__(self, seed=""):
        self.gen = produce_bag_generator(seed)
        initial_bag = next(self.gen) + next(self.gen) + next(self.gen)
        self.value = initial_bag

    def update(self):
        piece = self.value[0]
        if len(self.value) <= 14:
            self.value = self.value[1:] + next(self.gen)
        else:
            self.value = self.value[1:]
        return piece