# Battleships Game

Welcome to Battleships! This is my submission of my coursework for ECM1400 - Programming.
There are three different ways of playing: the simple game loop, AI opponent game loop, and via a web interface by using Flask.

This has been uploaded to Github at the following link: https://github.com/hazribo/Battleships/

## Table of Contents
- [Simple Game Loop](#simple-game-loop)
- [AI Opponent Game Loop](#ai-opponent-game-loop)
- [Flask Web Interface](#flask-web-interface)

- [Explanation of Game Files](#explanation-of-game-files)

- [Usage](#usage)
- [Testing](#testing)

## Simple Game Loop

Run the components.py file. This starts a game with just one board that the player attacks. Valid inputs are "(x, y) or "x, y". You are unable to input duplicate coordinates, and will be told to re-input if done so.

You can see your progress as a visualisation of the current board - showing "O" for missed shots and "X" for hits - is printed every round.

**NOTE:** To edit the type of ship placement that the board uses, you can modify the value of the "MODE" constant on line 34 of game_engine.py. The options available for this are "simple", "random", or "custom".
1. Simple placement: each ship is placed horizontally on each line from x values 0-4.
2. Random placement: ships are randomly placed around the board and can be both vertical and horizontal.
3. Custom placement: using the data from placement.json, the ships are placed onto the board. 
This json data uses the following format:

**{ShipName: [starting x coordinate, starting y coordinate, orientation]}**

The orientation can either be horizontal ("h"), or vertical ("v"). To modify this, **do not change the name of the ship**, only the position and orientation.

## AI Opponent Game Loop

Run the mp_game_engine.py file. This starts a game with two boards, one for the user and one for the AI. 
This uses the layout in the placement.json file for the user's board, and the random ship placement option for the AI's board.
This is functionally identical to the simple game loop, with the exception of the AI making attacks against your board, and you lose if the AI sinks all of your battleships before you sink all of the AI battleships.

## Flask Web Interface

This version of the game uses components.py, game_engine.py and mp_game_engine.py as the backend for a web interace using the Python library Flask and two template html files, main.html and placement.html.

Run the main.py file, and visit http://127.0.0.1:5000/placement. 
This takes you to the page that allows you to place each of your five ships on your board, using the R key to rotate the ship and the left mouse button to place them. The AI board is created using the random ship placement option.
Once all five ships have been placed, you click the green "Send Game" button, and you are redirected to http://127.0.0.1:5000. 
You and the AI take turns firing shots at the other's board. The game ends once either player has successfully sunk all of their opponents battleships.

**NOTE:** There are two difficulty options for the AI. The default is "normal", but there is an "easy" difficulty that can also be used. This can be changed by modifying the value of the "DIFFICULTY" constant on line 17 of main.py.
1. Easy difficulty: the AI randomly picks a square (that hasn't yet been attacked) and attacks it.
2. Normal difficulty: the game as easy, however, if the AI hits a user ship, its next attack will be one of the four squares directly adjacent to the previous attack square (if any are valid to be attacked).

## Explanation of Game Files

1. Components.py
This module has the following functions:
- initialise_board: creates a board of size 10x10, with each index holding a value of None.
- create_battleships: reads the battleship.txt file and gets battleship info.
- place_battleships(board, ships, type): uses the board and battleship info to place the battleships in the given style (type).

2. Game_engine.py
This module has the following functions:
- attack(coords, board, ships): carries out the attack on the given board at the given coordinates.
- cli_coordinates_input: client coordinate input; takes the user's inputted coordinates, returns them as a tuple.
- [simple_game_loop](#simple-game-loop)

3. Mp_game_engine.py
This module has the following functions:
- generate_attack(last_attack, ai_used_coords, difficulty): generates the AI's attack depending on the difficulty, whether it last hit a ship or not, and ensuring it cannot attack a square that has already been attacked.
- [ai_opponent_game_loop](#ai-opponent-game-loop).

## Usage

These modes can all be run by opening the files in the folder, or by running the files inside of an IDE. 
All modes can be run on any modern device that has Python installed, as well as the following libraries.
These can be installed by using **pip install NAME_HERE** in the command line:
- Flask
- Json
- Jsonify

For the testing files to work, the following libraries need to also be installed:
- Pytest
- Pytest-depends
- Pytest-cov

## Testing

You can run the testing files by running the module test_students.py, which is inside of the tests folder.
Upon being run, a file named test_report.txt is created in the base directory. This will show any errors in the code, if any. 
As of writing this, **there are no errors** in any of my program files.
