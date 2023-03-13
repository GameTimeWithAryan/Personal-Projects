# Tic Tac Toe

This project contains a package `ttt_engine` with modules to make and control a tic tac toe board for playing the game.
This project also includes 2 versions of the tic tac toe game made using the module -

1. The CLI game in terminal
2. The GUI game using pygame

## Installation

The package is currently not installable

## Usage

The repository can be cloned and the games can be played out of the box. For using the package, it needs to be used
directly by placing it in the directory to be used.
A file named `usage.py` placed in the same directory as the `ttt_engine` package can use the package as shown -

Creating a board object which can be used to play the game with its methods of size 3 i.e. a 3 X 3 grid

```python
from ttt_engine import Board

game_board = Board(3)
```

Playing a move at coordinate 2, 3 (row 2, column 3) of the grid and then printing the grid. The play_move method's
arguments are zero-indexed

```python
game_board.play_move(1, 2)
game_board.grid.print_grid()
```

#### Output:

```python
  1 2 3
1 _ _ _
2 _ _ X
3 _ _ _
```

### Documentation

Documentation of the code should be read to get an idea of all the methods available. These methods can be chained
together to form a game.

## Zero-indexed or One-indexed?
All methods of this module will take zero indexed values as their inputs and return them their outputs