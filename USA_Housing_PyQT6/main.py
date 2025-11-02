import sys
from PyQt6.QtWidgets import QApplication
from UIPrediction import UIPrediction

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = UIPrediction()
    window.show()
    sys.exit(app.exec())