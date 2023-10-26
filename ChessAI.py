import random

piece_scores={"K":0,"Q":9,"R":5,"B":3,"N":3,"P":1}
CHECKMATE=1000
STALEMATE=0


def find_random_moves(validMoves):
    return validMoves[random.randint(0,len(validMoves)-1)]
    


def find_best_move(gs,valid_Moves):
    turn_multiplier=1 if gs.whiteToMove else -1
    opponentMinMax_score= CHECKMATE
    best_player_move=None
    random.shuffle(valid_Moves)
    for playerMove in valid_Moves:
        gs.makeMove(playerMove)
        opponentMoves=gs.getValidMoves()
        opponentMaxScore= -CHECKMATE
        for opponentsMove in opponentMoves:
            gs.makeMove(opponentsMove)
            if gs.checkMate:
                score= - turn_multiplier * CHECKMATE
            elif gs.stalemate:
                score= STALEMATE
            else:
                score= -turn_multiplier * score_material(gs.board)
            if score > opponentMaxScore:
                opponentMaxScore=score
            gs.undoMove()
        if opponentMaxScore < opponentMinMax_score:
            opponentMinMax_score=opponentMaxScore
            best_player_move=playerMove
        gs.undoMove()
    return best_player_move


#only takes into account material score and the next move possible where you can win pieces
def find_best_move_greedy(gs,valid_Moves):
    turn_multiplier=1 if gs.whiteToMove else -1
    max_score= -CHECKMATE
    best_move=None
    for playerMove in valid_Moves:
        gs.makeMove(playerMove)
        if gs.checkMate:
            score= CHECKMATE
        elif gs.stalemate:
            score= STALEMATE
        else:
            score= turn_multiplier * score_material(gs.board)
        if score > max_score:
            max_score=score
            best_move=playerMove
        gs.undoMove()
    return best_move



def score_material(board):
    score=0
    for rows in board:
        for square in rows:
            if square[0]=="w":
                score+=piece_scores[square[1]]
            elif square[0]=="b":
                score-=piece_scores[square[1]]
    return score