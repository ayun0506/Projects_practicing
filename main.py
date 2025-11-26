#tkinter의 루트 윈도우 생성하고, TodoListApp의 인스턴스 생성
#애플리케이션의 이벤트 루프 시작

import tkinter as tk
from TodoListApp import TodoListApp

def main():
    root = tk.Tk()
    app = TodoListApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()