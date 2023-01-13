# tetris-AI

The plan: to build tetris from scratch in Python, and then write AI/s that will play against each other as well as humans. I'm treating this as a self-imposed challenge, to build an AI that can beat me at the game, practicing coding skills and hopefully learning along the way.

## Setup

Run `Tetris/test-functions.py`, you can try uncommenting previous tests and running them (some may be deprecated).

## Current features

![multiplayer image](https://github.com/Olive-Roe/tetris-AI/blob/main/images/multiplayer.png?raw=true)

![singleplayer image](https://github.com/Olive-Roe/tetris-AI/blob/main/images/testing.png?raw=true)

See `bucket-list.txt` for a more in-depth overview of what has been done already and future plans

### Tetris Engine

- Command-line display (for testing)
- 7-bag randomiser system
- Piece class with piece type, orientation, and position
- Rotation (CW, CCW, 180) and kick tables
- Line clear detection
- T-spin detection (includes t-spin minis and neo-tsds)
- Board class with many features
  - Rotation, movement, soft drop, hard drop
  - Starting seed for bag randomiser

### Display

- Uses Turtle to display boards
- Displays pieces, garbage lines with full color
- Ghost piece displays
- Hold slot and next queue (text based for now)
- (incomplete) Text display for live stats
- Slideshow function (for testing boards)

### Games

- Game class for 1v1s
  - Support for displaying multiple boards (up to 2 currently)
  - Turtle keybinds (not very smooth, temporary)
  - Automatic input (for future AI)
  - Implementation of tetr.io attack table
    - Keeps track of back-to-back and combo
    - Sends garbage to opponent
    - (incomplete) Garbage queue

### AI

- Finds all locations a piece could rest on
- Finds all theoretical moves from a position
- Pathfinding to find actions to a target location
- Finds the number of holes in a board
- Orders a list of possible moves by the least number of holes and number of lines cleared
- Chooses the 'best' move and can be played against (very rudimentary AI as of now)

## Formats

Most of the formats used in this project (e.g. to represent a board state, or a piece, or amount of garbage received) are my own, and so might not be very intuitive/widely used.

You can see the list of formats in more detail in `formats.txt`.

## Note: Modern Tetris

The tetris that is used in this project might not be the one you're used to. This version of tetris includes many more features like faster piece placement, a hold slot, games against others, etc. Here is a [short summary of some differences](https://tetrisinterest.com/modern-tetris-and-classic-tetris-what-is-the-difference "Article highlighting difference of Modern and Classic tetris").
