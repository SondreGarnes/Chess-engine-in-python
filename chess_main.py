#This is the main driver file, it will be responsible for handling user input and displaying the current GameState object

class GameState():
    def __init__(self):
        #board is an 8x8 2d list, each element of the list has 2 characters.
        #The first character represents the color of the piece, 'b' or 'w'
        #The second character represents the type of the piece, 'K', 'Q', 'R', 'B', 'N' or 'P'
        #"--" represents an empty space with no piece
        self.board=[
            ["bR","bN","bB","bQ","bK","bB","bN","bR"],
            ["bp","bp","bp","bp","bp","bp","bp","bp"],
            ["--","--","--","--","--","--","--","--"],
            ['--','--','--','--','--','--','--','--'],
            ['--','--','--','--','--','--','--','--'],
            ['--','--','--','--','--','--','--','--'],
            ["wp","wp","wp","wp","wp","wp","wp","wp"],
            ["wR","wN","wB","wQ","wK","wB","wN","wR"]]