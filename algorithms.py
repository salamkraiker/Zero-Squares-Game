import time
from collections import deque
from heapq import heappush, heappop


def find_path_to_goal(state, start, goal):
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    queue = deque([(start, None)])
    visited = set()
    parent_map = {}
    nodes_visited = 0

    start_time = time.time()

    while queue:
        current, parent = queue.popleft()

        if current in visited:
            continue

        visited.add(current)
        print(f"Visited node: {current}")

        nodes_visited += 1
        parent_map[current] = parent

        if current == goal:
            end_time = time.time()
            elapsed_time = end_time - start_time

            path = []
            while current is not None:
                path.append(current)
                current = parent_map[current]

            return path[::-1], nodes_visited, elapsed_time

        for dr, dc in directions:
            next_pos = current
            goal_reached = False

            while True:
                next_step = (next_pos[0] + dr, next_pos[1] + dc)

                if (0 <= next_step[0] < state.quadrats.size and
                        0 <= next_step[1] < state.quadrats.size and
                        state.quadrats.get_square(next_step[0], next_step[1]).type != "fixed"):
                    next_pos = next_step

                    if next_pos == goal:
                        goal_reached = True
                        break
                else:
                    break

            if next_pos != current:
                print(f"From {current}, can reach {next_pos}")
                if goal_reached:
                    print(f"Goal reached at {next_pos}")
                    parent_map[next_pos] = current
                    path = []
                    while next_pos is not None:
                        path.append(next_pos)
                        next_pos = parent_map[next_pos]
                    end_time = time.time()
                    elapsed_time = end_time - start_time
                    return path[::-1], nodes_visited, elapsed_time
                queue.append((next_pos, current))

    end_time = time.time()
    elapsed_time = end_time - start_time
    return None, nodes_visited, elapsed_time


def bfs( state,start, goal):
    path, nodes_visited, elapsed_time = find_path_to_goal(state, start, goal)
    if path:
        print("Path to goal:", path)
        print("Nodes visited:", nodes_visited)
        print("Elapsed time (seconds):", elapsed_time)
        return path, nodes_visited, elapsed_time
    else:
        print("No path found to the goal.")
        print("Nodes visited:", nodes_visited)
        print("Elapsed time (seconds):", elapsed_time)
        return None, nodes_visited, elapsed_time




def dfs_find_path_to_goal(state, start, goal):
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    stack = [(start, None)]
    visited = set()
    parent_map = {}
    nodes_visited = 0

    start_time = time.time()

    while stack:
        current, parent = stack.pop()

        if current in visited:
            continue

        visited.add(current)
        print(f"Visited node: {current}")

        nodes_visited += 1
        parent_map[current] = parent

        if current == goal:
            end_time = time.time()
            elapsed_time = end_time - start_time

            path = []
            while current is not None:
                path.append(current)
                current = parent_map[current]

            return path[::-1], nodes_visited, elapsed_time

        for dr, dc in directions:
            next_pos = current
            goal_reached = False

            while True:
                next_step = (next_pos[0] + dr, next_pos[1] + dc)

                if (0 <= next_step[0] < state.quadrats.size and
                        0 <= next_step[1] < state.quadrats.size and
                        state.quadrats.get_square(next_step[0], next_step[1]).type != "fixed"):
                    next_pos = next_step

                    if next_pos == goal:
                        goal_reached = True
                        break
                else:
                    break

            if next_pos != current:
                print(f"From {current}, can reach {next_pos}")
                if goal_reached:
                    print(f"Goal reached at {next_pos}")
                    parent_map[next_pos] = current
                    path = []
                    while next_pos is not None:
                        path.append(next_pos)
                        next_pos = parent_map[next_pos]
                    end_time = time.time()
                    elapsed_time = end_time - start_time
                    return path[::-1], nodes_visited, elapsed_time
                stack.append((next_pos, current))

    end_time = time.time()
    elapsed_time = end_time - start_time
    return None, nodes_visited, elapsed_time


def dfs(state, start, goal):
    path, nodes_visited, elapsed_time = dfs_find_path_to_goal(state,start, goal)
    if path:
        print("Path to goal:", path)
        print("Nodes visited:", nodes_visited)
        print("Elapsed time (seconds):", elapsed_time)
        return path, nodes_visited, elapsed_time
    else:
        print("No path found to the goal.")
        print("Nodes visited:", nodes_visited)
        print("Elapsed time (seconds):", elapsed_time)
        return None, nodes_visited, elapsed_time


def ucs_find_path_to_goal(self, start, goal):
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    priority_queue = []
    heappush(priority_queue, (0, start, None))
    visited = set()
    parent_map = {}
    cost_map = {start: 0}

    nodes_visited = 0
    start_time = time.time()

    while priority_queue:
        current_cost, current, parent = heappop(priority_queue)

        if current in visited:
            continue

        visited.add(current)
        print(f"Visited node: {current} with cost: {current_cost}")

        nodes_visited += 1
        parent_map[current] = parent

        if current == goal:
            end_time = time.time()
            elapsed_time = end_time - start_time

            path = []
            while current is not None:
                path.append(current)
                current = parent_map[current]

            return path[::-1], nodes_visited, elapsed_time

        for dr, dc in directions:
            next_pos = current
            goal_reached = False

            while True:
                next_step = (next_pos[0] + dr, next_pos[1] + dc)

                if (0 <= next_step[0] < self.quadrats.size and
                        0 <= next_step[1] < self.quadrats.size and
                        self.quadrats.get_square(next_step[0], next_step[1]).type != "fixed"):
                    next_pos = next_step

                    if next_pos == goal:
                        goal_reached = True
                        break
                else:
                    break

            if next_pos != current:
                print(f"From {current}, can reach {next_pos}")
                if goal_reached:
                    print(f"Goal reached at {next_pos}")
                    parent_map[next_pos] = current
                    path = []
                    while next_pos is not None:
                        path.append(next_pos)
                        next_pos = parent_map[next_pos]
                    end_time = time.time()
                    elapsed_time = end_time - start_time
                    return path[::-1], nodes_visited, elapsed_time
                heappush(priority_queue,
                         (current_cost + 1, next_pos, current))

    end_time = time.time()
    elapsed_time = end_time - start_time
    return None, nodes_visited, elapsed_time


def a_star_find_path_to_goal(state, start, goal):
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    def heuristic(node, goal):
        # Assuming node and goal are tuples (row, col)
        return abs(node[0] - goal[0]) + abs(node[1] - goal[1])

    priority_queue = []
    heappush(priority_queue, (heuristic(start, goal), 0, start, None))
    visited = set()
    parent_map = {}
    g_cost_map = {start: 0}

    nodes_visited = 0
    start_time = time.time()

    while priority_queue:
        f_cost, g_cost, current, parent = heappop(priority_queue)

        if current in visited:
            continue

        visited.add(current)
        print(f"Visited node: {current} with f_cost: {f_cost}, g_cost: {g_cost}")

        nodes_visited += 1
        parent_map[current] = parent

        if current == goal:
            end_time = time.time()
            elapsed_time = end_time - start_time

            # Reconstruct path
            path = []
            while current is not None:
                path.append(current)
                current = parent_map[current]

            return path[::-1], nodes_visited, elapsed_time

        for dr, dc in directions:
            next_pos = current
            goal_reached = False

            while True:
                next_step = (next_pos[0] + dr, next_pos[1] + dc)

                if (0 <= next_step[0] < state.quadrats.size and
                        0 <= next_step[1] < state.quadrats.size and
                        state.quadrats.get_square(next_step[0], next_step[1]).type != "fixed"):
                    next_pos = next_step

                    if next_pos == goal:
                        goal_reached = True
                        break
                else:
                    break

            if next_pos != current:
                print(f"From {current}, can reach {next_pos}")
                if goal_reached:
                    print(f"Goal reached at {next_pos}")
                    parent_map[next_pos] = current
                    path = []
                    while next_pos is not None:
                        path.append(next_pos)
                        next_pos = parent_map[next_pos]
                    end_time = time.time()
                    elapsed_time = end_time - start_time
                    return path[::-1], nodes_visited, elapsed_time
                heappush(priority_queue, (g_cost + 1 + heuristic(next_pos, goal), g_cost + 1, next_pos, current))

    end_time = time.time()
    elapsed_time = end_time - start_time
    return None, nodes_visited, elapsed_time


def heuristic(self, current, goal):
    return abs(current[0] - goal[0]) + abs(current[1] - goal[1])


def simple_ascent_hill_climbing(self, start, goal):
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # up, down, left, right
    current = start
    visited = set()
    parent_map = {}
    nodes_visited = 0  # Counter for visited nodes
    start_time = time.time()  # Start timing

    while current != goal:
        visited.add(current)
        nodes_visited += 1

        best_neighbor = None
        best_value = float('-inf')  # Best heuristic value (We maximize this)

        for dr, dc in directions:
            next_pos = (current[0] + dr, current[1] + dc)

            if (0 <= next_pos[0] < self.quadrats.size and
                    0 <= next_pos[1] < self.quadrats.size and
                    self.quadrats.get_square(next_pos[0], next_pos[1]).type != "fixed" and
                    next_pos not in visited):

                value = self.heuristic(next_pos, goal)  # Heuristic value for the next position

                if value > best_value:
                    best_value = value
                    best_neighbor = next_pos

        if best_neighbor is None:
            end_time = time.time()
            elapsed_time = end_time - start_time
            return None, nodes_visited, elapsed_time  # No path found

        # Move to the best neighbor
        parent_map[best_neighbor] = current
        current = best_neighbor

    # Backtrack to reconstruct the path
    path = []
    while current is not None:
        path.append(current)
        current = parent_map[current]

    end_time = time.time()
    elapsed_time = end_time - start_time
    return path[::-1], nodes_visited, elapsed_time  # Reverse the path to start -> goal


def steepest_ascent_hill_climbing(state, start, goal):
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    current = start
    visited = set()
    parent_map = {}
    nodes_visited = 0
    start_time = time.time()

    while current != goal:
        visited.add(current)
        nodes_visited += 1

        best_neighbor = None
        best_value = float('-inf')  # Best heuristic value (We maximize this)

        for dr, dc in directions:
            next_pos = (current[0] + dr, current[1] + dc)

            if (0 <= next_pos[0] < state.quadrats.size and
                    0 <= next_pos[1] < state.quadrats.size and
                    state.quadrats.get_square(next_pos[0], next_pos[1]).type != "fixed" and
                    next_pos not in visited):

                value = state.heuristic(next_pos, goal)

                if value > best_value:
                    best_value = value
                    best_neighbor = next_pos

        if best_neighbor is None:
            end_time = time.time()
            elapsed_time = end_time - start_time
            return None, nodes_visited, elapsed_time

        parent_map[best_neighbor] = current
        current = best_neighbor

    path = []
    while current is not None:
        path.append(current)
        current = parent_map[current]

    end_time = time.time()
    elapsed_time = end_time - start_time
    return path[::-1], nodes_visited, elapsed_time
