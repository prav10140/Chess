from flask import Flask, request, jsonify
import chess

app = Flask(__name__)

# Global variable to store the game state
board = chess.Board()

@app.route('/api/move', methods=['POST'])
def make_move():
    move = request.json['move']
    try:
        board.push_san(move)
        return jsonify({
            'fen': board.fen(),
            'game_over': board.is_game_over(),
            'in_check': board.is_check(),
            'turn': 'white' if board.turn == chess.WHITE else 'black'
        })
    except ValueError:
        return jsonify({'error': 'Invalid move'}), 400

@app.route('/api/reset', methods=['POST'])
def reset_game():
    global board
    board = chess.Board()
    return jsonify({'fen': board.fen()})

if __name__ == '__main__':
    app.run(debug=True)
