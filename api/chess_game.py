from flask import Flask, request, jsonify
import chess

app = Flask(__name__)

# Global variable to store the game state
board = chess.Board()

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
                'turn': 'white' if board.turn == chess.WHITE else 'black',
                'valid_moves': [move.uci() for move in board.legal_moves]
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
        'fen': board.fen(),
        'valid_moves': [move.uci() for move in board.legal_moves]
    })

@app.route('/api/valid_moves', methods=['GET'])
def get_valid_moves():
    square = request.args.get('square')
    if square:
        valid_moves = [move.uci() for move in board.legal_moves if move.from_square == chess.parse_square(square)]
    else:
        valid_moves = [move.uci() for move in board.legal_moves]
    return jsonify({'valid_moves': valid_moves})

if __name__ == '__main__':
    app.run(debug=True)


