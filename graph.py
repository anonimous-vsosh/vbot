import sys
import tkinter as tk
from tkinter import messagebox, simpledialog
from typing import List, Tuple, Dict


class FunctionNamesInput:
    def __init__(self):
        self.function_names = {}
        self.root = tk.Tk()
        self.root.title("OCPM Robotics Contest - Настройка функций")
        self.root.geometry("400x250")

        self._setup_ui()
        self._center_window()
        self.root.mainloop()

    def _center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'+{x}+{y}')

    def _setup_ui(self):
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(expand=True, fill=tk.BOTH)

        tk.Label(main_frame,
                 text="Введите имена функций управления",
                 font=('Arial', 12, 'bold')).pack(pady=10)

        fields = [
            ("Поворот налево:", "turn_left"),
            ("Поворот направо:", "turn_right"),
            ("Движение до перекрестка:", "go_to_cross"),
            ("Экстренная остановка:", "emergency_stop")
        ]

        self.entries = {}
        for text, key in fields:
            frame = tk.Frame(main_frame)
            frame.pack(fill=tk.X, pady=3)

            tk.Label(frame, text=text, width=20, anchor='w').pack(side=tk.LEFT)
            entry = tk.Entry(frame)
            entry.pack(side=tk.RIGHT, expand=True, fill=tk.X)
            self.entries[key] = entry

        tk.Button(main_frame,
                  text="Подтвердить",
                  command=self._on_submit,
                  bg="#4CAF50",
                  fg="white").pack(pady=15)

    def _on_submit(self):
        try:
            self.function_names = {
                key: entry.get().strip()
                for key, entry in self.entries.items()
            }

            if not all(self.function_names.values()):
                raise ValueError("Все поля должны быть заполнены")

            self.root.destroy()

        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def get_function_names(self) -> Dict[str, str]:
        return self.function_names


import tkinter as tk
from tkinter import messagebox

class WeightCollector:
    """Окно ввода весов рёбер графа и получение результата"""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Веса рёбер")
        self.root.geometry("900x800")
        self.root.resizable(False, False)

        self.columns = ["а", "б", "в", "г", "д", "е", "ж"]
        self.rows = ["1", "2", "3", "4", "5"]
        self.cell_size = 120
        self.entries = []

        self.create_interface()
        self.weights = None

        self.root.mainloop()

    def create_interface(self):
        # Canvas для сетки
        canvas_frame = tk.Frame(self.root)
        canvas_frame.pack(padx=10, pady=10)

        canvas_width = self.cell_size * (len(self.columns) + 1)
        canvas_height = self.cell_size * (len(self.rows) + 1)

        self.canvas = tk.Canvas(canvas_frame, width=canvas_width, height=canvas_height, bg="white")
        self.canvas.pack()

        self.create_grid()
        self.create_entries()

        # Кнопка под canvas
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        tk.Button(
            button_frame,
            text="Получить веса",
            command=self.on_submit,
            bg='#4CAF50',
            fg='white',
            font=("Arial", 12, "bold"),
            width=20,
            height=2
        ).pack()

    def create_grid(self):
        for i in range(len(self.columns) + 1):
            for j in range(len(self.rows) + 1):
                x1, y1 = i * self.cell_size, j * self.cell_size
                x2, y2 = x1 + self.cell_size, y1 + self.cell_size
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="black")

        for i, col in enumerate(self.columns):
            x = (i + 1) * self.cell_size + self.cell_size // 2
            self.canvas.create_text(x, 15, text=col, font=('Arial', 10, 'bold'))

        for j, row in enumerate(self.rows):
            y = (j + 1) * self.cell_size + self.cell_size // 2
            self.canvas.create_text(15, y, text=row, font=('Arial', 10, 'bold'))

    def create_entries(self):
        # Вертикальные рёбра
        for i in range(len(self.columns)):
            for j in range(1, len(self.rows)):
                x = (i + 1) * self.cell_size
                y = j * self.cell_size + self.cell_size // 2
                entry = self._make_entry(x, y)
                self.entries.append(entry)

        # Горизонтальные рёбра
        for i in range(1, len(self.columns)):
            for j in range(len(self.rows)):
                x = i * self.cell_size + self.cell_size // 2
                y = (j + 1) * self.cell_size
                entry = self._make_entry(x, y)
                self.entries.append(entry)

        # Добавим табуляцию
        for i in range(len(self.entries) - 1):
            self.entries[i].bind("<Tab>", lambda e, idx=i: self._focus_next(idx))
        self.entries[-1].bind("<Tab>", lambda e: self._focus_next(0))
        self.entries[0].focus_set()

    def _make_entry(self, x, y):
        entry = tk.Entry(self.root, width=3, justify="center")
        entry.insert(0, "1")
        entry.place(in_=self.canvas, x=x - 15, y=y - 10)
        return entry

    def _focus_next(self, index):
        next_index = (index + 1) % len(self.entries)
        self.entries[next_index].focus_set()
        return "break"  # предотвращает стандартный переход фокуса

    def on_submit(self):
        try:
            raw = [int(entry.get()) for entry in self.entries]
            self.weights = []

            for i in range(6):  # по вертикали
                self.weights += raw[i * 4:(i + 1) * 4]
                self.weights += raw[28 + i * 5:28 + (i + 1) * 5]
            self.weights += raw[24:28]  # оставшиеся горизонтальные

            self.root.destroy()
        except ValueError:
            messagebox.showerror("Ошибка", "Все веса должны быть целыми числами.")

def get_weights():
    app = WeightCollector()
    return app.weights


class PathCodeGenerator:
    """Генератор кода для перемещения робота"""

    def __init__(self, function_names: Dict[str, str], weights: List[int]):
        self.function_names = function_names
        self.weights = weights
        self.ROWS = 5
        self.COLS = 7
        self.COL_MAP = {c: i for i, c in enumerate("абвгдеж")}

    def generate_code(self):
        with open("get_path_func.txt", "w") as f:
            sys.stdout = f
            self.print_header()
            self.print_condition_blocks()
            sys.stdout = sys.__stdout__

    def print_header(self):
        print(f"""/*
 * OCPM robotics contest
 * Senior group - task 1
 * Generated code
 */
void get_path(byte x, byte y) {{""")

    def print_condition_blocks(self):
        for i in range(self.COLS):
            for j in range(self.ROWS):
                code = self._generate_single_condition(i, j)
                print(code)
        print("}")  # Закрываем тело функции get_path

    def _generate_single_condition(self, x: int, y: int) -> str:
        condition = f"  if (x == {x} && y == {y})" if (x, y) == (0, 2) else f"  else if (x == {x} && y == {y})"
        finish = self.vertex_to_str(x, y)
        path = self.way(self.weights, finish)
        path_code = self.code(path)
        function_lines = [f"    {self.function_names['go_to_cross']}();" if cmd == 0
                          else f"    {self.function_names['turn_left']}();" if cmd == 1
                          else f"    {self.function_names['turn_right']}();" for cmd in path_code]
        actions = "\n".join(function_lines)
        stop_code = f"""    {self.function_names['emergency_stop']}();
    delay(4000);"""

        return f"""
  {condition} {{
{actions}
{stop_code}
  }}""".strip()

    def parse_vertex(self, vertex: str) -> tuple:
        col_map = self.COL_MAP
        x = col_map[vertex[0]]
        y = int(vertex[1]) - 1
        return (x, y)

    def vertex_to_str(self, x: int, y: int) -> str:
        col_map = {i: c for i, c in enumerate("абвгдеж")}
        return f"{col_map[x]}{y + 1}"

    def get_weight(self, x1: int, y1: int, x2: int, y2: int) -> int:
        if x1 == x2:
            index = 9 * x1 + min(y1, y2)
        else:
            index = 9 * min(x1, x2) + 4 + y1
        return self.weights[index]

    def way(self, weights: List[int], finish: str) -> List[str]:
        start = self.parse_vertex("а3")
        goal = self.parse_vertex(finish)

        pq = [(0, start)]
        dist = {start: 0}
        prev = {start: None}

        while pq:
            pq.sort()
            current_dist, (cx, cy) = pq.pop(0)

            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nx, ny = cx + dx, cy + dy
                if 0 <= nx < self.COLS and 0 <= ny < self.ROWS:
                    edge_weight = self.get_weight(cx, cy, nx, ny)
                    new_dist = current_dist + edge_weight
                    if new_dist < dist.get((nx, ny), float('inf')):
                        dist[(nx, ny)] = new_dist
                        prev[(nx, ny)] = (cx, cy)
                        pq.append((new_dist, (nx, ny)))

        path = []
        step = goal
        while step:
            path.append(self.vertex_to_str(*step))
            step = prev.get(step)

        return path[::-1]

    def code(self, way: List[str]) -> List[int]:
        result = []
        curr_dir = 0

        for index in range(1, len(way)):
            prev_point = way[index - 1]
            curr_point = way[index]
            px, py = self.parse_vertex(prev_point)
            cx, cy = self.parse_vertex(curr_point)

            dx, dy = cx - px, cy - py

            if dx == 1:  # вправо
                result += [1] * ((curr_dir - 0) % 4)
                curr_dir = 0
            elif dx == -1:  # влево
                result += [1] * ((curr_dir - 2) % 4)
                curr_dir = 2
            elif dy == 1:  # вниз
                result += [1] * ((curr_dir - 1) % 4)
                curr_dir = 1
            elif dy == -1:  # вверх
                result += [1] * ((curr_dir - 3) % 4)
                curr_dir = 3

            result.append(0)

        return result



def main():
    # Получаем имена функций
    function_input = FunctionNamesInput()
    function_names = function_input.get_function_names()

    # Получаем веса рёбер
    weight_window = get_weights()

    # Генерируем код
    generator = PathCodeGenerator(function_names, weight_window)
    generator.generate_code()

    messagebox.showinfo("Готово", "Код успешно сгенерирован в файле get_path_func.txt")


if __name__ == "__main__":
    main()
