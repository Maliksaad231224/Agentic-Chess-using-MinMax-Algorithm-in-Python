
import chess
import pygame
import random
import math

X = 800
Y = 800
screen = pygame.display.set_mode((X, Y))
pygame.init()
# Original variable names with improved colors
WHITE = (255, 255, 255)       # Pure white (for pieces and text)
GREY = (200, 200, 200)        # Light grey for light squares (was 128,128,128)
YELLOW = (255, 255, 100)      # Brighter yellow for highlights (was 204,204,0)
BLUE = (100, 200, 255)        # Softer, brighter blue for legal moves (was 50,255,255)
BLACK = (50, 50, 50)  


b = chess.Board()
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
    # Draw chessboard squares with alternating colors
    for i in range(64):
        row = i // 8
        col = i % 8
        color = GREY if (row + col) % 2 == 0 else BLACK
        pygame.draw.rect(screen, color, (col*100, row*100, 100, 100))
    
    # Draw pieces
    for i in range(64):
        piece = board.piece_at(i)
        if piece:
            # Adjusted y-coordinate calculation for better piece centering
            x_pos = (i % 8) * 100 + (100 - PIECE_SIZE) // 2
            y_pos = (7 - i // 8) * 100 + (100 - PIECE_SIZE) // 2
            screen.blit(pieces[str(piece)], (x_pos, y_pos))
    
    # Draw grid lines (optional - can remove if using solid squares)
    for i in range(1, 8):
        pygame.draw.line(screen, WHITE, (0, i*100), (800, i*100), 2)
        pygame.draw.line(screen, WHITE, (i*100, 0), (i*100, 800), 2)
    
    pygame.display.flip()

def main(BOARD):
     #for human vs human game
    screen.fill(BLACK)
    pygame.display.set_caption('AI Powered Chess')

    index_moves = []
    status = True
    while(status):
        update(screen, BOARD)

        for event in pygame.event.get():
            if event.type ==pygame.QUIT:
                status = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                screen.fill(BLACK)
                #positio n of mouse
                pos = pygame.mouse.get_pos()
                #calculating clicked square's index
                 #divide x axis by 100 to get column number
                #divide y axis by 100 to get row number
                # rounds down to the nearest integer 
                square = (math.floor(pos[0]/100), math.floor(pos[1]/100))
                #calculate the row number from top. since origin is top-left, we need to invert the y- coordinates. by subtracting square[1] from 7 we get row number from top
                #*8 this multiplied row number by 8, calculating the starting index of row
                # + square[0] adds the column number to row starting index giving us index of square
                index = (7-square[1]*8+(square[0]))

                if index in index_moves:
                    move = moves[index_moves.index(index)]
                    BOARD.push(move)
                    index=None
                    index_moves = []

                else:
                    piece = BOARD.piece_at(index)  # checks if there is a piece on clicked square

                    if piece == None:
                        pass # on empty
                    else:
                        all_moves = list(BOARD.legal_moves)
                        moves = []
                        for m in all_moves:
                            if m.from_square == index:
                                moves.append(m)
                                #highlight legal squares
                                t = m.to_square
                                TX1 = 100*(t%8)
                                TY1 = 100*(7-t//8)

                                pygame.draw.rect(screen, BLUE, pygame.Rect(TX1, TY1, 100, 100),5)

                        index_moves = [a.to_square for a in moves]

        if BOARD.outcome() !=None:
            print(BOARD.outcome())
            status=False
            print(BOARD)
    pygame.quit()


def main_one_agent(BOARD,agent, agent_color):
    screen.fill(BLACK)
    pygame.display.set_caption('AI Chess')

    index_moves = []
    status = True
    while(status):
        update(screen, BOARD)

        if BOARD.turn == agent_color:
            BOARD.push(agent(BOARD))
            screen.fill(BLACK)
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    status = False
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    screen.fill(BLACK)

                    pos = pygame.mouse.get_pos()
                    square = (math.floor(pos[0]/100),math.floor(pos[1]/100))
                    index = (7-square[1])*8+(square[0])
                    
                    if index in index_moves:
                        move = moves[index_moves.index(index)]

                        BOARD.push(move)
                        index= None
                        index_moves = []
                    else:
                        piece = BOARD.piece_at(index)
                        if piece ==None:
                            pass
                        else:
                            all_moves = list(BOARD.legal_moves)
                            moves = []
                            for m in all_moves:
                                if m.from_square == index:
                                    moves.append(m)
                                    t = m.to_square
                                    TX1 = 100*(t%8)
                                    TY1 = 100*(t-t//8)
                                    pygame.draw.rect(screen, BLUE, pygame.Rect(TX1, TY1, 100,100),5)
                            
                            index_moves = [a.to_square for a in moves]

        if BOARD.outcome()!= None:
            print(BOARD.outcome())
            status = False
            print(BOARD)

    pygame.quit()
    

def main_two_agent(BOARD, agent1, agent_color1, agent2):
    screen.fill(BLACK)
    pygame.display.set_caption('Chess')
    status = True
    while(status):
        update(screen, BOARD)
        if BOARD.turn == agent_color1:
            BOARD.push(agent1(BOARD))

        else:
            BOARD.push(agent2(BOARD))
        
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                status = False
        
        if BOARD.outcome()!= None:
            print(BOARD.outcome())
            status=False
            print(BOARD)

    pygame.quit()




