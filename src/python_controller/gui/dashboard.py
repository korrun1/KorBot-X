from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QComboBox, QProgressBar, QTextEdit
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPalette, QColor
import sys
from threading import Thread
from bot import run_bot  # Import run_bot from bot.py

class KorBotDashboard(QMainWindow):
    # ... (the rest of the code remains the same)
    def __init__(self):
        super().__init__()
        self.setWindowTitle("KorBot X Dashboard")
        self.setGeometry(100, 100, 800, 600)
        self.set_dark_mode()  # Call it here
        self.init_ui()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_dashboard)
        self.timer.start(5000)  # Update every 5 seconds
        self.bot_thread = None

    def set_dark_mode(self):
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.Base, QColor(25, 25, 25))
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor(53, 53, 53))
        palette.setColor(QPalette.ColorRole.ToolTipBase, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.ToolTipText, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.Button, QColor(53, 53, 53))
        palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.BrightText, Qt.GlobalColor.red)
        palette.setColor(QPalette.ColorRole.Link, QColor(42, 130, 218))
        palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.black)
        QApplication.setPalette(palette)

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Overview Panel
        overview_label = QLabel("Overview")
        layout.addWidget(overview_label)
        self.equity_label = QLabel("Equity: $10000")
        layout.addWidget(self.equity_label)
        self.floating_pl = QLabel("Floating P/L: $0")
        layout.addWidget(self.floating_pl)
        self.drawdown_bar = QProgressBar()
        self.drawdown_bar.setValue(5)
        layout.addWidget(self.drawdown_bar)

        # Strategy Panel
        strategy_label = QLabel("Strategy Control")
        layout.addWidget(strategy_label)
        self.strategy_combo = QComboBox()
        self.strategy_combo.addItems(["Scalping", "Mean Reversion", "Breakout", "Swing"])
        layout.addWidget(self.strategy_combo)
        self.start_button = QPushButton("Start Bot")
        self.start_button.clicked.connect(self.start_bot)
        layout.addWidget(self.start_button)
        self.stop_button = QPushButton("Stop Bot")
        self.stop_button.clicked.connect(self.stop_bot)
        layout.addWidget(self.stop_button)

        # Log Panel
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        layout.addWidget(self.log_text)

    def update_dashboard(self):
        # Placeholder update (integrate real data later)
        self.equity_label.setText("Equity: $10500")
        self.floating_pl.setText("Floating P/L: +$500")
        self.drawdown_bar.setValue(3)
        self.log_text.append("Dashboard updated.")

    def start_bot(self):
        self.log_text.append("Starting KorBot X...")
        self.bot_thread = Thread(target=run_bot)
        self.bot_thread.start()

    def stop_bot(self):
        self.log_text.append("Stopping KorBot X...")
        # Add logic to stop thread if needed

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = KorBotDashboard()
    window.show()
    sys.exit(app.exec())