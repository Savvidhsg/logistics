import sys
from PyQt6.QtWidgets import QApplication
from ui import StorageMap
import database

if __name__ == "__main__":
    database.init_db()
    
    app = QApplication(sys.argv)
    window = StorageMap()
    window.show()
    sys.exit(app.exec())
