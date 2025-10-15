from tkinter import messagebox
from UI.UiComponent import Frame, Button, Board, Label, ComboBox, Text
from Algorithm import Algorithm
import tkinter as tk
import tkextrafont

# Biến toàn cục cho chương trình
N = 8

if __name__=="__main__":
# -----------GIAO DIỆN--------------
    # Khởi tạo giao diện
    root = tk.Tk()
    root.title("8 rooks")
    scrW = root.winfo_screenwidth()
    scrH = root.winfo_screenheight()

    # Nạp font chữ
    _font = tkextrafont.Font(file="UI/font/MinecraftTen-VGORe.ttf", family="Minecraft Ten")
    fontMinecraft = "Minecraft Ten"

    # Tạo tiêu đề
    frameTitle = Frame(root).draw(0, 0, columnspan=3, border=0, relief="flat")
    title = Label(frameTitle)
    title.draw(0, 0, text="8 ROOKS", font=fontMinecraft, fontSize=30)

    # Tạo 1 label text bên trái để xem các trạng thái đặt xe
    frameLabelProcess = Frame(root).draw(1, 0)
    LabelProcess = Text(frameLabelProcess).draw(0, 0)
    
    # Tạo 2 bàn cờ trống trái - phải
    frameBoardLeft = Frame(root).draw(1, 1)
    BoardLeft = Board(frameBoardLeft)
    posLeft = BoardLeft.draw()  # Vị trí quân xe trên bàn cờ trái

    frameBoardRight = Frame(root).draw(1, 2)
    BoardRight = Board(frameBoardRight)
    posRight = BoardRight.draw() # Vị trí quân xe trên bàn cờ phải

    # Tạo các button
    frameButtonLeft = Frame(root).draw(2, 1, border=0, relief="flat")
    frameButtonRight = Frame(root).draw(2, 2, border=0, relief="flat")

    PathBtn = Button(frameButtonLeft).draw(0, 1, text="Path", background="lightgreen", width=8, height=1, fontSize=13)
    ResetBtn = Button(frameButtonLeft).draw(0, 2, text="Reset", background="red", color="white", width=8, height=1, fontSize=13)
    speedBtn = Button(frameButtonLeft).draw(0, 0, text="Speed x1", background="lightgreen", width=10, height=1, fontSize=13)
    RunBtn = Button(frameButtonRight).draw(1, 0, text="Run", background="cyan", width=8, height=1, fontSize=13)

    # Tạo combo box chọn thuật toán
    algorithmName = ["BFS", "DFS", "DLS", "IDS", "UCS",
                     "Greedy", "A*",
                     "Hill - Climbing", "Simulated Annealing", "Genetic Algorithm", "Beam Search",
                     "AND-OR Tree Search", "Belief State Search", "Partially Observable Spaces",
                     "Backtracking", "Forward Checking", "AC-3"]
    comboBoxAlgorithm = ComboBox(frameButtonRight)
    cbb = comboBoxAlgorithm.draw(0, 0, values=algorithmName, width=45)

# ------------HÀM THỰC THI--------------
    path = []
    process = []
    speeds = ["Speed x1", "Speed x2", "Speed x3", "Speed x5", "Speed x10", "Speed x20", "Speed x100"]
    speedIndex = 0
    # Chạy thuật toán đã chọn
    def runClick():
        global path, process
        selectValue = cbb.get()

        if selectValue.startswith("----"):
            messagebox.showwarning("Thông báo", "Bạn chưa chọn thuật toán!")
            return
        
        runReset()
        path, process= Algorithm.run(selectValue, n=N)
        if path:
            BoardRight.setRooks(path)
        else:
            messagebox.showwarning("Thông báo", "Không đặt được 8 quân xe!")
            return
    
    # Đặt lần lượt từng quân xe như cách thuật toán đã làm
    def runPath():
        BoardLeft.setProcess(process, textProcess=LabelProcess)
    
    # Reset 2 bàn cờ về trạng thái ban đầu
    def runReset():
        global path, process, speedIndex
        path = []
        process = []
        BoardLeft.process = []
        BoardRight.process = []
        BoardLeft.reset()
        BoardRight.reset()
        LabelProcess.delete("1.0", tk.END)
    
    # Thay đổi tốc độ đặt quân xe
    def changeSpeed():
        global speedIndex
        speedIndex = (speedIndex + 1) % len(speeds)
        speedBtn.config(text=speeds[speedIndex])
        BoardLeft.setSpeed(speeds[speedIndex])
    
    RunBtn.config(command=runClick)
    PathBtn.config(command=runPath)
    speedBtn.config(command=changeSpeed)
    ResetBtn.config(command=runReset)
    
    # Điều chỉnh vị trí xuất hiện của màn hình
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    root.geometry(f"{width}x{height}+{(scrW - width) // 2}+{(scrH - height - 100) // 2}")
    root.mainloop()