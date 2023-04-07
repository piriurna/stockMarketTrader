from PyQt5.QtWidgets import QMainWindow, QTabWidget, QVBoxLayout, QWidget, QLineEdit, QPushButton, QHBoxLayout

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


def create_tab(figure):
    tab = QWidget()
    vbox = QVBoxLayout()

    canvas = FigureCanvas(figure)
    vbox.addWidget(canvas)

    tab.setLayout(vbox)

    return tab


class MainWindow(QMainWindow):
    def __init__(self, figures, refresh_callback):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Stock Market Analysis")
        self.setGeometry(100, 100, 1200, 600)

        self.refresh_callback = refresh_callback

        self.tabs_widget = QTabWidget()

        for i, figure in enumerate(figures):
            self.tabs_widget.addTab(create_tab(figure), f"Figure {i + 1}")

        self.central_widget = QWidget()
        self.central_layout = QVBoxLayout(self.central_widget)

        self.search_bar = QLineEdit()
        self.search_button = QPushButton("Refresh")
        self.search_button.clicked.connect(self.refresh)

        self.search_layout = QHBoxLayout()
        self.search_layout.addWidget(self.search_bar)
        self.search_layout.addWidget(self.search_button)

        self.central_layout.addLayout(self.search_layout)
        self.central_layout.addWidget(self.tabs_widget)
        self.setCentralWidget(self.central_widget)

    def refresh(self):
        symbol = self.search_bar.text()
        figures = self.refresh_callback(symbol)

        for i in range(self.tabs_widget.count()):
            self.tabs_widget.removeTab(0)
            plt.close()  # Close the figure after removing the tab

        for i, figure in enumerate(figures):
            self.tabs_widget.addTab(create_tab(figure), f"Figure {i + 1}")
