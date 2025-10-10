import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

# 1. Object Frame
class Frame:
    def __init__(self, root):
        self.root = root
        
    def draw(self, row, col, 
             width=None, height=None, 
             background=None, relief="solid", 
             border=1,
             columnspan=None, rowspan=None,
             padx=10, pady=10):
        """Vẽ khung frame ở tọa độ (row, col)"""
        frame = ttk.Frame(
            self.root,
            width=width, height=height,
            bg=background,
            relief = relief,
            borderwidth=border
        )
        frame.grid(
            column=col, row=row, 
            columnspan=columnspan, rowspan=rowspan,
            padx=padx, pady=pady
        )
        return frame

class Button:
    def __init__(self, frame):
        self.frame = frame
        
    def draw(self, row, col,
             text="",
             background=None, color="black",
             width=25, height=None,
             padx=10, pady=5,
             font="Arial", fontSize=10, fontStyle="normal",
             command=None):
        """Tạo 1 nút button ở tọa độ (row, col)"""
        button = tk.Button(self.frame, text=text, 
                           width=width, height=height, 
                           background=background, 
                           fg=color, font=(font, fontSize, fontStyle),
                           command=command)
        button.grid(row=row, column=col, padx=padx, pady=pady)
        return button

class ImageRooks:
    """Khởi tạo hình ảnh quân xe từ thư mục"""
    def __init__(self):
        self.white = ImageTk.PhotoImage(Image.open("./UI/whiteX.png").resize((60, 60)))
        self.black = ImageTk.PhotoImage(Image.open("./UI/blackX.png").resize((60, 60)))
        self.null = tk.PhotoImage(width=1, height=1)

class Board:
    def __init__(self, frame, n=8):
        self.frame = frame
        self.image = ImageRooks()
        self.n = n
        self.buttons = None         # Vị trí các ô có thể đặt xe
        self.settingRook = True     # Trạng thái hiện tại có đang trong quá trình đặt xe ko
        self.process = []           # List tiến trình đặt xe của thuật toán
        self.speedTime = 200        # Tốc độ của hàng đợi after
        
    def draw(self):
        """Vẽ bàn cờ trắng đen xen kẽ lên frame"""
        buttons = []
        for i in range(self.n):
            row = []
            for j in range(self.n):
                color = "white" if (i + j) % 2 == 0 else "black"
                img = self.image.null                
                btn = tk.Button(self.frame, image=img, width=60, height=60, bg=color,
                                relief="flat", borderwidth=0, highlightthickness=0)
                btn.grid(row=i, column=j, padx=1, pady=1)
                row.append(btn)
            buttons.append(row)
        self.buttons = buttons
        return buttons
    
    def setRooks(self, rooksPos=[]):
        """Đặt các quân xe lên bàn cờ"""
        for i in range(self.n):
            for j in range(self.n):
                self.buttons[i][j].config(image=self.image.null)
        
        if not rooksPos:
            return 
        if isinstance(rooksPos[0], tuple):
            state = rooksPos
        else:
            state = [(row, col) for row, col in enumerate(rooksPos)]

        for row, col in state:
            color = "white" if (row + col) % 2 == 0 else "black"
            img = self.image.white if color == "black" else self.image.black
            self.buttons[row][col].config(image=img)
    
    def setSpeed(self, speedTxt):
        index = int(speedTxt[7:])
        self.speedTime = 200 // index
    
    def setProcess(self, process=[], textProcess=None):
        self.process = process
        """Chạy quá trình đặt quân xe của thuật toán"""
        if not self.settingRook:
            self.settingRook = True
        textProcess.delete("1.0", tk.END)
        for state in process:
            if not self.settingRook:
                return
            self.setRooks(state)
            textProcess.insert(tk.END, str(state) + "\n")
            textProcess.see(tk.END)
            self.frame.update()
            self.frame.after(self.speedTime)
    
    def reset(self):
        """Khởi tạo lại trạng thái ban đầu cho 2 bàn cờ"""
        self.settingRook = False
        self.setRooks()
    
class Label:
    def __init__(self, root):
        self.root = root
    
    def draw(self, row, col, 
             text=None,
             font="Arial", fontSize=16, fontStyle="normal",
             color="black", background=None,
             padx=10, pady=5):
        """Tạo 1 label chứa text lên màn hình"""
        label = tk.Label(
            self.root, text=text, 
            font=(font, fontSize, fontStyle),
            bg=background, fg=color            
        )
        
        label.grid(row=row, column=col, padx=padx, pady=pady)
        return label
    
class ComboBox:
    def __init__(self, frame):
        self.frame = frame

    def draw(self, row, col, 
             values, default="-------------------Choose Algorithm-------------------", 
             width=20, padx=10, pady=5):
        """Tạo 1 combo box chứa các giá trị trong values"""
        if default not in values:
            values = [default] + values
        
        comboBox = ttk.Combobox(self.frame, values=values, width=width, state="readonly")
        comboBox.set(default)
        comboBox.grid(row=row, column=col, padx=padx, pady=pady)
        return comboBox
    
class Text:
    def __init__(self, frame):
        self.frame = frame
        self.label = None

    def draw(self, row, col,
             width=25, height = 30,
             anchor="nw", padx=5, pady=5):
        """Tạo 1 hộp text để xem tiến trình đặt xe hiện tại"""
        label = tk.Text(self.frame, width=width, height=height)
        label.pack(anchor=anchor, padx=padx, pady=pady)
        
        self.label = label
        return label