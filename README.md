#Chess Bot Project

##Introduction
This project is a functional chess bot capable of playing against a human player. It features a graphical user interface (GUI) where players can move chess pieces, and the bot responds with reasonable moves based on the current state of the chessboard. The bot utilizes the Minimax algorithm with alpha-beta pruning to efficiently determine its moves.

##Features
- User-Friendly Interface: The GUI allows users to easily select and move chess pieces.
- Accurate Chess Logic: Implements all chess rules, including castling, en passant, promotion, and checkmate.
- AI Competence: The chess bot plays at a level suitable for casual players.

##Requirements
 - Python 3.x
 - numpy library
 - pygame library
 - tkinter library

##Algorithm Details
The main algorithm used by the bot is located in the algorithms folder, specifically in the minmax.py file. This file contains the implementation of the Minimax algorithm with alpha-beta pruning.

##Project Structure
pygame_gui.py: Main script to run the chess GUI.
algorithms/minmax.py: Contains the Minimax algorithm with alpha-beta pruning.
piece/: Contains classes for different chess pieces and their movement logic.
undo_functions/: Contains functions to undo moves.
board/: Contains functions to load the board from FEN notation and handle board-related logic.
castling/: Contains functions related to castling moves.
en_passant/: Contains functions related to en passant captures.
promotion/: Contains functions related to piece promotion.

##How to Play
Run the GUI script.
Move pieces by clicking on them and selecting the target square.
The bot will automatically make its move after yours.
The game ends when a checkmate, stalemate, or draw by repetition occurs.
Introduction

MIT License

Copyright (c) [2024] [Thijn Broekhuizen]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
