def find_1D_iterator(line, char):
    pos = 0
    pos = line.find(char, pos)
    while pos != -1:
        yield pos
        pos = line.find(char, pos + 1)

def find_2D_iterator(grid, char):
    for y, line in enumerate(grid):
        for x in find_1D_iterator(line, char):
            yield (x, y)

class GameState:
    def __init__(self):
        self.grid = []  # Khởi tạo grid
        self.ares = None  # Vị trí người chơi
        self.stones = []  # Vị trí đá
        self.switches = []  # Vị trí mục tiêu
        self.walls = []  # Vị trí tường
        self.weights = []  # Trọng số
        self.pre_active_stone_index = None
        self.active_stone_index = None  # Chỉ số của tảng đá đang được thao tác
        self.current_stones = [] # Toạ độ hiện tại của các tảng đá
        self.pre_stones = [] # Toạ độ trước một bước của các tảng đá

    def extract_locations(self, grid):
        areses = list(find_2D_iterator(grid, "@"))  # Tìm vị trí người chơi
        areses_on_a_target = list(find_2D_iterator(grid, "+"))

        # Kiểm tra có đúng một người chơi
        assert len(areses) + len(areses_on_a_target) <= 1, "Có nhiều hơn một người chơi"
        
        # Xác định vị trí người chơi
        if len(areses) == 1:
            self.ares = areses[0]
        elif len(areses_on_a_target) == 1:
            self.ares = areses_on_a_target[0]
        # Tìm vị trí đá và các mục tiêu
        self.stones = list(find_2D_iterator(grid, "$"))  # Vị trí đá
        self.switches = list(find_2D_iterator(grid, "."))  # Vị trí mục tiêu
        switches_with_stones = list(find_2D_iterator(grid, "*"))  # Vị trí đá trên mục tiêu
        self.stones += switches_with_stones
        self.switches += switches_with_stones

        # Tìm tường
        self.walls = list(find_2D_iterator(grid, "#"))

        # Đảm bảo số lượng đá bằng số lượng mục tiêu
        assert len(self.stones) == len(self.switches), "Số lượng đá phải bằng số lượng mục tiêu"
        # Sao chép stones vào current_stones (không dùng tham chiếu)
        self.current_stones = list(self.stones)  # Chuyển đổi từ tuple sang list


        self.stones = tuple(self.stones)
        self.switches = tuple(self.switches)
        self.walls = tuple(self.walls)

    def read_gameState_file(self, file_path):
        with open(file_path, 'r') as f:
            first_line = f.readline().strip()
            self.weights = list(map(int, first_line.split()))  # Đọc trọng số từ dòng đầu tiên
            self.grid = [line.rstrip('\n') for line in f]  # Đọc từng dòng và xóa ký tự xuống dòng
        self.nrows = len(self.grid) 
        self.ncols = max(len(line.rstrip()) for line in self.grid) 
        self.extract_locations(self.grid)

    # Cập nhật mảng lưu vị trí hiện tại và trước một bước của các tảng đá, chỉ số của tảng đá đang được đẩy (nếu có)
    def update_active_stone_index(self,x,y,move):
        arr = ["U","R","L","D"]
        self.pre_stones = self.current_stones[:]  
        if (x, y) in self.current_stones and move in arr:
            self.active_stone_index = self.current_stones.index((x,y))
            if move == "U":
                self.current_stones[self.active_stone_index] = (x,y-1)
            elif move == "D":
                self.current_stones[self.active_stone_index] = (x,y+1)
            elif move == "R":
                self.current_stones[self.active_stone_index] = (x+1,y)
            else:
                self.current_stones[self.active_stone_index] = (x-1,y)
        else:
            self.active_stone_index = None  # Không có viên đá nào đang được thao tác
