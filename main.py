from flask import Flask, render_template, jsonify, request
import json
from components import *
from mp_game_engine import *

app = Flask(__name__)

# Initialises variables:
board = []
ai_last_attack = [-1, -1, False]
ai_used_coords = []
user_used_coords = []
game_finished = False

## CHANGE DIFFICULTY SETTING BELOW:
# Options: easy, normal
DIFFICULTY = "normal"

# Initialises the AI board:
ai_board = initialise_board()
ai_ships = create_battleships()
place_battleships(ai_board, ai_ships, "random")

@app.route("/", methods=["GET"])
def root():
    global board
    print(board)

    if request.method == "GET":
        print(json.dumps(board))
        return render_template("main.html", player_board=board)

@app.route("/attack", methods=["GET"])
def attack():
    global board
    global ai_board
    global ai_last_attack
    global game_finished

    if request.args:
        while not game_finished:
            # Gets the x and y values for the tile that the user clicked:
            x = request.args.get("x")
            y = request.args.get("y")
            x, y = int(x), int(y)
            print(x, y)
            user_coords = (x, y)

            repeat = False
            if user_coords in user_used_coords:
                repeat = True
            else:
                user_used_coords.append(user_coords)
                # Checks to see if you hit the AIs ship:
                if ai_board[x][y] != None:
                    ai_board[x][y] = None
                    hit = True
                else:
                    hit = False
            
            # Runs AI turn to get coords, no duplicates:
            ai_unique = False
            while not ai_unique:    
                ai_coords = generate_attack(ai_last_attack, ai_used_coords, DIFFICULTY)
                print(ai_coords)
                if ai_coords in ai_used_coords:
                    ai_unique = False
                
                # Gets AI attack, only if user attack was valid:
                elif ai_coords not in ai_used_coords and repeat == False:
                    # Saves last attack co-ordinates for medium difficulty:
                    c = str(ai_coords)
                    c = c.strip("()").split(",")
                    ai_x, ai_y = int(c[0]), int(c[1])

                    # Checks (ai_y, ai_x) as that's what main.html does:
                    if board[ai_y][ai_x] != None:
                        board[ai_y][ai_x] = None
                        ai_last_attack = [ai_x, ai_y, True]
                    else:
                        ai_last_attack = [ai_x, ai_y, False]

                    # Saves new coords to ai used coords list:
                    ai_used_coords.append(ai_coords)
                    ai_unique = True
                    
                    # Checks if user has won (all values in AI board are None):
                    if all(val is None for row in ai_board for val in row):
                        game_finished = True
                        return jsonify({"hit": hit, "AI_Turn": ai_coords, "finished": "Game over! You win!"})
                    
                    # Checks if user has lost (all values in user board are None):
                    elif all(val is None for row in board for val in row):
                        game_finished = True
                        return jsonify({"hit": hit, "AI_Turn": ai_coords, "finished": "Game over! You lose."})
                    
                    # Otherwise, sends data to template:
                    elif any(val is not None for row in board + ai_board for val in row): 
                        return jsonify({"hit": hit, "AI_Turn": ai_coords})

@app.route("/placement", methods=["GET", "POST"])
def placement_interface():
    ships = create_battleships()
    print(ships)
    BOARD_SIZE = 10

    if request.method == "GET":
        return render_template("placement.html", board_size=BOARD_SIZE, ships=ships)
    
    if request.method == "POST":
        global board
        # get ship data & pass to board:
        data = request.get_json()
        print(data)
        board_data = initialise_board()
        board = place_battleships(board_data, data, "flask")
        return jsonify({"success": True})

if __name__ == "__main__":
    app.template_folder = "templates"
    app.run()