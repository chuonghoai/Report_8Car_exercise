from collections import deque
import heapq
import math
import random
from copy import deepcopy

N = 8

def run(choosed, n=N):
    if choosed == "BFS": return BFS(n)
    elif choosed == "DFS": return DFS(n)
    elif choosed == "UCS": return UCS(n)
    elif choosed == "DLS": return DLS(n)
    elif choosed == "IDS": return IDS(n)
    elif choosed == "Greedy": return greedy(n)
    elif choosed == "A*": return Astar(n)
    elif choosed == "Hill - Climbing": return HillClimbing(n)
    elif choosed == "Simulated Annealing": 
        path = None
        while path is None:
            path, process = SimulatedAnnealing(n)
        return path, process
    elif choosed == "Genetic Algorithm": return geneticAlgorithm(n)
    elif choosed == "Beam Search": return beam(n)
    elif choosed == "AND-OR Tree Search": 
        _path, process = AndOrTreeSearch(n)
        path = extractPath(_path)
        return path, process
    elif choosed == "Belief State Search": return beliefSearch(n)
    elif choosed == "Partially Observable Spaces": return POS_algorithm(n)
    elif choosed == "Backtracking": return backtrackingAlgorithm(n)
    elif choosed == "Forward Checking": return forwardCheckingAlgorithm(n)
    elif choosed == "AC-3": return AC3(n)
    return None, None

# Hàm ước tính chi phí heuritic = 2*n - số hàng và cột đã đặt
def heuristic(path, n=8):
    row = {r for r, _ in path}
    col = {c for _, c in path}
    return (n - len(row)) + (n - len(col))

# Hàm tính chi phí hiện tại = số quân xe đã đặt
def CalCost(path):
    return len(path)

# Hàm tính số xung đột  = số cặp quân xe xung đột
def costConflict(state):
    n = len(state)
    conflicts = 0
    for i in range(n):
        for j in range(i + 1, n):
            if state[i] == state[j]:
                conflicts += 1
    return conflicts

# Hàm tạo trạng thái con ngẫu nhiên
def createChildRandom(state, n):
    child = state[:]
    row = random.randint(0, n - 1)
    possible_cols = [c for c in range(n) if c != child[row]]
    child[row] = random.choice(possible_cols)
    return child

# Hàm lấy trạng thái cuối cùng của AND-OR tree search
def extractPath(plan):
    state = []
    while plan:
        _, outcomes = plan[0]
        state_next, subplan = outcomes[0]
        state = state_next
        plan = subplan
    return state

# Tìm các cột đang trống
def free_col(state, n=N):
    used = set(state)
    return [c for c in range(n) if c not in used]
    
# Tạo trạng thái ngẫu nhiên
def random_state(n=N):
        return [random.randint(0, n - 1) for _ in range(n)]
# 1. BFS
def BFS(n=8):
    process = []
    q = deque([([], 0)])
    while q:
        pos, row = q.popleft()
        process.append(pos)
        if row == n:
            return pos, process
        
        used_col = set(pos)
        for col in range(n):
            if col not in used_col:
                new_pos = pos + [col]
                q.append((new_pos, row + 1))
    return None, process

# 2. DFS
def DFS(n=8, visible_mode=False, startState=None):
    if startState is None:
        startState = []
    process = []

    def dfs(state, row=0):
        process.append(state[:])
        if len(state) == n:
            return state
        if any(r == row for r, _ in state):
            return dfs(state, row + 1)
        for col in range(n):
            if all(r != row and c != col for r, c in state):
                state.append((row, col))
                result = dfs(state, row + 1)
                if result:
                    return result
                state.pop()
        return None
    
    result = dfs(startState)
    return result, process

# 3. UCS
def UCS(n=8):
    frontier = []
    heapq.heappush(frontier, (CalCost([]), []))
    process = []

    while frontier:
        cost, path = heapq.heappop(frontier)
        process.append(path.copy())

        if len(path) == n:
            print(len(process))
            return path, process

        row = len(path)
        for col in range(n):
            conflict = any(col == c for r, c in path)
            if not conflict:
                new_path = path + [(row, col)]
                heapq.heappush(frontier, (CalCost(new_path), new_path))
    return [], process

# 4. IDL
def DLS(n=8, limit=8):
    process = []

    def recursive(path, depth):
        process.append(path.copy())  # lưu trạng thái hiện tại
        if len(path) == n:  # đủ 8 quân
            return path
        elif depth == 0:
            return "cutoff"
        row = len(path)
        cutoff_occurred = False
        for col in range(n):
            # kiểm tra xung đột với các quân đã đặt
            conflict = any(col == c for r, c in path)
            if not conflict:
                child_path = path + [(row, col)]
                result = recursive(child_path, depth - 1)
                if result == "cutoff":
                    cutoff_occurred = True
                elif result is not False:
                    return result
        if cutoff_occurred:
            return "cutoff"
        else:
            return False

    path = recursive([], limit)
    return path, process

# 5. IDS
def IDS(n=8, maxDepth=10):
    totalProcess = []
    for depth in range(1, maxDepth + 1):
        path, process = DLS(n, limit=depth)
        totalProcess.extend(process)
        if path != "cutoff" and path is not False:
            return path, totalProcess
    return None, totalProcess

# 6. Greedy
def greedy(n=8):
    process = []
    start_path = []  # path rỗng ban đầu
    start_h = heuristic(start_path, n)
    queue = [(start_h, start_path)]  # heap: (heuristic, path)

    while queue:
        _, path = heapq.heappop(queue)
        # process.append(path.copy())
        if len(path) == n:
            return path, process
        row = len(path)
        for col in range(n):
            conflict = any(col == c for r, c in path)
            if not conflict:
                new_path = path + [(row, col)]
                h = heuristic(new_path, n)
                process.append(new_path.copy())
                heapq.heappush(queue, (h, new_path))
    return [], process

# 7. A*
def Astar(n=8):
    process = []
    start_path = []
    start_cost = CalCost(start_path)
    start_heur = heuristic(start_path, n)
    start_f = start_cost + start_heur
    queue = [(start_f, start_path)]
    
    while queue:
        _, path = heapq.heappop(queue)
        process.append(path.copy())
        if len(path) == n:
            return path, process
        row = len(path)
        for col in range(n):
            conflict = any(col == c for r, c in path)
            if not conflict:
                new_path = path + [(row, col)]
                g = CalCost(new_path)
                h = heuristic(new_path, n)
                f = g + h
                heapq.heappush(queue, (f, new_path))
    return [], process

# 8. Hill Climbing
def HillClimbing(n=8):
    path = []       # path hiện tại
    process = []     # danh sách các ô (row, col) đã thử

    for row in range(n):
        best_col = None
        best_cost = float('inf')

        for col in range(n):
            tempPath = path + [col]
            cost = costConflict(tempPath)
            process.append(tempPath)  # lưu ô đang thử

            if cost < best_cost:
                best_cost = cost
                best_col = col

        path.append(best_col)

    return path, process

# 9. Simulated Annealing
def SimulatedAnnealing(n=8, T=1000, T_min=1, alpha=0.95):
    state = [random.randint(0, n - 1) for _ in range(n)]
    cost = costConflict(state)
    process = []

    while T > T_min:
        process.append(state[:])
        if cost == 0:
            return state, process
        child = createChildRandom(state, n)
        child_cost = costConflict(child)
        delta = child_cost - cost
        if delta <= 0:
            state = child
            cost = child_cost
        else:
            if random.random() < math.exp(-delta / T):
                state = child
                cost = child_cost
        T *= alpha
    return None, process

# 10. Genetic Algorithm
def geneticAlgorithm(n=8, pop_size=100, generations=500, mutate_rate=0.1):
    def select_parent(population, k=3):
        participants = random.sample(population, k)
        participants.sort(key=lambda s: costConflict(s))
        return participants[0]

    def crossover(p1, p2):
        point = random.randint(1, n - 1)
        c1 = p1[:point] + p2[point:]
        c2 = p2[:point] + p1[point:]
        return c1, c2

    def mutate(state):
        for i in range(n):
            if random.random() < mutate_rate:
                state[i] = random.randint(0, n - 1)

    population = [random_state() for _ in range(pop_size)]
    process = []  # lưu tất cả state được duyệt

    for _ in range(generations):
        # lưu tất cả cá thể của thế hệ hiện tại
        process.extend(population)

        # chọn best hiện tại
        population.sort(key=lambda s: costConflict(s))
        best = population[0]

        # nếu tìm thấy nghiệm không xung đột
        if costConflict(best) == 0:
            process.append(best[:])
            return best, process

        # tạo thế hệ mới
        new_pop = []
        while len(new_pop) < pop_size:
            p1, p2 = select_parent(population), select_parent(population)
            c1, c2 = crossover(p1, p2)
            mutate(c1)
            mutate(c2)
            new_pop.extend([c1, c2])
        population = new_pop[:pop_size]

    return None, process

# 11. Beam Search
def beam(n=8, k=5, max_loop=200):
    beam = [(random_state(), None) for _ in range(k)]
    beam = [(state, costConflict(state)) for state, _ in beam]
    process = []

    for _ in range(max_loop):
        beam.sort(key=lambda x: x[1])
        best_state, best_cost = beam[0]
        process.extend([s for s, _ in beam[::-1]])
        if best_cost == 0:
            return best_state, process

        neighbors = []
        for state, _ in beam:
            for row in range(n):
                for col in range(n):
                    if state[row] == col:
                        continue
                    new_state = state[:]
                    new_state[row] = col
                    neighbors.append((new_state, costConflict(new_state)))

        # chọn k trạng thái tốt nhất
        neighbors.sort(key=lambda x: x[1])
        beam = neighbors[:k]

    return None, process

# 12. AND-OR tree search
def AndOrTreeSearch(n=8):
    process = []

    def or_search(state, path):
        process.append(state[:])

        if len(state) == n:
            return []

        # tránh lặp vòng
        if state in path:
            return None

        for col in free_col(state):
            child = [state + [col]]
            plan = and_search(child, path + [state])
            if plan is not None:
                return [(col, plan)]
        return None

    def and_search(states, path):
        plans = []
        for s in states:
            plan = or_search(s, path)
            if plan is None:
                return None
            plans.append((s, plan))
        return plans

    plan = or_search([], [])
    return plan, process

# 13. Belief State Search
def beliefSearch(n=8):
    def random_start_state(n):
        n_stage = random.randint(1, max(1, n // 2))
        start_state = []
        for _ in range(n_stage):
            n_num = random.randint(0, max(1, n // 2))
            state = [random.randint(0, n - 1) for _ in range(n_num)]
            start_state.append(state)
        return start_state
    
    list_start_state = random_start_state(n)
    if not list_start_state:
        list_state = [[]]
    else:
        list_state = [s for s in list_start_state if costConflict(s) == 0]

    process = []

    while list_state:
        new_list_state = []
        for state in list_state:
            process.append(state[:])

            if len(state) == n:
                return state, process

            for col in free_col(state, n):
                child = state + [col]
                if costConflict(child) == 0:
                    new_list_state.append(child)
                    break

        list_state = new_list_state

    return None, process

# 14. Belief State Search
def POS_algorithm(n=8):
    def random_visible_from_goal():
        n_visible = random.randint(1, 2)
        visible = []
        for _ in range(n_visible):
            row = random.randint(0, n - 1)
            col = random.randint(0, n - 1)
            if all(r != row and c != col for r, c in visible):
                visible.append((row, col))
        return visible
    
    visibleState = random_visible_from_goal()
    return DFS(n=n, visible_mode=True, startState=visibleState)

# 15. Backtracking
def backtrackingAlgorithm(n=8):
    process = []
    
    def backtracking(state, row):
        process.append(state[:])
        if len(state) == n:
            return state
        for col in range(n):
            if all((c != col and r != row) for r, c in state):
                state.append((row, col))
                rs = backtracking(state, row + 1)
                if rs is None:
                    state.pop()
                else:
                    return rs
        return None

    return backtracking([], 0), process

# 16. Forward Checking
def forwardCheckingAlgorithm(n=8):
    process = []
    
    def forwardChecking(state, row, domain):
        process.append(state[:])
        if len(state) == n:
            return state
        if row >= n:
            return None
        
        for col in list(domain[row]):
            new_domain = {r: set(cols) for r, cols in domain.items()}
            state.append((row, col))
        
            for r in range(row + 1, n):
                if col in new_domain[r]:
                    new_domain[r].remove(col)
        
            if any(len(new_domain[r]) == 0 for r in range(row + 1, n)):
                state.pop()
                continue
        
            rs = forwardChecking(state, row + 1, new_domain)
            if rs is None:
                state.pop()
            else:
                return rs
        return None
    
    domain = {r: set(range(n)) for r in range(n)}
    return forwardChecking([], 0, domain), process

# AC-3
def AC3(n=8):
    process = []

    variable = list(range(n))
    domains = {Xi: list(range(n)) for Xi in variable}
    neighbors = {Xi: [Xj for Xj in variable if Xj != Xi] for Xi in variable}
    
    def constraint(Xi, x, Xj, y):
        return x != y

    def revise(Xi, Xj):
        revised = False
        for x in domains[Xi][:]:
            if not any(constraint(Xi, x, Xj, y) for y in domains[Xj]):
                domains[Xi].remove(x)
                revised = True
        return revised

    queue = deque([(Xi, Xj) for Xi in variable for Xj in neighbors[Xi]])

    while queue:
        Xi, Xj = queue.popleft()
        if revise(Xi, Xj):
            if not domains[Xi]:
                return [], process
            for Xk in neighbors[Xi]:
                if Xk != Xj:
                    queue.append((Xk, Xi))

    def backtracking(state, row):
        process.append(state[:])
        if len(state) == n:
            return state

        for col in domains[row]:
            if all((c != col and r != row) for r, c in state):
                state.append((row, col))
                rs = backtracking(state, row + 1)
                if rs is None:
                    state.pop()
                else:
                    return rs
        return None

    path = backtracking([], 0)
    return path, process