import itertools
import random
import copy

class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """

        # if the count of mines is equal to number of neighbouring cells
        if len(self.cells) == self.count:
            return self.cells

        # raise NotImplementedError

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """

        # if the count is 0, i.e. there are no mines
        if self.count == 0:
            return self.cells

        # raise NotImplementedError

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """

        # if we know that a cell is mine then removinig it from the set and decreasing count by 1
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

        # raise NotImplementedError

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """

        # if we know that a cell is safe, just removing it from the set
        if cell in self.cells:
            self.cells.remove(cell)
        
        # raise NotImplementedError


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        to mark that cell as a mine as well.
        Marks a cell as a mine, and updates all knowledge
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """

        # 1. marking the cell as a move that has been made
        self.moves_made.add(cell)

        # the x and y coordinates of the cell
        i = cell[0]
        j = cell[1]

        neighbors = list()

        # iterating over the neighbors 
        for row in range(i - 1, i + 2):
            for col in range(j - 1, j + 2):
                
                if (row, col) == cell:
                    continue

                if row > self.height - 1 or row < 0 or col > self.width - 1 or col < 0:
                    continue
                else:
                    if (row, col) not in self.moves_made:
                        neighbors.append((row, col))
        
        # 3. adding a new sentance to the knowlege base
        self.knowledge.append(Sentence(neighbors, count))

        # 2. marking the cell as safe
        self.mark_safe(cell)

        base = copy.deepcopy(self.knowledge)

        # 4. 
        for sentence in self.knowledge:
            # adding a cell to mines based on the knowlege
            if len(sentence.cells) == sentence.count:
                cells = copy.deepcopy(sentence.cells)
                for cell in cells:
                    self.mark_mine(cell)
                del sentence
            # adding a cell to safes based on the knowledge
            else:
                if sentence.count == 0:
                    cells = copy.deepcopy(sentence.cells)
                    for cell in cells:
                        self.mark_safe(cell)
                    del sentence

        # 5. adding new sentences to knowledege base inferred from the existing ones
        for sentence in base:
            if sentence.count == 0:
                continue

            # cells and counts of sentence 1
            cells1 = sentence.cells
            count1 = sentence.count
            
            for sentence2 in base:
                # cells and counts of sentence 2
                cells2 = sentence2.cells
                count2 = sentence2.count

                if sentence == sentence2 or sentence2.count == 0:
                    continue
                
                # if cells in sentence 2 is subest of cells in sentence 1
                elif cells2.issubset(cells1):
                    new_count = count1 - count2
                    new_cells = list(copy.deepcopy(cells1))
                    
                    # removing cells of sentence 2 from new cells list
                    for cell in cells2:
                        new_cells.remove(cell)

                    # removing the made moves from the new cells list
                    for cell in self.moves_made:
                        if cell in new_cells:
                            new_cells.remove(cell)

                    for sentence in base:
                        if set(new_cells).issubset(sentence.cells):
                            continue
                    
                    # adding new sentence to the knowledege base
                    self.knowledge.append(Sentence(new_cells, new_count))
                
                else:
                    continue
        
        # raise NotImplementedError

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """

        # printing number of unused safe cells and detected mines
        print(f"{len(self.safes - self.moves_made)} known unused safes.")
        print(f"{len(self.mines)} detected mines:\n{list(self.mines)}")

        # if safe cells exists
        if len(self.safes) != 0:
            for cell in self.safes:
                # the cell that is not mine and moved earlier is returned 
                if (cell not in self.moves_made) and (cell not in self.mines):
                    return cell
        else:
            return None
        
        # raise NotImplementedError

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        
        # moves is the list of available moves
        moves = []
        for i in range(0, self.height):
            for j in range(0, self.width):
                if (i, j) not in self.moves_made:
                    if (i, j) not in self.mines:
                        # return (i, j)
                        moves.append((i, j))

        # if no moves are remaining then game is over
        if len(moves) == 0:
            print("GAME FINISHED!")

        # else choosing a random move from the list
        else:
            random_move = random.choice(moves)
            self.moves_made.add(random_move)
            print(f"Move made {random_move}")
            return random_move

        # raise NotImplementedError
