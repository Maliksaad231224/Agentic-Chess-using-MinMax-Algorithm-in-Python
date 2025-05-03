import chess
import pygame
import random
import math

X = 800
Y = 800
screen = pygame.display.set_mode((X, Y))
pygame.init()

# Colors
WHITE = (255, 255, 255)
GREY = (200, 200, 200)
YELLOW = (255, 255, 100)
BLUE = (100, 200, 255)
BLACK = (50, 50, 50)

PIECE_SIZE = 100

def load_and_scale_piece(path):
    try:
        piece = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(piece, (PIECE_SIZE, PIECE_SIZE))
    except:
        print(f"Error loading image: {path}")
        surface = pygame.Surface((PIECE_SIZE, PIECE_SIZE))
        surface.fill((255, 0, 0))
        return surface

pieces = {
    'p': load_and_scale_piece('images/black_pawn.png'),
    'n': load_and_scale_piece('images/black_knight.png'),
    'b': load_and_scale_piece('images/black_bishop.png'),
    'r': load_and_scale_piece('images/black_rook.png'),
    'q': load_and_scale_piece('images/black_queen.png'),
    'k': load_and_scale_piece('images/black_king.png'),
    'P': load_and_scale_piece('images/white_pawn.png'),
    'N': load_and_scale_piece('images/white_knight.png'),
    'B': load_and_scale_piece('images/white_bishop.png'),
    'R': load_and_scale_piece('images/white_rook.png'),
    'Q': load_and_scale_piece('images/white_queen.png'),
    'K': load_and_scale_piece('images/white_king.png'),
}

def update(screen, board):
    for i in range(64):
        row = i // 8
        col = i % 8
        color = GREY if (row + col) % 2 == 0 else BLACK
        pygame.draw.rect(screen, color, (col*100, row*100, 100, 100))
    for i in range(64):
        piece = board.piece_at(i)
        if piece:
            x_pos = (i % 8) * 100 + (100 - PIECE_SIZE) // 2
            y_pos = (7 - i // 8) * 100 + (100 - PIECE_SIZE) // 2
            screen.blit(pieces[str(piece)], (x_pos, y_pos))
    for i in range(1, 8):
        pygame.draw.line(screen, WHITE, (0, i*100), (800, i*100), 2)
        pygame.draw.line(screen, WHITE, (i*100, 0), (i*100, 800), 2)
    pygame.display.flip()

def main_one_agent(board, agent, agent_color):
    screen.fill(BLACK)
    pygame.display.set_caption('AI Chess')
    index_moves = []
    status = True
    while status:
        update(screen, board)
        if board.turn == agent_color:
            board.push(agent(board))
            screen.fill(BLACK)
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    status = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    screen.fill(BLACK)
                    pos = pygame.mouse.get_pos()
                    square = (math.floor(pos[0]/100), math.floor(pos[1]/100))
                    index = (7 - square[1]) * 8 + square[0]
                    if index in index_moves:
                        move = moves[index_moves.index(index)]
                        board.push(move)
                        index = None
                        index_moves = []
                    else:
                        piece = board.piece_at(index)
                        if piece:
                            all_moves = list(board.legal_moves)
                            moves = []
                            for m in all_moves:
                                if m.from_square == index:
                                    moves.append(m)
                                    t = m.to_square
                                    TX1 = 100 * (t % 8)
                                    TY1 = 100 * (7 - t // 8)
                                    pygame.draw.rect(screen, BLUE, pygame.Rect(TX1, TY1, 100, 100), 5)
                            index_moves = [a.to_square for a in moves]
        if board.outcome():
            print(board.outcome())
            status = False
            print(board)
    pygame.quit()
