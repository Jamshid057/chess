"""Small local chess bot with bounded search; no external engine needed."""
import random
import time

import chess

VALUES = {chess.PAWN: 100, chess.KNIGHT: 320, chess.BISHOP: 330,
          chess.ROOK: 500, chess.QUEEN: 900, chess.KING: 0}


def evaluate(board):
    score = 0
    for square, piece in board.piece_map().items():
        centrality = 7 - abs(3.5 - chess.square_file(square)) - abs(3.5 - chess.square_rank(square))
        bonus = centrality * (8 if piece.piece_type in (chess.KNIGHT, chess.BISHOP) else 2)
        value = VALUES[piece.piece_type] + bonus
        score += value if piece.color == board.turn else -value
    return score


def choose_move(board, level):
    """Return a legal move, or None for a finished game. Work on a board copy."""
    if board.is_game_over(claim_draw=True):
        return None
    moves = list(board.legal_moves)
    if level == 1:
        return random.choice(moves)
    deadline = time.monotonic() + (0.3 if level == 2 else 1.0)

    def search(depth, alpha, beta, ply):
        if time.monotonic() >= deadline:
            raise TimeoutError
        if board.is_checkmate():
            return -100000 + ply
        if board.is_game_over(claim_draw=True):
            return 0
        if depth == 0:
            return evaluate(board)
        best = -float('inf')
        ordered = sorted(board.legal_moves,
                         key=lambda m: (bool(m.promotion), board.is_capture(m)), reverse=True)
        for move in ordered:
            board.push(move)
            try:
                value = -search(depth - 1, -beta, -alpha, ply + 1)
            finally:
                board.pop()
            best = max(best, value)
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return best

    random.shuffle(moves)
    best_move = moves[0]
    for depth in range(1, (2 if level == 2 else 4) + 1):
        iteration_move = best_move
        best_score = -float('inf')
        try:
            for move in moves:
                board.push(move)
                try:
                    score = -search(depth - 1, -float('inf'), -best_score, 1)
                finally:
                    board.pop()
                if score > best_score:
                    best_score = score
                    iteration_move = move
        except TimeoutError:
            break
        best_move = iteration_move
        moves.remove(best_move)
        moves.insert(0, best_move)
    return best_move
