import sys
import numpy as np
import matplotlib.pyplot as plt
from math import pi, sin, cos, tan, exp, log, sqrt
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget


def cot(x):
    return 1 / tan(x)


data = {
    'pi': pi,
    'sin': sin,
    'cos': cos,
    'tan': tan,
    'cot': cot,
    'exp': exp,
    'log': log,
    'sqrt': sqrt
}

class Graph(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Приложение для построения графиков")
        self.setGeometry(100, 100, 400, 250)
        widget = QWidget(self)
        self.setCentralWidget(widget)
        layout = QVBoxLayout()
        widget.setLayout(layout)
        func_label = QLabel("Введите выражение для y:")
        self.func_entry = QLineEdit()
        x_start_label = QLabel("Начальное значение x:")
        self.x_start_entry = QLineEdit()
        x_finish_label = QLabel("Конечное значение x:")
        self.x_finish_entry = QLineEdit()
        count_points_label = QLabel("Количество точек:")
        self.count_points_entry = QLineEdit()
        plot_button = QPushButton("Построить график")
        plot_button.clicked.connect(self.plot_graph)
        layout.addWidget(func_label)
        layout.addWidget(self.func_entry)
        layout.addWidget(x_start_label)
        layout.addWidget(self.x_start_entry)
        layout.addWidget(x_finish_label)
        layout.addWidget(self.x_finish_entry)
        layout.addWidget(count_points_label)
        layout.addWidget(self.count_points_entry)
        layout.addWidget(plot_button)

    def plot_graph(self):
        x_start = float(self.x_start_entry.text())
        x_finish = float(eval(self.x_finish_entry.text(), data))
        count_points = int(self.count_points_entry.text())

        x_values = np.linspace(x_start, x_finish, count_points)
        y = self.func_entry.text()
        y_values = [eval(y, data, {'x': x}) for x in x_values]

        plt.plot(x_values, y_values)
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title(f'График функции {y}')
        plt.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Graph()
    window.show()
    sys.exit(app.exec_())
