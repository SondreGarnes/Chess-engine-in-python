#This is the main driver file, it will be responsible for handling user input and displaying the current GameState object
import pygame as p
import chess_engine, ChessAI

WIDTH=HEIGHT=512
DIMENSION=8 #8x8 chess board
SQ_SIZE=HEIGHT//DIMENSION
MAX_FPS=15 #for animations later on
IMAGES={}

#Initialize a global dictionary of images. This will be called exactly once in the main
def loadImages():
    pieces=['wP','wR','wN','wB','wK','wQ','bP','bR','bN','bB','bK','bQ']
    for piece in pieces:
        IMAGES[piece]=p.transform.scale(p.image.load("images/"+piece+".png"),(SQ_SIZE,SQ_SIZE))
    #Note: we can access an image by saying 'IMAGES['wP']'

#The main driver for our code. This will handle user input and updating the graphics
def main():
    p.init()
    screen=p.display.set_mode((WIDTH,HEIGHT))
    clock=p.time.Clock()
    screen.fill(p.Color("white"))
    gs=chess_engine.GameState()
    validMoves=gs.getValidMoves()
    moveMade=False #flag variable for when a move is made
    animate=False #flag variable for when we should animate a move
    loadImages()
    running=True
    sqSelected=() #no square is selected, keep track of the last click of the user (tuple:(row,col))
    playerClicks=[] #keep track of player clicks (two tuples: [(6,4),(4,4)])
    gameOver=False
    player_one=True #if a human is playing white, then this will be True. If an AI is playing, then False
    player_two=False #same as above but for black
    while running:
        human_turn=(gs.whiteToMove and player_one) or (not gs.whiteToMove and player_two)
        for e in p.event.get():
            if e.type==p.QUIT:
                running=False
            #mouse handler
            elif e.type==p.MOUSEBUTTONDOWN:
                if not gameOver and human_turn:
                    location=p.mouse.get_pos() #(x,y) location of mouse
                    col=location[0]//SQ_SIZE
                    row=location[1]//SQ_SIZE
                    if sqSelected==(row,col):#the user clicked the same square twice
                        sqSelected=() #deselect
                        playerClicks=[] #clear player clicks
                    else:
                        sqSelected=(row,col)
                        playerClicks.append(sqSelected) #append for both 1st and 2nd clicks
                    if len(playerClicks)==2:
                        move=chess_engine.Move(playerClicks[0],playerClicks[1],gs.board)
                        print(move.getChessNotation())
                        for i in range(len(validMoves)):
                            if move == validMoves[i]:
                                gs.makeMove(validMoves[i])
                                moveMade=True
                                animate=True
                                sqSelected=() #reset user clicks    
                                playerClicks=[] 
                        if moveMade==False:
                            playerClicks=[sqSelected]
            #key handler
            elif e.type==p.KEYDOWN:
                if e.key==p.K_z: #undo when 'z' is pressed
                    gs.undoMove()
                    moveMade=True
                    animate=False
                if e.key==p.K_r:#reset the board when 'r' is pressed
                    gs=chess_engine.GameState()
                    validMoves=gs.getValidMoves()
                    sqSelected=()
                    playerClicks=[]
                    moveMade=False
                    animate=False
        #AI move finder logic
        if not gameOver and not human_turn:
            AImove=ChessAI.find_best_move(gs,validMoves)
            if AImove is None:
                AImove=ChessAI.find_random_moves(validMoves)
            gs.makeMove(AImove)
            moveMade=True
            animate=True

        if moveMade:
            if animate:
                animatingMove(gs.moveLog[-1],screen,gs.board,clock)
            validMoves=gs.getValidMoves()
            moveMade=False
            animate=False

        drawGameState(screen,gs,validMoves,sqSelected)
        if gs.chechkmate:
            gameOver=True
            if gs.whiteToMove:
                drawText(screen,'Black wins by checkmate')
            else:
                drawText(screen,'White wins by checkmate')
        elif gs.stalemate:
            gameOver=True
            drawText(screen,'Stalemate')

        clock.tick(MAX_FPS)
        p.display.flip()

def highlightsquares(screen,gs,validMoves,sqSelected):
    if sqSelected!=():
        r,c=sqSelected
        if gs.board[r][c][0]==("w" if gs.whiteToMove else "b"): #sqselected is a piece that can be moved
            #highlight selected square
            s=p.Surface((SQ_SIZE,SQ_SIZE))
            s.set_alpha(100)
            s.fill(p.Color('blue'))
            screen.blit(s,(c*SQ_SIZE,r*SQ_SIZE))
            #highlight moves from that square
            s.fill(p.Color('yellow'))
            for move in validMoves:
                if move.startRow==r and move.startCol==c:
                    screen.blit(s,(move.endCol*SQ_SIZE,move.endRow*SQ_SIZE))






#Responsible for all the graphics within a current game state
def drawGameState(screen,gs,validMoves,sqSelected):
    drawBoard(screen) #draw squares on the board
    highlightsquares(screen,gs,validMoves,sqSelected)
    drawPieces(screen,gs.board) #draw pieces on top of those squares


#Draw the squares on the board.
def drawBoard(screen):
    global colors
    colors=[p.Color("white"),p.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color=colors[((r+c) % 2)]
            p.draw.rect(screen,color,p.Rect(c*SQ_SIZE,r*SQ_SIZE,SQ_SIZE,SQ_SIZE))

#Draw the pieces on the board using the current GameState.board
def drawPieces(screen,board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece=board[r][c]
            if piece!="--":
                screen.blit(IMAGES[piece],p.Rect(c*SQ_SIZE,r*SQ_SIZE,SQ_SIZE,SQ_SIZE))


def animatingMove(move,screen,board,clock):
    global colors
    dR=move.endRow-move.startRow
    dC=move.endCol-move.startCol
    framesPerSquare=10 #frames to move one square
    frameCount=(abs(dR)+abs(dC))*framesPerSquare
    for frame in range(frameCount+1):
        r,c=((move.startRow+dR*frame/frameCount,move.startCol+dC*frame/frameCount))
        drawBoard(screen)
        drawPieces(screen,board)
        #erase the piece moved from its ending square
        color=colors[(move.endRow+move.endCol)%2]
        endSquare=p.Rect(move.endCol*SQ_SIZE,move.endRow*SQ_SIZE,SQ_SIZE,SQ_SIZE)
        p.draw.rect(screen,color,endSquare)
        #draw captured piece onto rectangle
        if move.pieceCaptured!="--":
            screen.blit(IMAGES[move.pieceCaptured],endSquare)
        #draw moving piece
        screen.blit(IMAGES[move.pieceMoved],p.Rect(c*SQ_SIZE,r*SQ_SIZE,SQ_SIZE,SQ_SIZE))
        p.display.flip()
        clock.tick(60)


def drawText(screen,text):
    font=p.font.SysFont("Helvitca",32,True,False)
    textObject=font.render(text,0,p.Color('Gray'))
    textLocation=p.Rect(0,0,WIDTH,HEIGHT).move(WIDTH/2-textObject.get_width()/2,HEIGHT/2-textObject.get_height()/2)
    screen.blit(textObject,textLocation)
    textObject=font.render(text,0,p.Color('Black'))
    screen.blit(textObject,textLocation)


if __name__=="__main__":
    main()


