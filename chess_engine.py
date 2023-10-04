#This class is responsible for storing all the information about the current state of the chess game, 
#also responsible for determining the valid moves at the current state. It will also keep a move log.
class GameState():
    def __init__(self):
        #board is an 8x8 2d list, each element of the list has 2 characters.
        #The first character represents the color of the piece, 'b' or 'w'
        #The second character represents the type of the piece, 'K', 'Q', 'R', 'B', 'N' or 'P'
        #"--" represents an empty space with no piece
        self.board=[
            ["bR","bN","bB","bQ","bK","bB","bN","bR"],
            ["bP","bP","bP","bP","bP","bP","bP","bP"],
            ["--","--","--","--","--","--","--","--"],
            ['--','--','--','--','--','--','--','--'],
            ['--','--','--','--','--','--','--','--'],
            ['--','--','--','--','--','--','--','--'],
            ["wP","wP","wP","wP","wP","wP","wP","wP"],
            ["wR","wN","wB","wQ","wK","wB","wN","wR"]]
        self.moveFunctions={'P':self.getPawnMoves,'R':self.getRookMoves,"N":self.getKnightMoves,
                            "B":self.getBishopMoves,"Q":self.getQueenMoves,"K":self.getKingMoves}
        self.whiteToMove=True
        self.moveLog=[]
        self.whiteKingLocation=(7,4)
        self.blackKingLocation=(0,4)
        self.chechMate=False
        self.staleMate=False
        self.isEnpassantMove=() #coordinates for the square where en passant capture is possible
        





    def makeMove(self,move):
        self.board[move.startRow][move.startCol]="--"
        self.board[move.endRow][move.endCol]=move.pieceMoved
        self.moveLog.append(move) #log the move so we can undo it later
        self.whiteToMove=not self.whiteToMove #swap players
        #update the king's location if moved
        if move.pieceMoved=="wK":
            self.whiteKingLocation=(move.endRow,move.endCol)
        elif move.pieceMoved=="bK":
            self.blackKingLocation=(move.endRow,move.endCol)

        #pawn promotion
        if move.isPawnPromotion:
            self.board[move.endRow][move.endCol]=move.pieceMoved[0]+"Q"
        
        #enpassant move
        if move.isEnpassantMove:
            self.board[move.startRow][move.endCol]="--"
        
        #update enpassant move variable
        if move.pieceMoved[1]=="P" and abs(move.startRow-move.endRow)==2: #only on 2 square pawn advances
            self.isEnpassantMove=((move.startRow+move.endRow)//2,move.startCol)
        else:
            self.isEnpassantMove=()




    def undoMove(self):
        if len(self.moveLog)!=0: #if there is a move to undo
            move=self.moveLog.pop()
            self.board[move.startRow][move.startCol]=move.pieceMoved
            self.board[move.endRow][move.endCol]=move.pieceCaptured
            self.whiteToMove=not self.whiteToMove
            #update the king's location if moved
            if move.pieceMoved=="wK":
                self.whiteKingLocation=(move.startRow,move.startCol)
            elif move.pieceMoved=="bK":
                self.blackKingLocation=(move.startRow,move.startCol)
            #undo enpassant move
            if move.isEnpassantMove:
                self.board[move.endRow][move.endCol]="--"
                self.board[move.startRow][move.endCol]=move.pieceCaptured
                self.isEnpassantMove=(move.endRow,move.endCol)
            #undo a 2 square pawn advance
            if move.pieceMoved[1]=="P" and abs(move.startRow-move.endRow)==2:
                self.isEnpassantMove=()
                

    
    def getValidMoves(self):
        tempEnpassantMove=self.isEnpassantMove
        #1)generate all possible moves
    
        moves=self.getAllPossibleMoves()

        #2)for each move, make the move
        for i in range(len(moves)-1,-1,-1): #when removing from a list, go backwards through that list
            self.makeMove(moves[i])

            self.whiteToMove=not self.whiteToMove #switch turns
            if self.inCheck():
                moves.remove(moves[i])#if the move leaves you in check, it's not a valid move
            self.whiteToMove=not self.whiteToMove #switch turns back
            self.undoMove()
        if len(moves)==0:
            if self.inCheck():
                self.checkMate=True
            else:
                self.staleMate=True
        else:
            self.checkMate=False
            self.staleMate=False
        self.isEnpassantMove=tempEnpassantMove
        return moves
        

        
    
    def inCheck(self):
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0],self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0],self.blackKingLocation[1])

    def squareUnderAttack(self,r,c):
        self.whiteToMove=not self.whiteToMove #switch to opponent's turn
        oppMoves=self.getAllPossibleMoves()
        self.whiteToMove=not self.whiteToMove #switch turns back
        for move in oppMoves:
            if move.endRow==r and move.endCol==c:
                return True
        return False
    

    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn=self.board[r][c][0]
                if (turn=="w" and self.whiteToMove) or (turn=="b" and not self.whiteToMove):
                    piece=self.board[r][c][1]
                    self.moveFunctions[piece](r,c,moves)
        return moves
    
    def getPawnMoves(self,r,c,moves):
        #white pawn moves
        if self.whiteToMove: #white pawn moves
            if self.board[r-1][c]=="--":#1 square pawn advance
                moves.append(Move((r,c),(r-1,c),self.board))
                if r==6 and self.board[r-2][c]=="--":#2 square pawn advance
                    moves.append(Move((r,c),(r-2,c),self.board))
            if c-1>=0:
                if self.board[r-1][c-1][0]=="b":#enemy piece to capture to the left
                    moves.append(Move((r,c),(r-1,c-1),self.board))
                elif (r-1,c-1)==self.isEnpassantMove:
                    moves.append(Move((r,c),(r-1,c-1),self.board,isEnpassantMove=True))
            if c+1<=7:
                if self.board[r-1][c+1][0]=="b":#enemy piece to capture to the right
                    moves.append(Move((r,c),(r-1,c+1),self.board))
                elif (r-1,c+1)==self.isEnpassantMove:
                    moves.append(Move((r,c),(r-1,c+1),self.board,isEnpassantMove=True))
        #black pawn moves
        if not self.whiteToMove:
            if self.board[r+1][c]=="--":
                moves.append(Move((r,c),(r+1,c),self.board))
                if r==1 and self.board[r+2][c]=="--":
                    moves.append(Move((r,c),(r+2,c),self.board))
            if c-1>=0:
                if self.board[r+1][c-1][0]=="w":
                    moves.append(Move((r,c),(r+1,c-1),self.board))
                elif (r+1,c-1)==self.isEnpassantMove:
                    moves.append(Move((r,c),(r+1,c-1),self.board,isEnpassantMove=True))
            if c+1<=7:
                if self.board[r+1][c+1][0]=="w":
                    moves.append(Move((r,c),(r+1,c+1),self.board))    
                elif (r+1,c+1)==self.isEnpassantMove:
                    moves.append(Move((r,c),(r+1,c+1),self.board,isEnpassantMove=True))

            


    def getRookMoves(self,r,c,moves):
        
        directions=((-1,0),(0,-1),(1,0),(0,1))
        enemyColor="b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1,8):
                endRow=r+d[0]*i
                endCol=c+d[1]*i
                if 0<=endRow<8 and 0<=endCol<8:
                    endPiece=self.board[endRow][endCol]
                    if endPiece=="--":
                        moves.append(Move((r,c),(endRow,endCol),self.board))
                    elif endPiece[0]==enemyColor:
                        moves.append(Move((r,c),(endRow,endCol),self.board))
                        break
                    else: #friendly piece
                        break
                else: #off board
                    break


    
    def getKnightMoves(self,r,c,moves):
        #get all the moves for the knight
        knightMoves=[(-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1)]
        allyColor="w" if self.whiteToMove else "b"
        for m in knightMoves:
            endRow=r+m[0]
            endCol=c+m[1]
            if 0<=endRow<8 and 0<=endCol<8:
                endPiece=self.board[endRow][endCol]
                if endPiece[0]!=allyColor:
                    moves.append(Move((r,c),(endRow,endCol),self.board))


    def getBishopMoves(self,r,c,moves):
        #get all the moves for the bishop
        directions=((1,1),(1,-1),(-1,1),(-1,-1))
        enemyColor="b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1,8):
                endRow=r+d[0]*i
                endCol=c+d[1]*i
                if 0<=endRow<8 and 0<=endCol<8:
                    endPiece=self.board[endRow][endCol]
                    if endPiece=="--":
                        moves.append(Move((r,c),(endRow,endCol),self.board))
                    elif endPiece[0]==enemyColor:
                        moves.append(Move((r,c),(endRow,endCol),self.board))
                        break
                    else:
                        break
                else:
                    break


    def getQueenMoves(self,r,c,moves):
        directions=((1,1),(1,-1),(-1,1),(-1,-1),(1,0),(0,1),(-1,0),(0,-1))
        enemyColor="b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1,8):
                endRow=r+d[0]*i
                endCol=c+d[1]*i
                if 0<=endRow<8 and 0<=endCol<8:
                    endPiece=self.board[endRow][endCol]
                    if endPiece=="--":
                        moves.append(Move((r,c),(endRow,endCol),self.board))
                    elif endPiece[0]==enemyColor:
                        moves.append(Move((r,c),(endRow,endCol),self.board))
                        break
                    else:
                        break
                else:
                    break

    def getKingMoves(self,r,c,moves):
        directions=((1,1),(1,-1),(-1,1),(-1,-1),(1,0),(0,1),(-1,0),(0,-1))
        allyColor="w" if self.whiteToMove else "b"
        for i in range(8):
            endRow=r+directions[i][0]
            endCol=c+directions[i][1]
            if 0<=endRow<8 and 0<=endCol<8:
                endPiece=self.board[endRow][endCol]
                if endPiece[0]!=allyColor:
                    moves.append(Move((r,c),(endRow,endCol),self.board))
                    

    

    



#This class is responsible for storing information about the current state of a chess game. 
#It will also be responsible for determining the valid moves at the current state. It will also keep a move log.   
class Move():
    #maps keys to values
    #key:value
    ranksToRows={"1":7,"2":6,"3":5,"4":4,
                 "5":3,"6":2,"7":1,"8":0}
    rowsToRanks={v:k for k,v in ranksToRows.items()}
    filesToCols={"a":0,"b":1,"c":2,"d":3,
                 "e":4,"f":5,"g":6,"h":7}
    colsToFiles={v:k for k,v in filesToCols.items()}

    def __init__(self,startSq,endSq,board, isEnpassantMove=False):
        self.startRow=startSq[0]
        self.startCol=startSq[1]
        self.endRow=endSq[0]
        self.endCol=endSq[1]
        self.pieceMoved=board[self.startRow][self.startCol]
        self.pieceCaptured=board[self.endRow][self.endCol]
        self.moveID=self.startRow*1000+self.startCol*100+self.endRow*10+self.endCol
       
        self.isPawnPromotion=(self.pieceMoved=="wP" and self.endRow==0) or (self.pieceMoved=="bP" and self.endRow== 7)

        self.isEnpassantMove=isEnpassantMove
        if self.isEnpassantMove:
            self.pieceCaptured="wP" if self.pieceMoved=="bP" else "bP"    
        
    
    #Overriding the equals method
    def __eq__(self,other):
        if isinstance(other,Move):
            return self.moveID==other.moveID
        return False
    
    def getChessNotation(self):
        return self.getRankFile(self.startRow,self.startCol)+self.getRankFile(self.endRow,self.endCol)

    def getRankFile(self,r,c):
        return self.colsToFiles[c]+self.rowsToRanks[r]
    