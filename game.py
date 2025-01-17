import chess
import json

def chess_game(request):
    # Initialize a new chess game
    board = chess.Board()

    # Get move from the request (if any)
    move = request.args.get('move', '')

    if move:
        try:
            # Try to make the move
            move_obj = chess.Move.from_uci(move)
            if move_obj in board.legal_moves:
                board.push(move_obj)
            else:
                return json.dumps({"error": "Illegal move"})
        except Exception as e:
            return json.dumps({"error": "Invalid move format"})

    # Check for game status
    game_status = ""
    if board.is_checkmate():
        game_status = "Checkmate"
    elif board.is_stalemate():
        game_status = "Stalemate"
    elif board.is_check():
        game_status = "Check"

    # Return the board's FEN string and game status
    return json.dumps({"board": board.fen(), "status": game_status})
