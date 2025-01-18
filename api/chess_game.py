from flask import Flask, request, jsonify, send_from_directory
import chess
import os

app = Flask(__name__)

# Global variable to store the game state
board = chess.Board()

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

@app.route('/api/move', methods=['POST'])
def make_move():
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

if __name__ == '__main__':
    app.run(debug=True)


