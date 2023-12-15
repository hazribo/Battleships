import random as rdm
import json

# Creates 10x10 board (all None values)
def initialise_board(size: int=10):
    board = [[None]*size for _ in range(0, size)]
    return board

# Creates list of ships from battleships.txt
def create_battleships(filename: str="battleships.txt"):
    battleships = {}
    f = open(filename, "r").readlines
    for line in f():
        line = line.split(",")
        battleships[line[0]] = int(line[1])
    return battleships

# Places battleships on board
# Optional: type; either simple, random, or custom - determines placement of ships.
def place_battleships(board: list, ships: dict, type: str="simple"):
    # Initialise Constant: Ship length for Custom/Flask placement:
    SHIP_LENGTHS = [5, 4, 3, 3, 2] 

    # Simple ship placement - each ship at front of first 5 lines.
    if type == "simple":
        count = 0
        for i, j in ships.items():
            for k in range (0, int(j)):
                board[count][k] = i
            count+=1
    
    # Random ship placement - still only horizontal.
    elif type == "random":
        for ship_type, ship_length in ships.items():
            done = False
            while not done:
                x, y = rdm.randint(0, 9), rdm.randint(0, 9)
                direction = rdm.choice(["h", "v"])

                # Make sure position is within board size:
                if direction == "h" and y + ship_length <= 10:
                    # Ensure that no ships are already present in this location:
                    invalid = any(board[x][y] is not None for y in range(y, y + ship_length))
                    if not invalid:
                        for y in range(y, y + ship_length):
                            board[x][y] = ship_type
                        done = True
                
                # Make sure position is within board size:
                elif direction == "v" and x + ship_length <= 10:
                    # Ensure that no ships are already present in this location:
                    invalid = any(board[x][y] is not None for x in range(x, x + ship_length))
                    if not invalid:
                        for x in range(x, x + ship_length):
                            board[x][y] = ship_type
                        done = True

    # Custom ship placement - read from placement.json file.
    elif type == "custom":
        with open("placement.json", 'r') as f:
            ships = json.load(f)
        
        i = 0
        # zip combines the ship data and ship lengths so can be iterated together:
        for (ship_name, (start_x, start_y, orientation)), length in zip(ships.items(), SHIP_LENGTHS):
            start_x, start_y = int(start_x), int(start_y)

            for i in range(0, length):
                if orientation == "h":
                    board[start_y][start_x + i] = ship_name
                elif orientation == "v":
                    board[start_y + i][start_x] = ship_name
                i+=1

    # Flask ship placement - same as custom, but for use with main.py
    elif type == "flask":
        ## No validity checks needed - this is done via the template.
        # Initialise variables:
        i = 0

        # zip combines the ship data and ship lengths so can be iterated together:
        for (ship_name, (start_x, start_y, orientation)), length in zip(ships.items(), SHIP_LENGTHS):
            start_x, start_y = int(start_x), int(start_y)

            for i in range(0, length):
                if orientation == "h":
                    board[start_y][start_x + i] = ship_name
                elif orientation == "v":
                    board[start_y + i][start_x] = ship_name
                i+=1
    return board

# Allows manual testing of simple_game_loop
if __name__ == "__main__":
    from game_engine import simple_game_loop
    simple_game_loop()
