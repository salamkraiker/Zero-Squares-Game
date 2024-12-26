from collections import deque
from heapq import heappush, heappop

import pygame
import copy
from time import time
import time
# إعداداتي العامة
WHITE = (255, 255, 255)
GRAY = (105, 105, 105)
CYAN_GREEN = (0, 255, 255)
RED2 = (255, 4, 190)
BLACK = (0, 0, 0)
SQUARE_SIZE = 50
GRID_SIZE = 7


class Quadrat:
    def __init__(self, type, color=WHITE):
        self.color = color
        self.type = type

class Quadrats:
    def __init__(self, n):
        self.size = n
        self.quadrats = [[Quadrat("empty", WHITE) for _ in range(n)] for _ in range(n)]
        self.selected_squares = []
        self.goals = {}
        self.goal_colors = {}

    def get_square(self, x, y):
            if 0 <= x < self.size and 0 <= y < self.size:
                return self.quadrats[x][y]
            return None

    def set_quadrat(self, x, y, quadrat):
        if 0 <= x < self.size and 0 <= y < self.size:
            self.quadrats[x][y] = quadrat
            if quadrat.type == "movable":
                self.selected_squares.append((x, y))

    def set_goal(self, x, y, goal_id, goal_color):
        if 0 <= x < self.size and 0 <= y < self.size:
            self.goals[(x, y)] = goal_id
            self.goal_colors[(x, y)] = goal_color

    def draw_quadrat(self, screen):
        for i in range(self.size):
            for j in range(self.size):
                rect = pygame.Rect(j * SQUARE_SIZE, i * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                quadrat = self.quadrats[i][j]

                if quadrat.type == "movable":
                    color = quadrat.color
                elif quadrat.type == "fixed":
                    color = GRAY
                else:
                    color = WHITE

                pygame.draw.rect(screen, color, rect)
                pygame.draw.rect(screen, BLACK, rect, 1)

                if quadrat.type != "movable":
                    for (goal_pos, goal_id) in self.goals.items():
                        if (i, j) == goal_pos:
                            goal_color = self.goal_colors.get(goal_pos, WHITE)
                            pygame.draw.rect(screen, goal_color, rect, 3)

    def print_grid(self):
        for i, row in enumerate(self.quadrats):
            line = "  "
            for j, quadrat in enumerate(row):
                if (i, j) in self.goals:
                    line += " G "
                elif quadrat.type == "movable":
                    line += " M "
                elif quadrat.type == "empty":
                    line += " 0 "
                elif quadrat.type == "fixed":
                    line += " # "
            print(line)
        print("\n")

class State:
    def __init__(self, quadrats):
        self.quadrats = copy.deepcopy(quadrats)
        self.game_won = False
        self.movable_squares = self.get_movable_squares()
        self.completed_goals = []
        self.path = []

    def heuristic(self, current, goal):
        return abs(current[0] - goal[0]) + abs(current[1] - goal[1])

    def get_movable_squares(self):
                movable = []
                for x in range(self.quadrats.size):
                    for y in range(self.quadrats.size):
                        square = self.quadrats.get_square(x, y)
                        if square and square.type == "movable":
                            movable.append((x, y))
                return movable

    def can_move(self, x, y, direction):
        if not (0 <= x < self.quadrats.size and 0 <= y < self.quadrats.size):
            return False

        if self.quadrats.quadrats[x][y].type != "movable":
            return False

        dx, dy = 0, 0
        if direction == "up":
            dx, dy = -1, 0
        elif direction == "down":
            dx, dy = 1, 0
        elif direction == "left":
            dx, dy = 0, -1
        elif direction == "right":
            dx, dy = 0, 1


        new_x, new_y = x + dx, y + dy
        if not (0 <= new_x < self.quadrats.size and 0 <= new_y < self.quadrats.size):
            return False

        next_quadrat = self.quadrats.quadrats[new_x][new_y]
        if next_quadrat.type == "empty" or (new_x, new_y) in self.quadrats.goals:
            if (new_x, new_y) not in self.quadrats.selected_squares:

                adjacent_x, adjacent_y = x + 1 * dx, y + 1 * dy
                if 0 <= adjacent_x < self.quadrats.size and 0 <= adjacent_y < self.quadrats.size:
                    adjacent_quadrat = self.quadrats.quadrats[adjacent_x][adjacent_y]
                    if adjacent_quadrat.type == "movable":
                        return False
                return True
        return False


    def get_available_moves(self, x, y):
        if not (0 <= x < self.quadrats.size and 0 <= y < self.quadrats.size):
            return []

        if self.quadrats.quadrats[x][y].type != "movable":
            return []

        available_moves = []
        for direction in ["up", "down", "left", "right"]:
            if self.can_move(x, y, direction):
                available_moves.append(direction)

        print(f"Available moves for square at ({x}, {y}): {available_moves}")
        return available_moves

    def print_all_available_moves(self):
        visited = set()
        for x, y in self.quadrats.selected_squares:
            if (x, y) not in visited:
                self.get_available_moves(x, y)
                visited.add((x, y))


    def check_win_condition(self):
        if self.game_won:
            print("Game won!")
            return True

        completed_goals = []
        for (x, y) in self.quadrats.selected_squares:
            if (x, y) in self.quadrats.goals:
                goal_color = self.quadrats.goal_colors.get((x, y), WHITE)
                square_color = self.quadrats.quadrats[x][y].color
                if square_color == goal_color:
                    if (x, y) not in completed_goals:
                        completed_goals.append((x, y))

        if not completed_goals:
            return False

        for (x, y) in completed_goals:
            if (x, y) in self.quadrats.goals:
                del self.quadrats.goals[(x, y)]
            if (x, y) in self.quadrats.goal_colors:
                del self.quadrats.goal_colors[(x, y)]
            if (x, y) in self.quadrats.selected_squares:
                self.quadrats.quadrats[x][y] = Quadrat("empty", WHITE)
                self.quadrats.selected_squares.remove((x, y))

        if not self.quadrats.goals:
            self.game_won = True
            return True

        return False

    def move_quadrat(self, x, y, direction):
        if not self.can_move(x, y, direction):
            return False

        dx, dy = 0, 0
        if direction == "up":
            dx, dy = -1, 0
        elif direction == "down":
            dx, dy = 1, 0
        elif direction == "left":
            dx, dy = 0, -1
        elif direction == "right":
            dx, dy = 0, 1

        new_positions = []
        for square in self.quadrats.selected_squares:
            current_x, current_y = square
            new_x, new_y = current_x, current_y

            if self.can_move(current_x, current_y, direction):
                while (0 <= new_x + dx < self.quadrats.size and
                       0 <= new_y + dy < self.quadrats.size):
                    next_x, next_y = new_x + dx, new_y + dy

                    if (next_x, next_y) in self.quadrats.goals:
                        goal_color = self.quadrats.goal_colors.get((next_x, next_y), WHITE)
                        square_color = self.quadrats.quadrats[current_x][current_y].color
                        if square_color == goal_color:
                            if any((sq_x, sq_y) == (next_x, next_y) for (sq_x, sq_y) in self.quadrats.selected_squares):
                                break
                            else:
                                new_x, new_y = next_x, next_y
                                break
                        else:
                            if not any((sq_x, sq_y) == (next_x, next_y) for (sq_x, sq_y) in
                                       self.quadrats.selected_squares):
                                new_x, new_y = next_x, next_y
                            else:
                                break

                    elif self.quadrats.quadrats[next_x][next_y].type == "empty":
                        new_x, new_y = next_x, next_y
                    else:
                        break

            if (new_x, new_y) != (current_x, current_y):
                new_positions.append((current_x, current_y, new_x, new_y))

        for current_x, current_y, new_x, new_y in new_positions:
            if (new_x, new_y) != (current_x, current_y):
                self.quadrats.quadrats[new_x][new_y] = Quadrat("movable", self.quadrats.quadrats[current_x][current_y].color)
                self.quadrats.quadrats[current_x][current_y] = Quadrat("empty", WHITE)
                self.quadrats.selected_squares.remove((current_x, current_y))
                self.quadrats.selected_squares.append((new_x, new_y))

        if self.check_win_condition():
            return True

        print("Grid after move:")
        self.quadrats.print_grid()
        self.print_all_available_moves()
        print("________________________")

        return False

    def move(self, direction):
        new_quadrats = copy.deepcopy(self.quadrats)

        for square in new_quadrats.selected_squares:
            current_x, current_y = square

            if direction == "up":
                new_x, new_y = current_x - 1, current_y
            elif direction == "down":
                new_x, new_y = current_x + 1, current_y
            elif direction == "left":
                new_x, new_y = current_x, current_y - 1
            elif direction == "right":
                new_x, new_y = current_x, current_y + 1

            if 0 <= new_x < new_quadrats.size and 0 <= new_y < new_quadrats.size:
                if new_quadrats.quadrats[new_x][new_y].type == "empty" or \
                        (new_x, new_y) in new_quadrats.goals:
                    symbol = new_quadrats.quadrats[current_x][current_y].color
                    new_quadrats.quadrats[new_x][new_y] = Quadrat("movable", symbol)
                    new_quadrats.quadrats[current_x][current_y] = Quadrat("empty", WHITE)

                    new_quadrats.selected_squares.remove((current_x, current_y))
                    new_quadrats.selected_squares.append((new_x, new_y))

        return State(new_quadrats)


