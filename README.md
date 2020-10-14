## Dots and Boxes

This UI for the dots and boxes game. Game rules can be found:
https://en.wikipedia.org/wiki/Dots_and_Boxes

What is unique about this implementation is that it allows not just to play against other human opponent 
but to play against 3 bot levels or to watch bots play against each other

Users can create there own bots following guidelines described in this repository:
https://github.com/lavinski/boxyDotsBot

Player selection page:
![PlayerSelection](Screenshots/playerselection.png?raw=true "Player Selection page")

### Bots
Game comes with 3 preinstalled bots

### Easy bot
**Players/RandomBot**

This bot is the simples one. What it does is just picks random move from available moves.

### Medium
**Players/MiniMaxBot**

This bot is implements using MiniMax algorithm (https://en.wikipedia.org/wiki/Minimax)

### Medium
**Players/AlphaBetaBot**

This bot is implements using MiniMax algorithm (https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning)

## ScreenShots
![BoxyDotsGame](Screenshots/dotsandboxes.png?raw=true "Dots and boxes")
![PlayerSelection](Screenshots/playerselection.png?raw=true "Player Selection page")
![GameExample](Screenshots/gameexample.png?raw=true "Game example")
