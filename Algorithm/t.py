from collections import deque

def ac3(variables, domains, constraints):
    """
    Thuật toán AC-3 để thực thi tính nhất quán cung.
    """
    process_log = []
    queue = deque(list(constraints))
    process_log.append(f"Hàng đợi ban đầu: {list(queue)}")

    while queue:
        (xi, xj) = queue.popleft()
        process_log.append(f"\nĐang xử lý cung: ({xi}, {xj})")
        
        if revise(domains, xi, xj, process_log):
            if not domains[xi]:
                process_log.append(f"Miền của {xi} trống. Không có lời giải.")
                return False, process_log
            
            neighbors = [neighbor for neighbor in variables if neighbor != xi and (neighbor, xi) in constraints]
            for xk in neighbors:
                if (xk, xi) not in queue:
                    queue.append((xk, xi))
                    process_log.append(f"Miền của {xi} đã thay đổi. Thêm cung ({xk}, {xi}) vào hàng đợi.")
    
    process_log.append("\nAC-3 hoàn thành. Các miền giá trị đã nhất quán.")
    return True, process_log

def revise(domains, xi, xj, process_log):
    """
    Hàm trợ giúp cho AC-3 để sửa đổi miền của xi.
    """
    revised = False
    for x in list(domains[xi]):
        # Nếu không có giá trị nào trong miền của xj cho phép (x, y) thỏa mãn ràng buộc
        if not any(x != y for y in domains[xj]):
            domains[xi].remove(x)
            revised = True
            process_log.append(f"Loại bỏ giá trị {x} khỏi miền của {xi} vì không có giá trị hỗ trợ trong {xj}.")
    return revised

def backtracking_search(variables, domains, constraints, assignment):
    """
    Thuật toán quay lui để tìm một lời giải.
    """
    if len(assignment) == len(variables):
        return assignment

    var = [v for v in variables if v not in assignment][0]

    for value in domains[var]:
        assignment[var] = value
        if is_consistent(var, value, assignment, constraints):
            result = backtracking_search(variables, domains, constraints, assignment)
            if result:
                return result
        del assignment[var]
    
    return None

def is_consistent(var, value, assignment, constraints):
    """
    Kiểm tra xem một giá trị có nhất quán với các phép gán hiện tại không.
    """
    for assigned_var, assigned_value in assignment.items():
        if var != assigned_var and value == assigned_value:
            return False
    return True

if __name__ == '__main__':
    # Thiết lập bài toán 8 quân xe
    num_rooks = 8
    variables = [f'R{i+1}' for i in range(num_rooks)]
    domains = {var: set(range(1, num_rooks + 1)) for var in variables}
    
    constraints = []
    for i in range(len(variables)):
        for j in range(i + 1, len(variables)):
            constraints.append((variables[i], variables[j]))
            constraints.append((variables[j], variables[i]))

    # Chạy AC-3
    is_solvable, process = ac3(variables, domains.copy(), constraints)

    print("--- QUÁ TRÌNH CỦA THUẬT TOÁN AC-3 ---")
    for step in process:
        print(step)

    print("\n--- MIỀN GIÁ TRỊ SAU KHI CHẠY AC-3 ---")
    for var, domain in domains.items():
        print(f"{var}: {sorted(list(domain))}")

    # Tìm một lời giải bằng backtracking
    print("\n--- TÌM MỘT LỜI GIẢI (PATH) BẰNG BACKTRACKING ---")
    solution_path = backtracking_search(variables, domains, constraints, {})
    
    if solution_path:
        print("Một lời giải đã được tìm thấy:")
        # Sắp xếp theo tên biến để hiển thị có thứ tự
        sorted_solution = sorted(solution_path.items())
        for var, value in sorted_solution:
            print(f"Quân xe ở cột {var[1:]} được đặt ở hàng {value}")
        
        print("\nBiểu diễn trên bàn cờ:")
        board = [['.' for _ in range(num_rooks)] for _ in range(num_rooks)]
        for var, value in sorted_solution:
            col = int(var[1:]) - 1
            row = value - 1
            board[row][col] = 'R'
        
        for row in board:
            print(' '.join(row))
    else:
        print("Không tìm thấy lời giải.")