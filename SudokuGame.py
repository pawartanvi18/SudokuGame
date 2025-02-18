import sys
import random
import numpy as np
from PyQt6.QtWidgets import (QApplication, QWidget, QGridLayout, QPushButton, QLineEdit, QLabel, QVBoxLayout, QHBoxLayout)
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QFont, QPalette, QColor

class SudokuGame(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sudoku Game")
        self.grid_size = 9
        self.mistakes = 0
        self.max_mistakes = 3
        self.timer = QTimer()
        self.time_elapsed = 0
        self.timer.timeout.connect(self.update_timer)
        self.init_ui()
        self.new_game()

    def init_ui(self):
        main_layout = QVBoxLayout()
        self.grid_layout = QGridLayout()
        self.cells = [[QLineEdit(self) for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                cell = self.cells[i][j]
                cell.setMaxLength(1)
                cell.setFixedSize(50, 50)
                cell.setFont(QFont("Arial", 16))
                cell.setAlignment(Qt.AlignmentFlag.AlignCenter)
                cell.textChanged.connect(lambda text, x=i, y=j: self.validate_input(x, y, text))
                cell.setStyleSheet(self.get_cell_style(i, j))
                self.grid_layout.addWidget(cell, i, j)
                
        main_layout.addLayout(self.grid_layout)
        
        info_layout = QHBoxLayout()
        self.mistakes_label = QLabel("Mistakes: 0 / 3")
        self.timer_label = QLabel("Time: 00:00")
        info_layout.addWidget(self.mistakes_label)
        info_layout.addWidget(self.timer_label)
        main_layout.addLayout(info_layout)
        
        self.number_buttons = QHBoxLayout()
        for num in range(1, 10):
            btn = QPushButton(str(num))
            btn.setFixedSize(40, 40)
            btn.clicked.connect(lambda _, n=num: self.insert_number(n))
            self.number_buttons.addWidget(btn)
        main_layout.addLayout(self.number_buttons)
        
        self.new_game_button = QPushButton("New Game")
        self.new_game_button.clicked.connect(self.new_game)
        main_layout.addWidget(self.new_game_button)
        
        self.setLayout(main_layout)
    
    def get_cell_style(self, row, col):
        style = "border: 1px solid black; font-size: 18px;"
        if row % 3 == 0 and row != 0:
            style += "border-top: 3px solid black;"
        if col % 3 == 0 and col != 0:
            style += "border-left: 3px solid black;"
        if row == 8:
            style += "border-bottom: 3px solid black;"
        if col == 8:
            style += "border-right: 3px solid black;"
        return style
    
    def new_game(self):
        self.board = self.generate_sudoku()
        self.solution = np.copy(self.board)
        self.mistakes = 0
        self.time_elapsed = 0
        self.mistakes_label.setText("Mistakes: 0 / 3")
        self.timer_label.setText("Time: 00:00")
        self.timer.start(1000)
        
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                cell = self.cells[i][j]
                cell.setStyleSheet(self.get_cell_style(i, j))
                if self.board[i][j] != 0:
                    cell.setText(str(self.board[i][j]))
                    cell.setReadOnly(True)
                else:
                    cell.setText("")
                    cell.setReadOnly(False)
    
    def generate_sudoku(self):
        board = np.zeros((9, 9), dtype=int)
        for _ in range(17):
            row, col = random.randint(0, 8), random.randint(0, 8)
            num = random.randint(1, 9)
            if board[row][col] == 0 and self.is_valid(board, row, col, num):
                board[row][col] = num
        return board
    
    def is_valid(self, board, row, col, num):
        if num in board[row]:
            return False
        if num in board[:, col]:
            return False
        box_x, box_y = (row // 3) * 3, (col // 3) * 3
        if num in board[box_x:box_x+3, box_y:box_y+3]:
            return False
        return True
    
    def validate_input(self, row, col, text):
        if text.isdigit():
            num = int(text)
            if self.solution[row][col] == 0:
                if not self.is_valid(self.solution, row, col, num):
                    self.mistakes += 1
                    self.mistakes_label.setText(f"Mistakes: {self.mistakes} / 3")
                    if self.mistakes >= self.max_mistakes:
                        self.new_game()
    
    def insert_number(self, num):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if self.cells[i][j].hasFocus():
                    self.cells[i][j].setText(str(num))
                    return
    
    def update_timer(self):
        self.time_elapsed += 1
        minutes, seconds = divmod(self.time_elapsed, 60)
        self.timer_label.setText(f"Time: {minutes:02}:{seconds:02}")
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SudokuGame()
    window.show()
    sys.exit(app.exec())
