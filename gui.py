import tkinter as tk
from PIL import Image, ImageTk, ImageDraw, ImageFont  
from sokoban import GameState  
import search
from problem import *

# Cửa sổ MainMenu
class MainMenu:
    def __init__(self, master):
        self.master = master
        self.master.title("Main Menu")

        self.background_image = Image.open("./image/map/background.png")
        self.background_image = self.background_image.resize((800, 600), Image.Resampling.LANCZOS)
        self.background_photo = ImageTk.PhotoImage(self.background_image)

        # Tạo khung cho cửa sổ
        self.main_frame = tk.Frame(master)
        self.main_frame.pack()

        # Canva chứa giao diện cho cửa sổ
        self.canvas = tk.Canvas(self.main_frame, width=800, height=600)
        self.canvas.pack()
        self.canvas.create_image(0, 0, anchor='nw', image=self.background_photo)

        # Tạo nút Algorithm
        self.algorithm_button = tk.Button(self.main_frame, text="Algorithms", command=self.show_algorithm_page, width=20)
        self.canvas.create_window(400, 300, window=self.algorithm_button)

        # Tạo nút Level
        self.level_button = tk.Button(self.main_frame, text="Levels", command=self.show_level_page, width=20)
        self.canvas.create_window(400, 350, window=self.level_button)

        # Tạo nút Setting
        self.setting_button = tk.Button(self.main_frame, text="Setting", width=20)
        self.canvas.create_window(400, 400, window=self.setting_button)


    def show_algorithm_page(self):
        self.main_frame.pack_forget()
        AlgorithmPage(self.master, self, self.background_photo)

    def show_level_page(self):
        self.main_frame.pack_forget()
        LevelPage(self.master, self, self.background_photo)

# Cửa sổ Algorithm
class AlgorithmPage:
    def __init__(self, master, main_menu, background_photo):
        self.master = master
        self.main_menu = main_menu
        self.background_photo = background_photo

        self.algorithm_frame = tk.Frame(master)
        self.algorithm_frame.pack()

        self.canvas = tk.Canvas(self.algorithm_frame, width=800, height=600)
        self.canvas.pack()
        self.canvas.create_image(0, 0, anchor='nw', image=self.background_photo)

        # Tạo các nút thuật toán tương ứng
        algorithms = [("Breadth-First Search", "BFS", 300),
                      ("Depth-First Search", "DFS", 350),
                      ("Uniform Cost Search", "UCS", 400),
                      ("A* Search", "A Star", 450)]

        for text, alg, y_pos in algorithms:
            button = tk.Button(self.algorithm_frame, text=text, command=lambda a=alg: self.algorithm_detail_game(a), width=20)
            self.canvas.create_window(400, y_pos, window=button)

        self.back_button = tk.Button(self.algorithm_frame, text="Back to Main Menu", command=self.back_to_main_menu, width=15)
        self.canvas.create_window(400, 500, window=self.back_button)
        
    def algorithm_detail_game(self, algorithm):
        self.algorithm_frame.pack_forget()

        new_frame = tk.Frame(self.master)
        new_frame.pack()

        background_image = Image.open(f"./image/algorithms/{algorithm}.png").resize((800, 600), Image.LANCZOS)
        background_photo = ImageTk.PhotoImage(background_image)

        canvas = tk.Canvas(new_frame, width=800, height=600)
        canvas.pack()
        canvas.create_image(0, 0, anchor='nw', image=background_photo)
        canvas.image = background_photo

        label = tk.Label(new_frame, text=f"Algorithm: {algorithm}", font=("Arial", 20), bg="white")
        canvas.create_window(400, 30, window=label)

        back_button = tk.Button(new_frame, text="Back", command=lambda: self.back_to_algorithm_page(new_frame), width=20)
        canvas.create_window(400, 570, window=back_button)

    def back_to_algorithm_page(self, new_frame):
        new_frame.pack_forget()
        self.algorithm_frame.pack()

    def back_to_main_menu(self):
        self.algorithm_frame.pack_forget()
        self.main_menu.main_frame.pack()

    
# Cửa sổ Level
class LevelPage:
    def __init__(self, master, main_menu, background_photo):
        self.master = master
        self.main_menu = main_menu
        self.background_photo = background_photo

        # Khởi tạo level hiện tại và level lớn nhất
        self.current_level = 1
        self.total_levels = 10  

        self.level_frame = tk.Frame(master)
        self.level_frame.pack()

        self.canvas = tk.Canvas(self.level_frame, width=800, height=600)
        self.canvas.pack()
        self.canvas.create_image(0, 0, anchor='nw', image=self.background_photo)

        # Tạo nút Level
        self.level_button = tk.Button(self.level_frame, text=f"Level {self.current_level}",
                                      font=("Arial", 20), width=15, state="disabled")
        self.canvas.create_window(400, 300, window=self.level_button)

        # Tạo các sự kiện bàn phím
        self.master.bind("<Left>", self.previous_level)
        self.master.bind("<Right>", self.next_level)
        self.master.bind("<Return>", self.select_level)

        self.back_button = tk.Button(self.level_frame, text="Back to Main Menu",command=self.back_to_main_menu, width=20)
        self.canvas.create_window(400, 400, window=self.back_button)

    def previous_level(self, event):
        if self.current_level > 1:
            self.current_level -= 1
            self.level_button.config(text=f"Level {self.current_level}")

    def next_level(self, event):
        if self.current_level < self.total_levels:
            self.current_level += 1
            self.level_button.config(text=f"Level {self.current_level}")

    def select_level(self, event):
        self.level_frame.pack_forget()
        LevelDetailPage(self.master, self, self.current_level)

    def back_to_main_menu(self):
        self.level_frame.pack_forget()
        self.main_menu.main_frame.pack()

# Cửa số level cụ thể
class LevelDetailPage:
    def __init__(self, master, level_page, level):
        self.master = master
        self.level_page = level_page
        self.level = level  # Lưu lại Level hiện tại

        self.detail_frame = tk.Frame(master)
        self.detail_frame.pack()

        bg_path = f"./image/level/level{level}.png"
        self.background_image = Image.open(bg_path).resize((800, 600), Image.Resampling.LANCZOS)
        self.background_photo = ImageTk.PhotoImage(self.background_image)

        self.canvas = tk.Canvas(self.detail_frame, width=800, height=600)
        self.canvas.pack()
        self.canvas.create_image(0, 0, anchor='nw', image=self.background_photo)

        # Tạo nhãn level tương ứng đã chọn
        level_label = tk.Label(self.detail_frame, text=f"Level {level}", font=("Arial", 20), bg="white", width=10)
        self.canvas.create_window(400, 50, window=level_label)

        # Tạo các nút thuật toán
        algorithms = ["DFS", "BFS", "A*", "UCS"]
        for idx, algo in enumerate(algorithms):
            button = tk.Button(self.detail_frame, text=algo, font=("Arial", 14), width=15,command=lambda a=algo: self.start_game(a))  # Attach event
            self.canvas.create_window(100, 200 + idx * 50, window=button)

        self.back_button = tk.Button(self.detail_frame, text="Back to Levels",command=self.back_to_levels, width=20)
        self.canvas.create_window(100, 400, window=self.back_button)

    def start_game(self, algorithm):
        gameState = GameState()
        level_str = str(self.level).zfill(2)
        gameState.read_gameState_file(f"./input/input-{level_str}.txt")
        problem = SearchProblem(gameState)

        if algorithm == "BFS":
            solution = search.breadthFirstSearch(problem)
        elif algorithm == "DFS":
            solution = search.depthFirstSearch(problem)
        elif algorithm == "UCS":
            solution = search.uniformCostSearch(problem)
        elif algorithm == "A*":
            solution = search.aStarSearch(problem)

        f = open(f"./output/output-{level_str}.txt","a")
        f.write(solution)
        f.write('\n')
        f.close()
        lines = solution.splitlines()
        last_line = lines[-1]

        self.detail_frame.pack_forget()  

        # Khởi tạo giao diện game
        self.gui = SokobanGUI(self.master, gameState, last_line, previous_page=self)

    def back_to_levels(self):
        """Quay lại trang Level."""
        self.detail_frame.pack_forget()
        self.level_page.level_frame.pack()

# Cửa sổ SokobanGUI
class SokobanGUI:
    def __init__(self, master, gameState,path, previous_page=None):
        self.master = master
        self.gameState = gameState
        self.cell_size = 80
        self.previous_page = previous_page
        self.is_paused = False  # Cờ lưu trạng thái tạm dừng
        self.is_reset = False # Cờ lưu trạng thái khởi tạo lại
        self.length = max(len(line) for line in self.gameState.grid)  
        self.canvas = tk.Canvas(master, width=self.length * self.cell_size * 1.5,height=len(self.gameState.grid) * self.cell_size * 1.5)
        self.canvas.pack()
        
        # Gắn ảnh tương ứng với từng kí tự
        self.images = {
            '#': self.load_image("./image/map/brick.png"),
            '.': self.load_image("./image/map/goal.png"),
            '@': self.load_image("./image/map/character.png"),
            ' ': self.load_image("./image/map/ground.png"),  
            '%': self.load_image("./image/map/out_of_map.png")
        }

        # Vẽ bản đồ và khởi tạo bước đi, trọng số
        self.draw_map()
        self.path = path  
        self.current_step = 0 
        self.weights = 0 
        
        # Tạo các nút Start, Pause, Reset
        self.canvas.pack(side=tk.LEFT, padx=10, pady=10)

        self.control_frame = tk.Frame(master)
        self.control_frame.pack(side=tk.RIGHT, fill=tk.Y)  

        tk.Label(self.control_frame).pack(expand=True)  # Nhãn rỗng tạo khoảng trống phía trên

        self.start_button = tk.Button(self.control_frame, text="Start", command=self.start_game, width=10, height=2)
        self.start_button.pack(pady=5)

        self.pause_button = tk.Button(self.control_frame, text="Pause", command=self.pause_game, width=10, height=2)
        self.pause_button.pack(pady=5)

        self.reset_button = tk.Button(self.control_frame, text="Reset", command=self.reset_game, width=10, height=2)
        self.reset_button.pack(pady=5)

        # Nút quay lại
        self.back_button = tk.Button(self.control_frame, text="Back", command=self.back_to_previous_page, width=10, height=2)
        self.back_button.pack(pady=5)

        tk.Label(self.control_frame).pack(expand=True)
        self.master.after(400, self.move_player)  
    

    def load_image(self, path):
        img = Image.open(path).resize((self.cell_size, self.cell_size), Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(img)
    
    def draw_text(self, text, y_position):
        x = self.length * self.cell_size + self.cell_size * 1.5
        y = y_position  
        self.canvas.create_text(x, y, anchor='ne', text=text, font=("Arial", 12), fill="black")

    def draw_map(self):
        for y, line in enumerate(self.gameState.grid):
            for x, char in enumerate(line):
                self.draw_cell(x, y, char)

    def draw_cell(self, x, y, char):
        x1 = x * self.cell_size
        y1 = y * self.cell_size
        idx = 0
        if char in ('$','*'):
            
            # Lấy về chỉ số tảng đá đang được thao tác
            if ((x,y)) in self.gameState.current_stones:
                idx = self.gameState.current_stones.index((x,y))
            else:
                idx = self.gameState.pre_stones.index((x,y))
            
            # Chèn trọng số ứng mỗi tảng đá 
            if (char == '$'):
                original_image = Image.open("./image/map/rock.png").resize((self.cell_size, self.cell_size), Image.Resampling.LANCZOS)
            else:
                original_image = Image.open("./image/map/rock_goal.png").resize((self.cell_size, self.cell_size), Image.Resampling.LANCZOS)
            
            draw = ImageDraw.Draw(original_image)
            font = ImageFont.truetype("arial.ttf", 30)
            text = str(self.gameState.weights[idx])

            text_bbox = draw.textbbox((0, 0), text, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]

            position = ((self.cell_size - text_width) // 2,(self.cell_size - text_height) // 2)

            draw.text(position, text, font=font, fill=(255, 255, 255))
            self.images[char] = ImageTk.PhotoImage(original_image)

            key = (char, x, y)
            self.images[key] = ImageTk.PhotoImage(original_image)

            if not hasattr(self, 'image_refs'):
                self.image_refs = []  

            if self.images[key] not in self.image_refs:
                self.image_refs.append(self.images[key]) 

            self.canvas.create_image(x1, y1, anchor='nw', image=self.images[key])
        else:
            self.canvas.create_image(x1, y1, anchor='nw', image=self.images[char])

    # Hàm để bắt đầu trò chơi
    def start_game(self):
        if self.is_paused:
            self.is_paused = False
        if self.is_reset:
            self.is_reset = False
        self.master.after(200, self.move_player) 

    # Hàm tạm dừng trò chơi
    def pause_game(self):
        self.is_paused = True

    # Hàm khởi tạo lại trò chơi
    def reset_game(self):
        level_str = str(self.previous_page.level).zfill(2)  
        self.gameState.read_gameState_file(f"./input/input-{level_str}.txt")  
        self.is_paused = False  
        self.is_reset = True
        self.redraw()

    def back_to_previous_page(self):
        self.canvas.pack_forget()
        self.control_frame.pack_forget()
        if self.previous_page:
            self.previous_page.detail_frame.pack()
    
    def move_player(self):
        if self.is_paused or self.current_step >= len(self.path):
            return
        move = self.path[self.current_step]
        self.update_player_position(move)
        self.current_step += 1
        self.master.after(500, self.move_player)
            
    def update_player_position(self, move):
        # x,y lưu toạ độ hiện tại của ares
        x, y = self.gameState.ares

        # Lưu toạ độ của ares trong bước đi tiếp theo
        if move == 'u' or move == 'U':  
            next_y = y - 1
            next_x = x
        elif move == 'd' or move == 'D':  
            next_y = y + 1
            next_x = x
        elif move == 'l' or move == 'L':  
            next_x = x - 1
            next_y = y
        elif move == 'r' or move == 'R':  
            next_x = x + 1
            next_y = y
        else:
            return  # Di chuyển không hợp lệ

        # Kiểm tra vị trí mới có hợp lệ hay không (không ra khỏi đồ thị và không đi xuyên tường)
        if 0 <= next_x < len(self.gameState.grid[next_y]) and 0 <= next_y < len(self.gameState.grid):
            if self.gameState.grid[next_y][next_x] != '#':  # not into the wall

                # Kiểm tra thao tác đẩy tảng đá
                if move.isupper():
                    self.gameState.pre_active_stone_index = self.gameState.active_stone_index
                    stone_x, stone_y = next_x, next_y # Lưu toạ độ hiện tại của tảng đá
                    
                    # Đẩy đá lên hoặc xuống
                    if move == 'U' or move == 'D' :
                        if move == 'U':
                            stone_y -= 1
                        else:
                            stone_y += 1
                        if self.gameState.grid[next_y][next_x] == '*':
                            self.gameState.grid[next_y] = self.gameState.grid[next_y][:x] + '.' + self.gameState.grid[next_y][x+1:]
                        if self.gameState.grid[stone_y][stone_x] == '.':
                            self.gameState.grid[stone_y] = self.gameState.grid[stone_y][:x] + '*' + self.gameState.grid[stone_y][x+1:]
                        else:
                            self.gameState.grid[stone_y] = self.gameState.grid[stone_y][:x] + '$' + self.gameState.grid[stone_y][x+1:]
                        if self.gameState.grid[y][x] != '.':
                            self.gameState.grid[y] = self.gameState.grid[y][:x] + ' ' + self.gameState.grid[y][x+1:] 
                    # Đẩy đá qua trái hoặc phải
                    else:
                        if move == 'L':
                            stone_x -= 1
                            if self.gameState.grid[next_y][next_x] == '*':
                                self.gameState.grid[y] = self.gameState.grid[y][:next_x] + '.'+self.gameState.grid[y][x:]
                            if self.gameState.grid[stone_y][stone_x] == '.':
                                self.gameState.grid[y] = self.gameState.grid[y][:stone_x] + '*'+self.gameState.grid[y][stone_x+1:]
                            elif self.gameState.grid[y][x] != '.' and self.gameState.grid[y][next_x] != '.':
                                self.gameState.grid[next_y] = self.gameState.grid[next_y][:stone_x] + '$  ' + self.gameState.grid[next_y][x+1:]
                            elif self.gameState.grid[y][next_x] == '.':
                                self.gameState.grid[y] = self.gameState.grid[y][:stone_x] + '$' + self.gameState.grid[y][next_x:]
                            else:
                                self.gameState.grid[next_y] = self.gameState.grid[next_y][:stone_x] + '$ ' + self.gameState.grid[next_y][x:]
                                                       
                        else:
                            stone_x += 1
                            if self.gameState.grid[next_y][next_x] == '*':
                                self.gameState.grid[y] = self.gameState.grid[y][:next_x] + '.'+self.gameState.grid[y][stone_x:]
                            if self.gameState.grid[stone_y][stone_x] == '.':
                                self.gameState.grid[y] = self.gameState.grid[y][:stone_x] + '*'+self.gameState.grid[y][stone_x+1:]
                            elif self.gameState.grid[y][x] != '.' and self.gameState.grid[y][next_x] != '.':
                                self.gameState.grid[next_y] = self.gameState.grid[next_y][:next_x] + ' $' + self.gameState.grid[next_y][stone_x+1:]
                            elif self.gameState.grid[y][next_x] == '.':
                                self.gameState.grid[next_y] = self.gameState.grid[next_y][:stone_x] + '$' + self.gameState.grid[next_y][stone_x+1:]
                            else:
                                self.gameState.grid[next_y] = self.gameState.grid[next_y][:stone_x] + '$' + self.gameState.grid[next_y][stone_x+1:]
                            
                if self.gameState.grid[y][x] != '.':
                    self.gameState.grid[y] = self.gameState.grid[y][:x] + ' ' + self.gameState.grid[y][x+1:]

                # Cập nhật lại vị trí của các tảng đá và chỉ số của tảng đá được đẩy
                self.gameState.update_active_stone_index(next_x,next_y,move)
                self.gameState.ares = (next_x, next_y)
                # Với mỗi bước sẽ vẽ lại đồ thị ứng với vị trị của các tảng đá và ares
                self.redraw()
                               
    def redraw(self):
        self.canvas.delete("all")  
        self.draw_map()  
        self.draw_cell(self.gameState.ares[0], self.gameState.ares[1], '@')
        y_start = 10  
        line_height = 20 

        # Hiển thị thống kê qua từng bước đi của ares
        if self.gameState.active_stone_index != None:
            self.weights += self.gameState.weights[self.gameState.active_stone_index]
        if self.is_reset:
            self.current_step = 0  
            self.weights = 0
            self.draw_text(f"STATISTIC:", y_start + line_height)
            self.draw_text(f"STEP: {self.current_step}", y_start + 2 * line_height)  
            self.draw_text(f"WEIGHTS: {self.weights}", y_start + 3 * line_height)
        else:
            self.draw_text(f"STATISTIC:", y_start + line_height)
            self.draw_text(f"STEP: {self.current_step+1}", y_start + 2 * line_height)  
            self.draw_text(f"WEIGHTS: {self.weights}", y_start + 3 * line_height)
