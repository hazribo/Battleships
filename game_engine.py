from components import initialise_board, create_battleships, place_battleships

# Checks if ship is at given coords, replace with None & decrements size
def attack(coords: tuple, board: list, ships: dict):
    x, y = coords
    print(coords)
    ship = board[y][x]
    if ship != None:
        hit = True
        ships[board[y][x]] -= 1
        board[y][x] = None

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
    MODE = "random" 

    print("Welcome to Battleships!")

    # Initialise Variables:
    board = initialise_board()
    ships = create_battleships()
    visual_board = initialise_board()
    used_coords = []
    over = False
    place_battleships(board, ships, MODE)

    # below loops until every value in board = None
    while over == False:
        for line in visual_board:
            print(line)
        unique = False
        while not unique:
            coords = cli_coordinates_input()
            if coords in used_coords:
                print("You've already attacked this square.")
            else:
                unique = True
                used_coords.append(coords)

        hit, sunk = attack(coords, board, ships)
        x, y = coords
        if hit == True:
            visual_board[y][x] = "X"
            print("Hit!")
        else:
            visual_board[y][x] = "O"
            print("Miss!")
        if sunk == True:
            print("You sunk the battleship!")

        # Checks to see if all ships have been hit:
        if all(val is None for row in board for val in row):
            over = True

    print("Game over - you win!")
    return