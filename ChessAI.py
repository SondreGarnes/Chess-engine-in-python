import random

piece_scores={"K":0,"Q":9,"R":5,"B":3,"N":3,"P":1}
CHECKMATE=1000
STALEMATE=0
DEPTH=3

def find_random_moves(validMoves):
    return validMoves[random.randint(0,len(validMoves)-1)]

def find_best_move_minmax(gs,validMoves):
    global nextMove
    find_move_minmax(gs,validMoves,DEPTH,gs.whiteToMove)
    return nextMove
    
def find_move_minmax(gs,validMoves,depth,whiteToMove ):
    global nextMove
    if depth==0:
        return score_board(gs)
    if whiteToMove:
        maxScore=-CHECKMATE
        random.shuffle(validMoves)
        for move in validMoves:
            gs.makeMove(move)
            nextMoves=gs.getValidMoves()
            score=find_move_minmax(gs,nextMoves,depth-1,False)
            if score>maxScore:
                maxScore=score
                if depth==DEPTH:
                    nextMove=move
            gs.undoMove()
        return maxScore
    else:
        minScore=CHECKMATE
        random.shuffle(validMoves)
        for move in validMoves:
            gs.makeMove(move)
            nextMoves=gs.getValidMoves()
            score=find_move_minmax(gs,nextMoves,depth-1,True)
            if score<minScore:
                minScore=score
                if depth==DEPTH:
                    nextMove=move
            gs.undoMove()
        return minScore

    
    
    



def find_best_move_greedy(gs,valid_Moves):
    turn_multiplier=1 if gs.whiteToMove else -1
    opponentMinMax_score= CHECKMATE
    best_player_move=None
    random.shuffle(valid_Moves)
    for playerMove in valid_Moves:
        gs.makeMove(playerMove)
        opponentMoves=gs.getValidMoves()
        if gs.stalemate:
            opponentMaxScore= STALEMATE
        elif gs.checkMate:
            opponentMaxScore= -CHECKMATE
        else:
            opponentMaxScore= -CHECKMATE
            for opponentsMove in opponentMoves:
                gs.makeMove(opponentsMove)
                gs.getValidMoves()
                if gs.checkMate:
                    score= CHECKMATE
                elif gs.stalemate:
                    score= STALEMATE
                else:
                    score= -turn_multiplier * score_board(gs.board)
                if score > opponentMaxScore:
                    opponentMaxScore=score
                gs.undoMove()
        if opponentMaxScore < opponentMinMax_score:
            opponentMinMax_score=opponentMaxScore
            best_player_move=playerMove
        gs.undoMove()
    return best_player_move

def score_board(gs):

    #positive score is good for white, negative score is good for black
    if gs.checkmate:
        if gs.whiteToMove:
            return -CHECKMATE
        else:
            return CHECKMATE
    elif gs.stalemate:
        return STALEMATE
    
    score=0
    for rows in gs.board:
        for square in rows:
            if square[0]=="w":
                score+=piece_scores[square[1]]
            elif square[0]=="b":
                score-=piece_scores[square[1]]
    return score

