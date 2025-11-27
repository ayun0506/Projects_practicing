#할 일 객체로 생성해서 데이터 관리 클래스
#(리스트를 파일로 저장 및 읽기 기능 위함)

class Todo:
    def __init__(self, task, deadline, completed=False):
        self.task = task
        self.deadline = deadline
        self.completed = completed
    def toggle_completed(self):
        self.completed = not self.completed
