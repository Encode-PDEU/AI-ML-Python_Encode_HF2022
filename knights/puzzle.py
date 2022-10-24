from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    # TODO
    
    # A can only be one of Knave or Knight and not both
    And( Or(AKnight, AKnave),
    Not( And(AKnight, AKnave))
    ),

    # If A is Knight, then according to what it says it needs to be both Knave and Knight
    Implication(AKnight, And(AKnight, AKnave))
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    # TODO

    # A can only be one of Knave or Knight and not both
    And( Or(AKnight, AKnave),
    Not( And(AKnight, AKnave))
    ),

    # B can only be one of Knave or Knight and not both
    And( Or(BKnight, BKnave),
    Not( And(BKnight, BKnave))
    ),

    # If A is Knight, i.e. what it says is true, therefore both A and B are Knaves (although this is a contradiction)
    Implication(AKnight, And(AKnave, BKnave)),

    # If A is Knave, i.e. what it says is false, therfore both aren't Knaves and that implies B is Knight
    Implication(AKnave, BKnight)
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    # TODO

    # A can only be one of Knave or Knight and not both
    And( Or(AKnight, AKnave),
    Not( And(AKnight, AKnave))
    ),

    # B can only be one of Knave or Knight and not both
    And( Or(BKnight, BKnave),
    Not( And(BKnight, BKnave))
    ),

    # According to A's statment if A is Knight, B has to be Knight; and if A is Knave, B has to be still Knight
    # Therefore whatever A is, i.e. Knave or Knight, that implies B to be Knight.
    Implication( Or(AKnave, AKnight), BKnight),

    # According to B's statment if B is Knight, A has to be Knave; and if B is Knave, A has to be still Knave
    # Therefore whatever B is, i.e. Knave or Knight, that implies A to be Knave.
    Implication( Or(BKnight, BKnave), AKnave)
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    # TODO

    # A can only be one of Knave or Knight and not both
    And( Or(AKnight, AKnave),
    Not( And(AKnight, AKnave))
    ),

    # B can only be one of Knave or Knight and not both
    And( Or(BKnight, BKnave),
    Not( And(BKnight, BKnave))
    ),

    # C can only be one of Knave or Knight and not both
    And( Or(CKnight, CKnave),
    Not( And(CKnight, CKnave))
    ),

    # If C is Knight, then A will be Knight
    Implication(CKnight, AKnight),

    # If B is Knave, according to what it says about C, C will be Knight
    Implication(BKnave, CKnight),

    # If A is Knight, It will say "I am a knight.", and if A is Knave it will say the same i.e. "I am a knight."
    # As in any case of A, A will never say "I am a knave.", this implies B is Knave
    Implication( Or(AKnight, AKnave), BKnave)
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
