import numpy as np
import random
import matplotlib.pyplot as plt
from typing import List, Tuple, Optional

class AntColonyTSP:
    """
    Giải thuật Đàn Kiến cho bài toán Người Du lịch (TSP)
    """
    
    def __init__(self, cities: List[Tuple[float, float]], 
                 n_ants: int = 10, 
                 alpha: float = 1.0, 
                 beta: float = 2.0, 
                 rho: float = 0.1, 
                 q: float = 100.0,
                 max_iterations: int = 100):
        """
        Khởi tạo thuật toán ACO
        
        Args:
            cities: Danh sách tọa độ các thành phố [(x1,y1), (x2,y2), ...]
            n_ants: Số lượng kiến
            alpha: Trọng số của pheromone
            beta: Trọng số của thông tin heuristic
            rho: Tỷ lệ bay hơi pheromone
            q: Hằng số để tính pheromone
            max_iterations: Số vòng lặp tối đa
        """
        self.cities = np.array(cities)
        self.n_cities = len(cities)
        self.n_ants = n_ants
        self.alpha = alpha
        self.beta = beta
        self.rho = rho
        self.q = q
        self.max_iterations = max_iterations
        
        # Tính ma trận khoảng cách
        self.distances = self._calculate_distance_matrix()
        
        # Khởi tạo ma trận pheromone
        self.pheromones = np.ones((self.n_cities, self.n_cities)) * 0.1
        
        # Lưu trữ kết quả tốt nhất
        self.best_path = None
        self.best_distance = float('inf')
        self.distance_history = []
    
    def _calculate_distance_matrix(self) -> np.ndarray:
        """Tính ma trận khoảng cách Euclidean giữa các thành phố"""
        distances = np.zeros((self.n_cities, self.n_cities))
        for i in range(self.n_cities):
            for j in range(i + 1, self.n_cities):
                dist = np.sqrt(np.sum((self.cities[i] - self.cities[j])**2))
                distances[i][j] = distances[j][i] = dist
        return distances
    
    def _calculate_probabilities(self, current_city: int, available_cities: List[int]) -> np.ndarray:
        """
        Tính xác suất chọn thành phố tiếp theo
        
        Args:
            current_city: Thành phố hiện tại
            available_cities: Danh sách các thành phố có thể đi
            
        Returns:
            Mảng xác suất cho mỗi thành phố có thể đi
        """
        pheromone_values = np.array([self.pheromones[current_city][city] for city in available_cities])
        heuristic_values = np.array([1.0 / max(self.distances[current_city][city], 1e-10) 
                                   for city in available_cities])
        
        # Tính giá trị attractiveness
        attractiveness = (pheromone_values ** self.alpha) * (heuristic_values ** self.beta)
        
        # Tránh chia cho 0
        total = np.sum(attractiveness)
        if total == 0:
            return np.ones(len(available_cities)) / len(available_cities)
        
        return attractiveness / total
    
    def _construct_path(self) -> Tuple[List[int], float]:
        """
        Xây dựng đường đi cho một con kiến
        
        Returns:
            Tuple (đường đi, tổng khoảng cách)
        """
        # Chọn thành phố bắt đầu ngẫu nhiên
        start_city = random.randint(0, self.n_cities - 1)
        path = [start_city]
        available_cities = list(range(self.n_cities))
        available_cities.remove(start_city)
        
        # Xây dựng đường đi
        while available_cities:
            current_city = path[-1]
            probabilities = self._calculate_probabilities(current_city, available_cities)
            
            # Chọn thành phố tiếp theo dựa trên xác suất
            next_city_idx = np.random.choice(len(available_cities), p=probabilities)
            next_city = available_cities[next_city_idx]
            
            path.append(next_city)
            available_cities.remove(next_city)
        
        # Tính tổng khoảng cách (bao gồm đường về)
        total_distance = 0
        for i in range(len(path)):
            current = path[i]
            next_city = path[(i + 1) % len(path)]  # Quay về thành phố đầu
            total_distance += self.distances[current][next_city]
        
        return path, total_distance
    
    def _update_pheromones(self, all_paths: List[Tuple[List[int], float]]):
        """
        Cập nhật ma trận pheromone
        
        Args:
            all_paths: Danh sách (đường đi, khoảng cách) của tất cả kiến
        """
        # Bay hơi pheromone
        self.pheromones *= (1 - self.rho)
        
        # Cập nhật pheromone dựa trên đường đi của các kiến
        for path, distance in all_paths:
            pheromone_deposit = self.q / distance
            
            # Cập nhật cho tất cả các cạnh trong đường đi
            for i in range(len(path)):
                current = path[i]
                next_city = path[(i + 1) % len(path)]
                self.pheromones[current][next_city] += pheromone_deposit
                self.pheromones[next_city][current] += pheromone_deposit
        
        # Đảm bảo pheromone không quá nhỏ
        self.pheromones = np.maximum(self.pheromones, 0.01)
    
    def solve(self, verbose: bool = True) -> Tuple[List[int], float]:
        """
        Giải bài toán TSP bằng thuật toán ACO
        
        Args:
            verbose: In thông tin quá trình tìm kiếm
            
        Returns:
            Tuple (đường đi tốt nhất, khoảng cách ngắn nhất)
        """
        for iteration in range(self.max_iterations):
            # Tạo đường đi cho tất cả kiến
            all_paths = []
            for _ in range(self.n_ants):
                path, distance = self._construct_path()
                all_paths.append((path, distance))
                
                # Cập nhật nghiệm tốt nhất
                if distance < self.best_distance:
                    self.best_distance = distance
                    self.best_path = path.copy()
            
            # Cập nhật pheromone
            self._update_pheromones(all_paths)
            
            # Lưu lịch sử
            self.distance_history.append(self.best_distance)
            
            if verbose and (iteration + 1) % 20 == 0:
                print(f"Vòng lặp {iteration + 1}: Khoảng cách tốt nhất = {self.best_distance:.2f}")
        
        return self.best_path, self.best_distance
    
    def plot_convergence(self):
        """Vẽ biểu đồ hội tụ thuật toán"""
        plt.figure(figsize=(10, 6))
        plt.plot(self.distance_history)
        plt.title('Quá trình Hội tụ của Thuật toán ACO')
        plt.xlabel('Vòng lặp')
        plt.ylabel('Khoảng cách tốt nhất')
        plt.grid(True)
        plt.show()
    
    def plot_solution(self):
        """Vẽ nghiệm tốt nhất"""
        if self.best_path is None:
            print("Chưa có nghiệm. Hãy chạy solve() trước.")
            return
        
        plt.figure(figsize=(10, 8))
        
        # Vẽ các thành phố
        x_coords = [self.cities[i][0] for i in range(self.n_cities)]
        y_coords = [self.cities[i][1] for i in range(self.n_cities)]
        plt.scatter(x_coords, y_coords, c='red', s=100, zorder=5)
        
        # Đánh số thành phố
        for i in range(self.n_cities):
            plt.annotate(f'{i}', (self.cities[i][0], self.cities[i][1]), 
                        xytext=(5, 5), textcoords='offset points')
        
        # Vẽ đường đi tốt nhất
        path_x = [self.cities[i][0] for i in self.best_path] + [self.cities[self.best_path[0]][0]]
        path_y = [self.cities[i][1] for i in self.best_path] + [self.cities[self.best_path[0]][1]]
        plt.plot(path_x, path_y, 'b-', linewidth=2, alpha=0.7)
        
        plt.title(f'Nghiệm tốt nhất - Khoảng cách: {self.best_distance:.2f}')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.grid(True, alpha=0.3)
        plt.show()


def input_cities() -> List[Tuple[float, float]]:
    """Nhập tọa độ các thành phố từ người dùng"""
    n = int(input("Nhập số lượng thành phố: "))
    cities = []
    print("Nhập tọa độ các thành phố (x y):")
    for i in range(n):
        while True:
            try:
                line = input(f"Thành phố {i}: ").strip()
                x, y = map(float, line.split())
                cities.append((x, y))
                break
            except ValueError:
                print("Lỗi: Vui lòng nhập hai số thực được phân cách bởi dấu cách")
    return cities

def generate_random_cities(n_cities: int, max_coord: float = 100) -> List[Tuple[float, float]]:
    """Tạo ngẫu nhiên tọa độ các thành phố để test"""
    random.seed(42)  # Để kết quả có thể tái lập
    return [(random.uniform(0, max_coord), random.uniform(0, max_coord)) 
            for _ in range(n_cities)]

def main():
    print("=== GIẢI THUẬT ĐÀN KIẾN CHO BÀI TOÁN NGƯỜI DU LỊCH ===")
    print("1. Nhập tọa độ thành phố thủ công")
    print("2. Tạo ngẫu nhiên để test")
    
    choice = input("Chọn (1/2): ").strip()
    
    if choice == '1':
        cities = input_cities()
    else:
        n_cities = int(input("Số thành phố để test (khuyến nghị 5-15): "))
        cities = generate_random_cities(n_cities)
        print(f"Đã tạo {n_cities} thành phố ngẫu nhiên")
    
    # Tạo đối tượng ACO với tham số mặc định
    aco = AntColonyTSP(
        cities=cities,
        n_ants=min(10, len(cities)),  # Số kiến tỉ lệ với số thành phố
        alpha=1.0,
        beta=2.0,
        rho=0.1,
        q=100.0,
        max_iterations=100
    )
    
    print(f"\nĐang giải bài toán với {len(cities)} thành phố...")
    print("Tham số: α=1.0, β=2.0, ρ=0.1, Q=100.0")
    
    # Giải bài toán
    best_path, best_distance = aco.solve(verbose=True)
    
    # In kết quả
    print(f"\n=== KẾT QUẢ ===")
    print(f"Đường đi tối ưu: {' -> '.join(map(str, best_path))} -> {best_path[0]}")
    print(f"Tổng khoảng cách: {best_distance:.4f}")
    
    # Vẽ biểu đồ (tùy chọn)
    try:
        show_plots = input("\nBạn có muốn xem biểu đồ? (y/n): ").lower() == 'y'
        if show_plots:
            aco.plot_convergence()
            aco.plot_solution()
    except:
        print("Không thể hiển thị biểu đồ (thiếu matplotlib)")

if __name__ == "__main__":
    main()
