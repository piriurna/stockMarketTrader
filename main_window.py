from PyQt5.QtWidgets import QMainWindow, QTabWidget, QVBoxLayout, QWidget, QLineEdit, QPushButton, QHBoxLayout, \
    QCheckBox, QScrollArea

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar

from analysis.stock_analysis import analyze_combined_stock_data


def create_tab(window, figure):
    tab = QWidget()
    vbox = QVBoxLayout()

    canvas = FigureCanvas(figure)
    vbox.addWidget(canvas)
    tab.setLayout(vbox)
    tab.toolbar = NavigationToolbar(canvas, tab)

    return tab


class MainWindow(QMainWindow):
    def __init__(self, figures, refresh_callback, stock_symbols, visible_search=True):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Stock Market Analysis")
        self.setGeometry(100, 100, 1200, 600)

        self.refresh_callback = refresh_callback

        self.tabs_widget = QTabWidget()

        for i, figure in enumerate(figures):
            self.tabs_widget.addTab(create_tab(self, figure), f"Figure {i + 1}")

        self.central_widget = QWidget()
        self.central_layout = QVBoxLayout(self.central_widget)

        if visible_search:
            self.search_bar = QLineEdit()
            self.search_button = QPushButton("Refresh")
            self.search_button.clicked.connect(self.refresh)

            self.search_layout = QHBoxLayout()
            self.search_layout.addWidget(self.search_bar)
            self.search_layout.addWidget(self.search_button)

            self.central_layout.addLayout(self.search_layout)
            self.central_layout.addWidget(self.tabs_widget)
            self.setCentralWidget(self.central_widget)
            self.search_bar.returnPressed.connect(self.refresh)

        self.stock_symbols = stock_symbols
        self.symbol_checkboxes = {}

        self.checkbox_container = QWidget()
        self.checkbox_layout = QVBoxLayout()

        for symbol in self.stock_symbols:
            checkbox = QCheckBox(symbol)
            checkbox.setChecked(True)
            self.symbol_checkboxes[symbol] = checkbox
            self.checkbox_layout.addWidget(checkbox)
            checkbox.toggled.connect(self.refresh_toggle)

        self.checkbox_container.setLayout(self.checkbox_layout)

        scroll = QScrollArea()
        scroll.setWidget(self.checkbox_container)
        scroll.setWidgetResizable(True)
        scroll.setFixedHeight(100)

        self.central_layout.addWidget(scroll)
        self.central_layout.addWidget(self.tabs_widget)
        self.setCentralWidget(self.central_widget)

    def get_selected_symbols(self):
        return [symbol for symbol, checkbox in self.symbol_checkboxes.items() if checkbox.isChecked()]

    def refresh_toggle(self):
        figures = self.refresh_callback(self.get_selected_symbols())
        self.update_tabs(figures)

    def refresh(self):
        symbol = self.search_bar.text()
        figures = self.refresh_callback([symbol])
        self.update_tabs(figures)

    def update_tabs(self, figures):
        for i in range(self.tabs_widget.count()):
            self.tabs_widget.removeTab(0)
            plt.close()  # Close the figure after removing the tab

        for i, figure in enumerate(figures):
            self.tabs_widget.addTab(create_tab(self, figure), f"Figure {i + 1}")
