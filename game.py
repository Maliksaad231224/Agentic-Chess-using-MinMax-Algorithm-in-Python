import chess
from Simple_Display import main, main_one_agent, main_two_agent
from algorithm import random_agent, most_value_agent, min_maxN, play_min_maxN

# Run AI vs AI game
main_one_agent(chess.Board(), play_min_maxN, chess.BLACK)