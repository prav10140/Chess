import chess
import json

def chess_game(request):
    board = chess.Board()
    
    # Get the player's move from the request (e.g., e2e4)
    move = request.args.get('move', '')
    
    if move:
        # Make the player's move if valid
        try:
            move_obj = chess.Move.from_uci(move)
            if move_obj in board.legal_moves:
                board.push(move_obj)
            else:
                return json.dumps({"error": "Illegal move"})
        except Exception as e:
            return json.dumps({"error": "Invalid move format"})
    
    # Check game state
    game_status = ""
    if board.is_checkmate():
        game_status = "Checkmate"
    elif board.is_stalemate():
        game_status = "Stalemate"
    elif board.is_check():
        game_status = "Check"
    
    # Return the current board as a FEN string and game status
    return json.dumps({"board": board.fen(), "status": game_status})

