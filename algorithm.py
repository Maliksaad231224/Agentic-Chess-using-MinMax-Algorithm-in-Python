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

def min_maxN(BOARD, depth):
    moves = list(BOARD.legal_moves)
    scores = []

    for move in moves:
        temp = deepcopy(BOARD)
        temp.push(move)
        temp_best_move = most_value_agent(temp)  # Uses greedy agent for opponent
        temp.push(temp_best_move)
        scores.append(eval_board(temp))  # Only looks 2 plies ahead

    if BOARD.turn == True:
        best_move = moves[scores.index(max(scores))]
    else:
        best_move = moves[scores.index(min(scores))]
    
    return best_move
def play_min_maxN(board):
    if reader:
        try:
            entry = reader.get(board)
            if entry:
                return entry.move
        except ValueError as e:
            print(f"Error while accessing the opening book: {e}")
            pass

    best_move = min_maxN(board, 3)
    return best_move

