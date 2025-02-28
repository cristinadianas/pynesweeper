# Pynesweeper

Pynesweeper is a Python-based implementation of the classic Minesweeper game, using the `curses` library for a terminal-based interface. The game allows players to uncover cells, mark potential mines, and navigate the board using keyboard controls.

## Features
- **Multiple Difficulty Levels**: Choose from Beginner, Medium, Difficult, or a custom board size.
- **Customizable Board**: Set your own width, height, and number of mines.
- **Keyboard Controls**:
  - Arrow keys to move the cursor.
  - Spacebar to reveal a cell. 
  - 'X' to mark/unmark a potential mine.
  - 'ESC' to exit the game.
- **Smart Reveal Mechanism**: Pressing Spacebar on an already revealed cell will automatically uncover all surrounding cells if the number of marked mines matches the number displayed on the cell. Otherwise, it does nothing.
- **Color-Coded Interface**: Different colors for marked mines, numbers, and game status.
- **Win/Lose Conditions**:
  - Win by uncovering all non-mine cells.
  - Lose by stepping on a mine.
- **Live Timer**: Track the time taken to complete the game.

## Flow
1. Select a difficulty level or create a custom board.
2. Navigate using the arrow keys.
3. Press `Space` to reveal a cell or `X` to mark a suspected mine.
5. Uncover all non-mine cells to win.
6. Avoid stepping on a mine to prevent losing the game.

## Controls
| Key  | Action               |
|------|----------------------|
| ↑    | Move cursor up      |
| ↓    | Move cursor down    |
| ←    | Move cursor left    |
| →    | Move cursor right   |
| Space| Reveal cell         |
| X    | Mark/unmark mine    |
| ESC  | Exit game           |

## Installation
Pynesweeper requires Python 3 and the `curses` module, which is included by default in Linux and macOS but requires `windows-curses` on Windows.

### Install dependencies (Windows only):
```sh
pip install windows-curses
```

## Running the Game
To start the game, run:
```sh
python pynesweeper.py
```
Follow the on-screen prompts to select your difficulty and play the game.

## Enjoy playing Pynesweeper!


