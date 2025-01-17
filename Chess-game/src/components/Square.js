import React from "react";

function Square({ piece, isValidMove, onClick }) {
    const getPieceSymbol = (piece) => {
        const symbols = {
            wK: "♔",
            wQ: "♕",
            wR: "♖",
            wB: "♗",
            wN: "♘",
            wP: "♙",
            bK: "♚",
            bQ: "♛",
            bR: "♜",
            bB: "♝",
            bN: "♞",
            bP: "♟",
        };
        return symbols[piece] || "";
    };

    return (
        <div
            className={`square ${isValidMove ? "valid-move" : ""}`}
            onClick={onClick}
        >
            {getPieceSymbol(piece)}
        </div>
    );
}

export default Square;

