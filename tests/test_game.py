import os
os.environ['SDL_VIDEODRIVER'] = 'dummy'
os.environ['SDL_AUDIODRIVER'] = 'dummy'

import unittest
from unittest.mock import patch
import chess
import pygame
import main
from bot import choose_move


class GameTests(unittest.TestCase):
    def test_bot_moves_are_legal_and_leave_board_unchanged(self):
        board = chess.Board()
        board.push_uci('e2e4')
        before = board.fen(), list(board.move_stack)
        for level in (1, 2, 3):
            self.assertIn(choose_move(board, level), board.legal_moves)
            self.assertEqual((board.fen(), list(board.move_stack)), before)

    def test_bot_finds_mate_and_stops_after_game(self):
        board = chess.Board('7k/5Q2/6K1/8/8/8/8/8 w - - 0 1')
        for level in (2, 3):
            move = choose_move(board, level)
            board.push(move)
            self.assertTrue(board.is_checkmate())
            self.assertIsNone(choose_move(board, level))
            board.pop()

    def test_square_mapping_in_both_orientations(self):
        for flipped in (False, True):
            for square in chess.SQUARES:
                self.assertEqual(main.square_at(main.square_rect(square, flipped).center, flipped), square)
        self.assertIsNone(main.square_at((10, 650)))

    def test_menu_duo_moves_and_return_to_menu(self):
        actions = [
            (pygame.MOUSEBUTTONDOWN, {'button': 1, 'pos': (400, 180)}),
            (pygame.MOUSEBUTTONDOWN, {'button': 1, 'pos': (300, 550)}),
            (pygame.MOUSEBUTTONDOWN, {'button': 1, 'pos': (360, 520)}),
            (pygame.MOUSEBUTTONDOWN, {'button': 1, 'pos': (360, 360)}),
            (pygame.KEYDOWN, {'key': pygame.K_u}),
            (pygame.KEYDOWN, {'key': pygame.K_m}),
            (pygame.QUIT, {}),
        ]
        def next_frame():
            if actions:
                event, attrs = actions.pop(0)
                pygame.event.post(pygame.event.Event(event, attrs))
        with patch.object(pygame.display, 'flip', side_effect=next_frame):
            main.main()
        self.assertFalse(actions)


if __name__ == '__main__':
    unittest.main()
