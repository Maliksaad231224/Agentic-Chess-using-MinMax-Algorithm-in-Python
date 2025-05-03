import chess
import random
from copy import deepcopy
import chess.polyglot


try:
    reader = chess.polyglot.open_reader('baron30.bin')
except FileNotFoundError:
    reader = None
    print("Opening book 'baron30.bin' not found. Proceeding without it.")
except ValueError as e:
    print(f"Error loading opening book: {e}")
    reader = None


scoring = {
    'p': -1,
    'n': -3,
    'b': -3,
    'r': -5,
    'q': -9,
    'k': 0,
    'P': 1,
    'N': 3,
    'B': 3,
    'R': 5,
    'Q': 9,
    'K': 0,
}

def eval_space(board):
    no_moves = len(list(board.legal_moves))
    value = no_moves / (20 + no_moves)
    return value if board.turn else -value

def eval_board(board):
    score = 0
    pieces = board.piece_map()
    for key in pieces:
        score += scoring.get(str(pieces[key]), 0)
    score += eval_space(board)
    return score

def random_agent(board):
    return random.choice(list(board.legal_moves))

def most_value_agent(board):
    moves = list(board.legal_moves)
    best_score = None
    best_move = None
    for move in moves:
        temp = deepcopy(board)
        temp.push(move)
        score = eval_board(temp)
        if best_score is None or (board.turn and score > best_score) or (not board.turn and score < best_score):
            best_score = score
            best_move = move
    return best_move

def min_maxN(board, depth):
    if depth == 0 or board.is_game_over():
        return eval_board(board), None

    moves = list(board.legal_moves)
    best_score = None
    best_move = None

    for move in moves:
        temp = deepcopy(board)
        temp.push(move)

        if temp.is_checkmate():
            return 1000, move

        if temp.is_stalemate() or temp.is_insufficient_material():
            score = 0
        else:
            score, _ = min_maxN(temp, depth - 1)

        if best_score is None or (board.turn and score > best_score) or (not board.turn and score < best_score):
            best_score = score
            best_move = move

    return best_score, best_move if depth == 3 else best_score

def play_min_maxN(board):
    if reader:
        try:
            entry = reader.get(board)
            if entry:
                return entry.move
        except ValueError as e:
            print(f"Error while accessing the opening book: {e}")
            pass

    _, best_move = min_maxN(board, 3)
    return best_move