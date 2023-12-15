from components import initialise_board, create_battleships, place_battleships

# Checks if ship is at given coords, replace with None & decrements size
def attack(coords: tuple, board: list, ships: dict):
    loc = list(coords)
    print(loc)
    ship = board[loc[1]][loc[0]]
    if ship != None:
        hit = True
        ships[ship] -= 1
        board[loc[1]][loc[0]] = None
        print(board)

        if ships[ship] == 0:
            sunk = True
        else:
            sunk = False
    else:
        hit = False
        sunk = False
    return hit, sunk

# Command-Line Input (CLI) for attack coordinates
def cli_coordinates_input():
    coords = input("Enter coords: ")
    # below returns a tuple of the individual co-ords, 
    # allowing "(x, y)"" or "x, y" as an input:
    return tuple(map(int, coords.strip("()").split(",")))

# Runs single player game loop
def simple_game_loop():
    ## CHANGE GAME TYPE BELOW:
    # Options: simple, random, custom.
    MODE = "simple" 

    print("Welcome to Battleships!")
    board = initialise_board()
    ships = create_battleships()
    place_battleships(board, ships, MODE)
    for line in board:
        print(line)
    # below loops until every value in board = None
    while any(val is not None for row in board for val in row): 
        coords = cli_coordinates_input()
        hit, sunk = attack(coords, board, ships)
        if hit == True:
            print("Hit!")
        if sunk == True:
            print("You sunk the battleship!")
    print("Game over - you win!")
    return