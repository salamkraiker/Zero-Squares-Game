
import json
from algorithms import *
from game_logic import *
from screens import *

# إعدادات عامة
SQUARE_SIZE = 50
WHITE = (255, 255, 255)
COLOR_MAP = {
    "RED2": (255, 0, 0),
    "CYAN_GREEN": (0, 255, 255),
    "GREEN": (0, 255, 0),
    "GRAY": (105, 105, 105),
    "BLUE": (0, 0, 255),
    "PINK": (255, 105, 180),
    "ORANGE": (255, 165, 0),
    "YELLOW": (255, 255, 0)
}

def load_levels_from_json(file_path):
    with open(file_path, "r") as file:
        data = json.load(file)
    return data["levels"]

def main():
    pygame.init()

    levels = load_levels_from_json("levels.json")

    while True:
        action = show_start_screen()
        if action == "start_game":
            play_game(levels[0])
        elif action == "select_level":
            chosen_level = select_level_screen()
            level_data = levels[chosen_level]
            play_game(level_data)

def play_game(level_data):
    grid = Quadrats(level_data["grid_size"])

    for fixed in level_data["fixed_squares"]:
        x, y = fixed
        grid.set_quadrat(x, y, Quadrat("fixed", COLOR_MAP["GRAY"]))

    for movable in level_data["movable_squares"]:
        x, y = movable["position"]
        color = COLOR_MAP[movable["color"]]
        grid.set_quadrat(x, y, Quadrat("movable", color))

    for goal in level_data["goals"]:
        x, y = goal["position"]
        color = COLOR_MAP[goal["color"]]
        grid.set_goal(x, y, "goal", color)

    state = State(grid)
    print("Initial Grid:")
    grid.print_grid()
    state.print_all_available_moves()

    print("__________________________")

    selected_algorithm = input(
        "Select algorithm (1 for A* / 2 for BFS / 3 for DFS / 4 for UCS / 5 for Simple Ascent Hill Climbing / 6 for Steepest Ascent Hill Climbing): "
    ).strip()

    if selected_algorithm == "1":
        selected_algorithm = "a_star"
    elif selected_algorithm == "2":
        selected_algorithm = "bfs"
    elif selected_algorithm == "3":
        selected_algorithm = "dfs"
    elif selected_algorithm == "4":
        selected_algorithm = "ucs"
    elif selected_algorithm == "5":
        selected_algorithm = "simple_ascent_hill_climbing"
    elif selected_algorithm == "6":
        selected_algorithm = "steepest_ascent_hill_climbing"
    else:
        print("Invalid input, defaulting to A*.")
        selected_algorithm = "a_star"

    for movable in level_data["movable_squares"]:
        start = tuple(movable["position"])
        color = movable["color"]

        goal = next(
            (tuple(g["position"]) for g in level_data["goals"] if g["color"] == color),
            None
        )

        path = None
        nodes_visited = None
        elapsed_time = None

        if goal:
            if selected_algorithm == "a_star":
                path, nodes_visited, elapsed_time = a_star_find_path_to_goal(state ,start, goal)
            elif selected_algorithm == "bfs":
                path, nodes_visited, elapsed_time = find_path_to_goal(state,start, goal)
            elif selected_algorithm == "dfs":
                path, nodes_visited, elapsed_time = dfs_find_path_to_goal(state,start, goal)
            elif selected_algorithm == "ucs":
                path, nodes_visited, elapsed_time = ucs_find_path_to_goal(state,start, goal)
            elif selected_algorithm == "simple_ascent_hill_climbing":
                path, nodes_visited, elapsed_time = simple_ascent_hill_climbing(state,start, goal)
            elif selected_algorithm == "steepest_ascent_hill_climbing":
                path, nodes_visited, elapsed_time = steepest_ascent_hill_climbing(state,start, goal)

            if path:
                print(f"{selected_algorithm.capitalize()} Path to goal:", path)
                print("Nodes visited:", nodes_visited)
                print("Elapsed time (seconds):", elapsed_time)
            else:
                print(f"No path found using {selected_algorithm.capitalize()}.")

    screen = pygame.display.set_mode((grid.size * SQUARE_SIZE, grid.size * SQUARE_SIZE))
    pygame.display.set_caption("Zero Squares Game")

    running = True
    game_won = False

    while running:
        screen.fill(WHITE)
        grid.draw_quadrat(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and not game_won:
                for x, y in grid.selected_squares:
                    if event.key == pygame.K_UP:
                        state.move_quadrat(x, y, "up")
                    elif event.key == pygame.K_DOWN:
                        state.move_quadrat(x, y, "down")
                    elif event.key == pygame.K_LEFT:
                        state.move_quadrat(x, y, "left")
                    elif event.key == pygame.K_RIGHT:
                        state.move_quadrat(x, y, "right")
                grid = state.quadrats

        if not game_won and state.check_win_condition():
            print("You've won!")
            game_won = True
            running = False

        pygame.display.flip()

if __name__ == "__main__":
    main()
