"""Bot va Duo rejimli Pygame shaxmat. Ishga tushirish: python main.py."""

import chess
import pygame
from concurrent.futures import ThreadPoolExecutor

from bot import choose_move

CELL = 80
BOARD_SIZE = CELL * 8
HEIGHT = BOARD_SIZE + 100
LIGHT = (238, 218, 181)
DARK = (151, 112, 79)
SYMBOLS = {
    "K": "♔", "Q": "♕", "R": "♖", "B": "♗", "N": "♘", "P": "♙",
    "k": "♚", "q": "♛", "r": "♜", "b": "♝", "n": "♞", "p": "♟",
}
PROMOTIONS = (chess.QUEEN, chess.ROOK, chess.BISHOP, chess.KNIGHT)


def square_at(pos, flipped=False):
    x, y = pos
    if 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE:
        file, rank = x // CELL, 7 - y // CELL
        return chess.square(7 - file, 7 - rank) if flipped else chess.square(file, rank)
    return None


def square_rect(square, flipped=False):
    if flipped:
        square = 63 - square
    return pygame.Rect(chess.square_file(square) * CELL,
                       (7 - chess.square_rank(square)) * CELL, CELL, CELL)


def status(board):
    outcome = board.outcome(claim_draw=True)
    if outcome:
        if outcome.winner is None:
            return "Durang!"
        winner = "Oq" if outcome.winner == chess.WHITE else "Qora"
        return f"{winner} g'alaba qozondi!"
    turn = "Oq" if board.turn == chess.WHITE else "Qora"
    return f"Navbat: {turn}" + (" — Shoh!" if board.is_check() else "")


def main():
    pygame.init()
    screen = pygame.display.set_mode((BOARD_SIZE, HEIGHT))
    pygame.display.set_caption("Shaxmat — Bot va Duo")
    font = pygame.font.SysFont("dejavusans,arial,helvetica", 22)
    piece_font = pygame.font.SysFont("apple symbols,segoe ui symbol,dejavusans", 62)
    clock = pygame.time.Clock()
    board = chess.Board()
    selected = None
    promotion_moves = []
    running = True
    menu = True
    mode = "bot"
    level = 2
    human_color = chess.WHITE
    generation = 0
    executor = ThreadPoolExecutor(max_workers=1)
    pending = None
    pending_generation = None

    def button(label, rect, active=False):
        pygame.draw.rect(screen, (70, 133, 95) if active else (65, 72, 85), rect, border_radius=10)
        text = font.render(label, True, (250, 250, 250))
        screen.blit(text, text.get_rect(center=rect.center))

    def reset_game():
        nonlocal selected, promotion_moves, generation
        board.reset()
        selected = None
        promotion_moves = []
        generation += 1

    def draw_piece(piece, rect):
        # Some systems lack a chess-symbol font; use letters as a fallback.
        symbol = SYMBOLS[piece.symbol()]
        if not piece_font.metrics(symbol)[0]:
            symbol = piece.symbol().upper()
        color = (250, 250, 250) if piece.color else (25, 25, 25)
        shadow = piece_font.render(symbol, True, (70, 60, 50))
        label = piece_font.render(symbol, True, color)
        dest = label.get_rect(center=rect.center)
        screen.blit(shadow, dest.move(1, 2))
        screen.blit(label, dest)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    menu = True
                    selected = None
                    promotion_moves = []
                    generation += 1
                    continue
                if menu:
                    continue
                if event.key == pygame.K_ESCAPE:
                    selected = None
                    promotion_moves = []
                elif event.key == pygame.K_r:
                    reset_game()
                elif event.key == pygame.K_u:
                    if board.move_stack:
                        board.pop()
                        if mode == "bot" and board.turn != human_color and board.move_stack:
                            board.pop()
                    generation += 1
                    selected = None
                    promotion_moves = []
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if menu:
                    for i, value in enumerate(("bot", "duo")):
                        if pygame.Rect(100 + i * 230, 160, 210, 55).collidepoint(event.pos):
                            mode = value
                    if mode == "bot":
                        for i in range(3):
                            if pygame.Rect(70 + i * 170, 280, 160, 55).collidepoint(event.pos):
                                level = i + 1
                        for i, value in enumerate((chess.WHITE, chess.BLACK)):
                            if pygame.Rect(100 + i * 230, 400, 210, 55).collidepoint(event.pos):
                                human_color = value
                    if pygame.Rect(170, 520, 300, 60).collidepoint(event.pos):
                        reset_game()
                        menu = False
                    continue
                if mode == "bot" and board.turn != human_color:
                    continue
                if promotion_moves:
                    for i, piece_type in enumerate(PROMOTIONS):
                        rect = pygame.Rect(160 + i * CELL, 280, CELL, CELL)
                        if rect.collidepoint(event.pos):
                            move = next(m for m in promotion_moves if m.promotion == piece_type)
                            board.push(move)
                            selected = None
                            promotion_moves = []
                            break
                    continue
                if board.is_game_over(claim_draw=True):
                    continue
                target = square_at(event.pos, mode == "bot" and human_color == chess.BLACK)
                if target is None:
                    continue
                moves = [m for m in board.legal_moves
                         if m.from_square == selected and m.to_square == target]
                if moves:
                    if moves[0].promotion:
                        promotion_moves = moves
                    else:
                        board.push(moves[0])
                        selected = None
                else:
                    piece = board.piece_at(target)
                    selected = target if piece and piece.color == board.turn else None

        screen.fill((35, 39, 46))
        if pending is not None and pending.done():
            move = pending.result()
            if (pending_generation == generation and not menu and mode == "bot"
                    and board.turn != human_color and move in board.legal_moves
                    and not board.is_game_over(claim_draw=True)):
                board.push(move)
            pending = None
        if menu:
            screen.blit(font.render("SHAXMAT — o'yin sozlamalari", True, (245, 245, 245)), (140, 70))
            button("Bot bilan", pygame.Rect(100, 160, 210, 55), mode == "bot")
            button("Duo (2 kishi)", pygame.Rect(330, 160, 210, 55), mode == "duo")
            if mode == "bot":
                screen.blit(font.render("Qiyinlik darajasi", True, LIGHT), (70, 245))
                for i, label in enumerate(("1: Oson", "2: O'rtacha", "3: Qiyin")):
                    button(label, pygame.Rect(70 + i * 170, 280, 160, 55), level == i + 1)
                screen.blit(font.render("Sizning tomoningiz", True, LIGHT), (100, 365))
                button("Oq", pygame.Rect(100, 400, 210, 55), human_color == chess.WHITE)
                button("Qora", pygame.Rect(330, 400, 210, 55), human_color == chess.BLACK)
            button("O'yinni boshlash", pygame.Rect(170, 520, 300, 60), True)
            pygame.display.flip()
            clock.tick(60)
            continue
        bot_turn = mode == "bot" and board.turn != human_color and not board.is_game_over(claim_draw=True)
        if running and bot_turn and pending is None:
            pending_generation = generation
            pending = executor.submit(choose_move, board.copy(), level)
        last_move = board.peek() if board.move_stack else None
        destinations = {m.to_square for m in board.legal_moves if m.from_square == selected}
        for square in chess.SQUARES:
            rect = square_rect(square, mode == "bot" and human_color == chess.BLACK)
            color = LIGHT if (chess.square_file(square) + chess.square_rank(square)) % 2 else DARK
            pygame.draw.rect(screen, color, rect)
            if last_move and square in (last_move.from_square, last_move.to_square):
                pygame.draw.rect(screen, (211, 188, 91), rect)
            if square == selected:
                pygame.draw.rect(screen, (111, 169, 104), rect)
            if board.is_check() and square == board.king(board.turn):
                pygame.draw.rect(screen, (210, 90, 85), rect)
            piece = board.piece_at(square)
            if piece:
                draw_piece(piece, rect)
            if square in destinations:
                if piece:
                    pygame.draw.circle(screen, (55, 115, 70), rect.center, 35, 4)
                else:
                    pygame.draw.circle(screen, (55, 115, 70), rect.center, 10)
        caption = status(board) + ("  Bot o'ylayapti..." if bot_turn else "")
        screen.blit(font.render(caption, True, (245, 245, 245)), (16, BOARD_SIZE + 12))
        screen.blit(font.render("R: yangi   U: qaytarish   M: menyu   Esc: bekor",
                                True, (190, 195, 205)), (16, BOARD_SIZE + 51))
        if promotion_moves:
            overlay = pygame.Surface((BOARD_SIZE, BOARD_SIZE), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 170))
            screen.blit(overlay, (0, 0))
            screen.blit(font.render("Piyoda uchun dona tanlang:", True, (255, 255, 255)), (160, 240))
            for i, piece_type in enumerate(PROMOTIONS):
                rect = pygame.Rect(160 + i * CELL, 280, CELL, CELL)
                pygame.draw.rect(screen, LIGHT, rect)
                pygame.draw.rect(screen, DARK, rect, 2)
                draw_piece(chess.Piece(piece_type, board.turn), rect)
        pygame.display.flip()
        clock.tick(60)
    executor.shutdown(wait=False, cancel_futures=True)
    pygame.quit()


if __name__ == "__main__":
    main()
