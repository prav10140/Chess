import React, { useState } from "react";
import Square from "./Square";

const initialBoard = [
    ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
    ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
    ["--", "--", "--", "--", "--", "--", "--", "--"],
    ["--", "--", "--", "--", "--", "--", "--", "--"],
    ["--", "--", "--", "--", "--", "--", "--", "--"],
    ["--", "--", "--", "--", "--", "--", "--", "--"],
    ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
    ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
];

function Chessboard() {
    const [board, setBoard] = useState(initialBoard);
    const [selectedPiece, setSelectedPiece] = useState(null);
    const [validMoves, setValidMoves] = useState([]);

    const handleSquareClick = (row, col) => {
        if (selectedPiece) {
            // Move the selected piece
            const newBoard = [...board];
            newBoard[row][col] = newBoard[selectedPiece.row][selectedPiece.col];
            newBoard[selectedPiece.row][selectedPiece.col] = "--";
            setBoard(newBoard);
            setSelectedPiece(null);
            setValidMoves([]);
        } else {
            // Select a piece and show valid moves
            setSelectedPiece({ row, col });
            setValidMoves([
                [row + 1, col],
                [row - 1, col],
            ]);
        }
    };

    return (
        <div className="chessboard">
            {board.map((row, rowIndex) =>
                row.map((piece, colIndex) => (
                    <Square
                        key={`${rowIndex}-${colIndex}`}
                        piece={piece}
                        isValidMove={validMoves.some(
                            ([r, c]) => r === rowIndex && c === colIndex
                        )}
                        onClick={() => handleSquareClick(rowIndex, colIndex)}
                    />
                ))
            )}
        </div>
    );
}

export default Chessboard;

