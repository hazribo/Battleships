from components import initialise_board, create_battleships, place_battleships
from game_engine import attack, cli_coordinates_input
import random as rdm
import json

# Generates AI attack coords to send to attack():
def generate_attack(last_attack=[-1, -1, False], ai_used_coords=[], difficulty="easy"):
    # Easy difficulty - AI will just pick random squares:
    if difficulty == "easy":
        x = rdm.randint(0, 9)
        y = rdm.randint(0, 9)
        ai_coords = tuple((x, y))

    # Normal difficulty - AI will pick squares adjacent to hit squares:
    if difficulty == "normal":
        print(last_attack)
        x, y = last_attack[0], last_attack[1]
        hit = last_attack[2]

        # Gets the squares the AI can pick:
        adjacent_squares = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
        # Filters out invalid choices (outside of board size):
        usable_squares = [(x, y) for x, y in adjacent_squares if 0 <= x < 10 and 0 <= y < 10]
        # Filters out squares that have already been used:
        valid_squares = [(x, y) for x, y in usable_squares if (x, y) not in ai_used_coords]
        print(valid_squares)

        # Selects attack square if valid option exists:
        if hit == True and valid_squares != []:
            choice = rdm.choice(valid_squares)
            ai_coords = tuple(choice)
        else:
            x = rdm.randint(0, 9)
            y = rdm.randint(0, 9)
            ai_coords = tuple((x, y))
    return ai_coords

# Runs 2 player (user + AI) game loop
def ai_opponent_game_loop():
    print("Welcome to Battleships!")
    user_board = initialise_board()
    ai_board = initialise_board()

    # Loads placement.json; 
    f = open("placement.json", "r")
    user_ships = json.load(f)
    ai_ships = create_battleships()
    # Places battleships on both user and AI board:
    place_battleships(user_board, user_ships, "custom")
    place_battleships(ai_board, ai_ships, "random")

    # Game continues as long as all ships haven't been sunk:
    while any(val is not None for row in user_board + ai_board for val in row): 
        # User attack:
        coords = cli_coordinates_input()
        hit, sunk = attack(coords, ai_board, ai_ships)
        if hit == True:
            print("Hit!")
        else:
            print("Miss!")
        if sunk == True:
            print("You sunk the AIs battleship!")

        # AI attack:
        ai_coords = generate_attack()
        ai_hit, ai_sunk = attack(ai_coords, user_board, user_ships)
        if ai_hit == True:
            print(f"AI attacked {ai_coords}. Hit!")
        else:
            print(f"AI attacked {ai_coords}. Miss!")
        if ai_sunk == True:
            print("The AI sunk your battleship!")

    print("Game over.")
    return

# Allows manual testing of simple_game_loop
if __name__ == "__main__":
    ai_opponent_game_loop()