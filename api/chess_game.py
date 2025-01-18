from flask import Flask, request, jsonify, send_from_directory
import chess
import random
import os

app = Flask(__name__)

# Global variable to store the game state
board = chess.Board()

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

@app.route('/api/move', methods=['POST'])
def make_move():
    global board
    move = request.json['move']
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
    global board
    board = chess.Board()
    return jsonify({
        'fen': board.fen()
    })

@app.route('/api/computer_move', methods=['POST'])
def computer_move():
    global board
    fen = request.json['fen']
    board.set_fen(fen)
    
    if board.is_game_over():
        return jsonify({'error': 'Game is over'})
    
    legal_moves = list(board.legal_moves)
    if not legal_moves:
        return jsonify({'error': 'No legal moves'})
    
    # Simple AI: choose a random legal move
    move = random.choice(legal_moves)
    board.push(move)
    
    return jsonify({
        'move': move.uci(),
        'fen': board.fen(),
        'game_over': board.is_game_over(),
        'in_check': board.is_check(),
        'turn': 'white' if board.turn == chess.WHITE else 'black'
    })

if __name__ == '__main__':
    app.run(debug=True)


