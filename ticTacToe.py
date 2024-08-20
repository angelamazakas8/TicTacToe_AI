
import pygame
import numpy as np
from gameStatus import GameStatus
from multiAgents import minimax, negamax
import sys, random


class RandomBoardTicTacToe:
    def __init__(self, size=(300, 400)):
        # Initialize the game window and other parameters
        self.size = self.width, self.height = size
        # Define some colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GREEN = (0, 255, 0)
        self.RED = (255, 0, 0)
        self.BLUE = (30, 144, 255)
        self.GREY = (192, 192, 192)
        self.RELAXING_PURPLE = (149, 107, 169)
        self.DARK_PURPLE = (48, 25, 52)
        self.GOLD = (255, 215, 0)
        self.TROMBONE_YELLOW = (210, 181, 91)
        self.CELADON_GREEN = (172, 225, 175)

        self.grid_size = 3
        self.MARGIN = 4

        self.WIDTH = self.size[0] / self.grid_size - self.MARGIN
        self.HEIGHT = self.size[0] / self.grid_size - self.MARGIN

        self.game_mode = "pvp"
        self.algorithm_mode = "minimax"
        self.final_score = 0


        self.game_reset()

    def draw_game(self):
        # Create a 2-dimensional array using the column and row variables
        pygame.init()
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption("Tic Tac Toe - X's turn")
        self.screen.fill(self.DARK_PURPLE)
        # Draw the grid

        for row in range(self.grid_size):
            for col in range(self.grid_size):
                # Get the x and y coordinates of the current grid location
                x = col * (self.WIDTH - 2 + self.MARGIN) + self.MARGIN
                y = row * (self.HEIGHT - 2 + self.MARGIN) + self.MARGIN
                # Draw the rectangle for the current grid location
                pygame.draw.rect(self.screen, self.RELAXING_PURPLE, (x, y, self.WIDTH, self.HEIGHT))

        # Adding a font
        font = pygame.font.SysFont("Arial", 15)

        # draw UI buttons
        self.reset_selection_rect = pygame.Rect(self.width - 77, self.height - 92, 65, 35)
        pygame.draw.rect(self.screen, self.TROMBONE_YELLOW, self.reset_selection_rect)
        text_reset = font.render("Reset", True, self.BLACK)
        text_reset_rect = text_reset.get_rect(center=self.reset_selection_rect.center)
        self.screen.blit(text_reset, text_reset_rect)

        # vbv = five by five, 5x5 grid selection button
        self.vbv_selection_rect = pygame.Rect(self.width - 147, self.height - 92, 65, 35)
        pygame.draw.rect(self.screen, self.TROMBONE_YELLOW, self.vbv_selection_rect)
        text_vbv = font.render("5X5", True, self.BLACK)
        text_vbv_rect = text_vbv.get_rect(center=self.vbv_selection_rect.center)
        self.screen.blit(text_vbv, text_vbv_rect)

        # fbf = four by four, 4x4 grid selection button
        self.fbf_selection_rect = pygame.Rect(self.width - 217, self.height - 92, 65, 35)
        pygame.draw.rect(self.screen, self.TROMBONE_YELLOW, self.fbf_selection_rect)
        text_fbf = font.render("4X4", True, self.BLACK)
        text_fbf_rect = text_fbf.get_rect(center=self.fbf_selection_rect.center)
        self.screen.blit(text_fbf, text_fbf_rect)

        # tbt = three by three, 3x3 grid selection button
        self.tbt_selection_rect = pygame.Rect(self.width - 287, self.height - 92, 65, 35)
        pygame.draw.rect(self.screen, self.TROMBONE_YELLOW, self.tbt_selection_rect)
        text_tbt = font.render("3X3", True, self.BLACK)
        text_tbt_rect = text_tbt.get_rect(center=self.tbt_selection_rect.center)
        self.screen.blit(text_tbt, text_tbt_rect)

        # negamax algorithm selection button
        self.negamax_selection_rect = pygame.Rect(self.width - 77, self.height - 48, 65, 35)
        pygame.draw.rect(self.screen, self.TROMBONE_YELLOW, self.negamax_selection_rect)
        text_negamax = font.render("Negamax", True, self.BLACK)
        text_negamax_rect = text_negamax.get_rect(center=self.negamax_selection_rect.center)
        self.screen.blit(text_negamax, text_negamax_rect)

        # minimax algorithm selection button
        self.minimax_selection_rect = pygame.Rect(self.width - 147, self.height - 48, 65, 35)
        pygame.draw.rect(self.screen, self.TROMBONE_YELLOW, self.minimax_selection_rect)
        text_minimax = font.render("Minimax", True, self.BLACK)
        text_minimax_rect = text_minimax.get_rect(center=self.minimax_selection_rect.center)
        self.screen.blit(text_minimax, text_minimax_rect)

        # pvai = Player versus AI, this is a game mode selection button
        self.pvai_selection_rect = pygame.Rect(self.width - 217, self.height - 48, 65, 35)
        pygame.draw.rect(self.screen, self.TROMBONE_YELLOW, self.pvai_selection_rect)
        text_pvai = font.render("P vs AI", True, self.BLACK)
        text_pvai_rect = text_pvai.get_rect(center=self.pvai_selection_rect.center)
        self.screen.blit(text_pvai, text_pvai_rect)

        # pvp = Player versus Player, this is a game mode selection button
        self.pvp_selection_rect = pygame.Rect(self.width - 287, self.height - 48, 65, 35)
        pygame.draw.rect(self.screen, self.TROMBONE_YELLOW, self.pvp_selection_rect)
        text_pvp = font.render("P vs P", True, self.BLACK)
        text_pvp_rect = text_pvp.get_rect(center=self.pvp_selection_rect.center)
        self.screen.blit(text_pvp, text_pvp_rect)

        pygame.display.update()

    def change_turn(self):

        if (self.game_state.turn_O):
            pygame.display.set_caption("Tic Tac Toe - O's turn")
        else:
            pygame.display.set_caption("Tic Tac Toe - X's turn")

    def draw_circle(self, x, y):
        # Get the x and y coordinates of the center of the circle
        cx = (self.WIDTH + self.MARGIN) * (x + 0.5)
        cy = (self.HEIGHT + self.MARGIN) * (y + 0.5)

        # radius, with offset
        radius = min(self.WIDTH, self.HEIGHT) / 3 - self.MARGIN

        # Draw a circle at the specified position
        # 3 is pixel size of width
        pygame.draw.circle(self.screen, self.GOLD, (int(cx), int(cy)), int(radius), 3)
        pygame.display.update()

    def draw_cross(self, x, y):
        # Calculate the coordinates for drawing the cross
        cx1 = x * (self.WIDTH + self.MARGIN) + self.MARGIN + self.WIDTH / 4
        cy1 = y * (self.HEIGHT + self.MARGIN) + self.MARGIN + self.HEIGHT / 4
        cx2 = x * (self.WIDTH + self.MARGIN) + self.MARGIN + self.WIDTH * 3 / 4
        cy2 = y * (self.HEIGHT + self.MARGIN) + self.MARGIN + self.HEIGHT * 3 / 4

        # Draw the cross
        pygame.draw.line(self.screen, self.CELADON_GREEN, (cx1, cy1), (cx2, cy2), 3)
        pygame.draw.line(self.screen, self.CELADON_GREEN, (cx1, cy2), (cx2, cy1), 3)

        pygame.display.update()

    def is_game_over(self):
        return self.game_state.is_terminal()

    def move(self, move):
        self.game_state = self.game_state.get_new_state(move)


    def play_ai(self):

        total_temp_set = []
        for i in range(len(self.game_state.board_state)):
            temp_set = []
            for j in range(len(self.game_state.board_state)):
                temp = self.game_state.board_state[i][j]
                temp_set.append(temp)
            total_temp_set.append(temp_set)
        temp_game = GameStatus(total_temp_set, False)

        if self.algorithm_mode == "minimax":
            value, best_move = minimax(temp_game, 5, temp_game.turn_O)
        else:
            value, best_move = negamax(temp_game, 3, temp_game.turn_O)
        print(self.game_state.board_state)


        # ai plays move (either minimax or negamax algorithm), draws circle
        row = best_move[0]
        col = best_move[1]
        self.change_turn()
        self.move((row, col))
        self.draw_circle(col, row)
        pygame.display.update()

    def game_reset(self):
        initial_board_state = [[0 for i in range(self.grid_size)] for j in range(self.grid_size)]
        self.game_state = GameStatus(initial_board_state, True)
        pygame.display.set_caption("Tic Tac Toe - X's turn")
        self.WIDTH = self.size[0] / self.grid_size - self.MARGIN
        self.HEIGHT = self.size[0] / self.grid_size - self.MARGIN
        self.draw_game()
        pygame.display.update()

    def play_game(self):
        done = False
        self.draw_game()

        while not done:
            for event in pygame.event.get():  # User did something
                if event.type == pygame.QUIT:
                    done = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()

                    # find approximate column from mouse's x coordinate
                    col = pos[0] // (self.WIDTH + self.MARGIN)

                    # make sure approximated column is not outside of largest possible index
                    # self.GRID_SIZE-1 gives largest possible index
                    col = min(col, self.grid_size - 1)

                    # convert to integer
                    col = int(col)

                    # find approximate row from mouse's y coordinate
                    row = pos[1] // (self.HEIGHT + self.MARGIN)

                    # make sure approximated row is not outside of largest possible index
                    row = min(row, self.grid_size - 1)

                    # convert to integer
                    row = int(row)

                    if self.reset_selection_rect.collidepoint(pos):
                        self.game_reset()
                    elif self.vbv_selection_rect.collidepoint(pos):
                        if self.grid_size != 5:
                            self.grid_size = 5
                            self.game_reset()
                    elif self.fbf_selection_rect.collidepoint(pos):
                        if self.grid_size != 4:
                            self.grid_size = 4
                            self.game_reset()
                    elif self.tbt_selection_rect.collidepoint(pos):
                        if self.grid_size != 3:
                            self.grid_size = 3
                            self.game_reset()
                    elif self.negamax_selection_rect.collidepoint(pos):
                        if self.algorithm_mode != "negamax":
                            self.algorithm_mode = "negamax"
                            self.game_reset()
                    elif self.minimax_selection_rect.collidepoint(pos):
                        if self.algorithm_mode != "minimax":
                            self.algorithm_mode = "minimax"
                            self.game_reset()
                    elif self.pvai_selection_rect.collidepoint(pos):
                        if self.game_mode != "pvai":
                            self.game_mode = "pvai"
                            self.game_reset()
                    elif self.pvp_selection_rect.collidepoint(pos):
                        if self.game_mode != "pvp":
                            self.game_mode = "pvp"
                            self.game_reset()
                    else:
                        if self.game_mode == "pvp":
                            if self.game_state.board_state[row][col] == 0 and self.game_state.turn_O:
                                # if empty, place move down on board
                                self.change_turn()
                                self.move((row, col))
                                self.draw_cross(col, row)
                            elif self.game_state.board_state[row][col] == 0 and not self.game_state.turn_O:
                                self.change_turn()
                                self.move((row, col))
                                self.draw_circle(col, row)
                        else:
                            if self.game_state.board_state[row][col] == 0 and self.game_state.turn_O:
                                # if empty, place move down on board, this uses the player's
                                # turn, and now it is the AI's turn
                                self.change_turn()
                                self.move((row, col))
                                self.draw_cross(col, row)

                                # AI uses their turn to make a move, and this function should set
                                # the turn back to the player
                                if not self.is_game_over():
                                    pygame.time.wait(random.randint(500, 3000))
                                    self.play_ai()

                    if self.is_game_over():
                        score_font = pygame.font.SysFont("Arial", 30)
                        message = self.game_state.determine_winner()

                        text = score_font.render(message, True, self.BLACK)
                        text_rect = text.get_rect(center=(self.width // 2, self.height // 2 - 50))
                        self.screen.blit(text, text_rect)
                        pygame.display.update()

            pygame.display.update()

        pygame.quit()


tictactoegame = RandomBoardTicTacToe()
tictactoegame.play_game()
