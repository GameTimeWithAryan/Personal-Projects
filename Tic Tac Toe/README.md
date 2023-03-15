# Tic Tac Toe

This project contains a package `ttt_engine` with modules to make and control
a tic tac toe board for playing the game.

This project also includes 2 versions of the tic tac toe game made using the module -

1. The CLI game in terminal
2. The GUI game using pygame

## Installation

The package is currently not installable

## Usage

The repository can be cloned and the games can be played out of the box.
Using the package requires placing it in the directory where it is to be used.

The Board class is used to control the game. It supports gameplay with more than 2 players
and grids of any size and supports custom classes to check the game state allowing you to add custom win/draw conditions.

To use the package in a file named `usage.py`, the directory structue would look like this -

```
├── usage.py
├── ttt_engine
    ├── ... 
```

Creating a Board instance which can be used to play the game -

```python
# usage.py

from ttt_engine import Board
game_board = Board()
```

Playing a move at coordinates row 2, column 3 of the grid and then printing the grid.
The play_move method's arguments are zero-indexed

```python
# usage.py

# ...
game_board.play_move(1, 2)
game_board.grid.print_grid()
```

### Output:

```python
  1 2 3
1 _ _ _
2 _ _ X
3 _ _ _
```

## Documentation

To understand all the methods available, it is a good idea to read the documentation of the code.
These methods can be chained together to form a game.

## Zero-indexed or One-indexed?
All methods of this module will take zero indexed values as their inputs and return them as their outputs
s