from flask import Flask, request, jsonify, send_from_directory
import chess
import random
import os

app = Flask(__name__)

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

@app.route('/api/move', methods=['POST'])
def make_move():
    data = request.json
    fen = data.get('fen')
    move = data.get('move')
    
    if not fen or not move:
        return jsonify({'error': 'Missing FEN or move'}), 400

    try:
        board = chess.Board(fen)
    except ValueError:
        return jsonify({'error': 'Invalid FEN'}), 400

    try:
        move_obj = chess.Move.from_uci(move)
        if move_obj in board.legal_moves:
            board.push(move_obj)
            return jsonify({
                'fen': board.fen(),
                'game_over': board.is_game_over(),
                'in_check': board.is_check(),
                'turn': 'white' if board.turn == chess.WHITE else 'black'
            })
        else:
            return jsonify({'error': 'Invalid move'}), 400
    except ValueError:
        return jsonify({'error': 'Invalid move format'}), 400

@app.route('/api/reset', methods=['POST'])
def reset_game():
    board = chess.Board()
    return jsonify({
        'fen': board.fen()
    })

@app.route('/api/computer_move', methods=['POST'])
def computer_move():
    data = request.json
    fen = data.get('fen')
    
    if not fen:
        return jsonify({'error': 'Missing FEN'}), 400

    try:
        board = chess.Board(fen)
    except ValueError:
        return jsonify({'error': 'Invalid FEN'}), 400
    
    if board.is_game_over():
        return jsonify({'error': 'Game is over'}), 400
    
    legal_moves = list(board.legal_moves)
    if not legal_moves:
        return jsonify({'error': 'No legal moves'}), 400
    
    # Debug: Log the legal moves
    print("Legal moves:", [move.uci() for move in legal_moves])

    # Simple AI: choose a random legal move
    move = random.choice(legal_moves)
    board.push(move)  # Update the board with the chosen move
    
    # Return the updated state
    return jsonify({
        'move': move.uci(),  # Computer's chosen move
        'fen': board.fen(),  # Updated FEN after the move
        'game_over': board.is_game_over(),
        'in_check': board.is_check(),
        'turn': 'white' if board.turn == chess.WHITE else 'black'
    })

if __name__ == '__main__':
    app.run(debug=True)

