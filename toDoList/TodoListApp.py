#GUI를 구성하기 위한 클래스
#할 일 목록을 저장하는 변수와 기능들을 정의하는 메서드로 구성
from Todo import Todo
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog

class TodoListApp:
    def __init__(self, root):
        self.root = root #tkinter의 루트 윈도우
        self.root.title("Todo List App")
        self.todo_list = [] #할일 목록을 저장하는 리스트

        self.create_widgets()

    #GUI 위젯 생성 메서드
    def create_widgets(self):
        self.list_frame = tk.Frame(self.root) #프레임(화면)을 생성
        self.list_frame.pack(side=tk.LEFT,padx=10,pady=10) #프레임 안 왼쪽/위쪽 10씩 여백 부여 //그 위치에 아래 리스트박스 등 생성됨

        self.todo_listbox = tk.Listbox(self.list_frame, width=40)
        self.todo_listbox.pack(side=tk.LEFT, fill=tk.BOTH)
        self.todo_listbox.bind("<<ListboxSelect>>", self.on_item_select)

        self.scrollbar = tk.Scrollbar(self.list_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y) #오른쪽에 메뉴 생성
        self.todo_listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.todo_listbox.yview)

        self.entry_frame = tk.Frame(self.root) #오른쪽에 프레임 생성
        self.entry_frame.pack(side=tk.RIGHT, padx=10, pady=10)

        self.task_label = tk.Label(self.entry_frame, text="할일")
        self.task_label.pack()
        self.task_entry = tk.Entry(self.entry_frame, width=30)
        self.task_entry.pack()

        self.deadline_label = tk.Label(self.entry_frame, text="마감일")
        self.deadline_label.pack()
        self.deadline_entry = tk.Entry(self.entry_frame, width=30)
        self.deadline_entry.pack()

        self.add_button = tk.Button(self.entry_frame, text="할일 추가", command=self.add_todo_item)
        self.add_button.pack(pady=10)
        self.mark_completed_button = tk.Button(self.entry_frame, text="완료 상태 변경", command=self.mark_completed)
        self.mark_completed_button.pack()

        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)
        self.file_menu = tk.Menu(self.menu, tearoff=False)
        self.menu.add_cascade(label="파일", menu=self.file_menu)
        self.file_menu.add_command(label="저장", command=self.save_todo_list)
        self.file_menu.add_command(label="불러오기", command=self.load_todo_list)
        self.file_menu.add_command(label="종료", command=self.root.quit)

    #입력된 할일 데이터를 기반으로 새로운 할일을 추가하는 메서드
    def add_todo_item(self):
        task = self.task_entry.get()
        deadline = self.deadline_entry.get()

        if task and deadline: #할일, 마감일 동시 만족할 시
            self.todo_list.append(Todo(task, deadline)) #Todo메서드 안에 할일과 마감일 추가
            self.update_listbox()
            self.task_entry.delete(0, tk.END)
            self.deadline_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("경고", "할일과 마감일을 입력하세요.")

    #할일 목록을 업데이트하여 Listbox위젯에 표시하는 메서드
    def update_listbox(self):
        self.todo_listbox.delete(0, tk.END)
        for item in self.todo_list:
            status = "완료" if item.completed else "진행중"
            self.todo_listbox.insert(tk.END, f"{item.task} (마감일: {item.deadline}, 상태: {status})")

    #Listbox에서 항목이 선택될 때 호출되는 이벤트 처리 메서드
    def on_item_select(self, event):
        selection = self.todo_listbox.curselection()
        if selection:
            self.selected_index = selection[0]
        else:
            self.selected_inidex = None

    #선택한 할일 항목의 완료 상태를 변경하는 메서드
    def mark_completed(self):
        if self.selected_index is not None:
            item = self.todo_list[self.selected_index]
            item.toggle_completed()
            self.update_listbox()

    #할일 목록을 파일에 저장하는 메서드
    def save_todo_list(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt")
        if file_path:
            try:
                with open(file_path, "w") as file:
                    for item in self.todo_list:
                        file.write(f"{item.task},{item.deadline},{item.completed}\n")
                    messagebox.showinfo("저장완료", "할일 목록이 저장되었습니다.")
            except Exception as e:
                messagebox.showerror("에러", str(e))

    #파일에서 할 일 목록을 불러오는 메서드
    def load_todo_list(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            try:
                self.todo_list = []
                with open(file_path, "r") as file:
                    lines = file.readlines()
                    for line in lines:
                        parts = line.strip().split(",")
                        task = parts[0]
                        deadline = parts[1]
                        completed = parts[2] == "True"
                        self.todo_list.append(Todo(task, deadline, completed))
                    self.update_listbox()
                    messagebox.showinfo("불러오기 완료", "할일 목록을 읽어왔습니다.")
            except Exception as e:
                messagebox.showerror("에러", str(e))

