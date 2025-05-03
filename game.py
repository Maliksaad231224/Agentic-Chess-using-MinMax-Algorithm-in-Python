import chess
from Simple_Display import main_one_agent
from algorithm import play_min_maxN


main_one_agent(chess.Board(), play_min_maxN, chess.BLACK)
