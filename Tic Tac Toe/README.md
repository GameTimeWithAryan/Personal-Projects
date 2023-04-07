# Tic Tac Toe

This project contains the package `ttt_engine` with modules to make and control
a tic tac toe board for playing the game.

This project also includes 2 versions of the tic tac toe game made using the module -

1. The CLI game in terminal
2. The GUI game using pygame

## Installation

The `ttt_engine` package is currently not installable, but it will be in future versions

## Getting Started

The repository can be cloned and the games can be played out of the box.
Using the `ttt_engine` package requires placing it in the directory where it is to be used, as it
is not installabe yet

To use the package in a file named `usage.py`, the directory structue would look like this -

```
├── usage.py
├── ttt_engine
    ├── ... 
```

## Usage

The `Board` class in the `board.py` file is used to control the tic tac toe game. It supports
gameplay with more than 2 players, grids of any size and adding of custom rules for checking the
game state allowing to add custom win/draw conditions. You can think of this class as the Game
manager, and use its attributes to manage various aspects of the game

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

```text
  1 2 3
1 _ _ _
2 _ _ X
3 _ _ _
```

## Documentation

To understand all the methods available, it is a good idea to read the documentation of
the code. These methods can be chained together to form a game.

## Zero-indexed or One-indexed?

All methods of this module will take zero indexed values as their inputs and
return them as their outputs

## Modding

Even though the whole project is centered about this package being a tic tac toe game
engine, the modules can be easily modded to allow playing other turn based board games
like connect 4 and other tic tac toe variations.

### Modding Options -

To modify the way game behaves, some speical arguments can be passed to the constructor of
Board class. Info about the parameter are given below, as well as in the docs of the board class -

1. size - a grid of dimensions `size * size` will be generated
2. players - a list of player marks, could be used to add multiple players
3. state_checker - A class implementing StateChecker ABC can be added in
   state_checker.py and passed in to the Board class constructor to allow custom win and draw
   conditions

## Project Vocabulary

Some speical words might be used in docs and comments, here are their meanings

ttt - tic tac toe

grid - list of lists of cells, an n x n space containing cells to hold player marks

cell - single space which can hold a player mark

mark - player marker, e.g. X mark, O mark

row - each horizontal straight line is a row

column - each vertical straight line is column

### Rows and columns

Playing a move at row 1 and column 2 on the board will look like -

```text
  1 2 3
1 _ X _
2 _ _ _
3 _ _ _
```

The code to accomplish this task would look like -

```python
from ttt_engine.board import Board

game_board = Board()
game_board.play_move(0, 1)  # Methods work with Zero-indexed values
```
