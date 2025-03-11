from PyQt6.QtWidgets import QWidget, QPushButton, QGridLayout, QSizePolicy, QVBoxLayout, QTableWidget, QTableWidgetItem, QInputDialog
from PyQt6.QtCore import Qt
import sqlite3
from database import update_slot  

class StorageMap(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Storage Map")
        self.setGeometry(100, 100, 600, 600)

        # Initialize database and create default slots
        from database import init_db
        init_db()  # Initialize DB and create default slots if necessary

        # Storage unit numbers
        self.unit_numbers = [
            [8, 7, 6, 5, 4, 3, 2, 1],  # Column 1
            [16, 15, 14, 13, 12, 11, 10, 9],  # Column 2
            [24, 23, 22, 21, 20, 19, 18, 17],  # Column 3
            [32, 31, 30, 29, 28, 27, 26, 25]  # Column 4
        ]

        self.buttons = {}
        grid_layout = QGridLayout()
        grid_layout.setHorizontalSpacing(15)
        grid_layout.setVerticalSpacing(0)
        grid_layout.setContentsMargins(0, 0, 0, 0)
        grid_layout.setSpacing(0)

        # Create buttons and initialize button colors based on status
        conn = sqlite3.connect("storage.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, status FROM slots")
        slot_status = cursor.fetchall()  # [(id, status), ...]

        # Create the buttons for each slot and set their colors based on status
        for col, units in enumerate(self.unit_numbers):
            for row, num in enumerate(units):
                # Create the button
                btn = QPushButton(f"{num:02d}")
                btn.setFixedSize(50, 50)
                btn.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

                # Set button color based on the status
                status = next(status for id, status in slot_status if id == num)  # Get the status of this button's slot
                if status == "not available":
                    btn.setStyleSheet("background-color: red; color: white; font-weight: bold;")
                else:
                    btn.setStyleSheet("background-color: green; color: white; font-weight: bold;")
                
                # Connect the button click to toggle its status
                btn.clicked.connect(lambda _, b=btn, n=num: self.toggle_status(b, n))

                grid_layout.addWidget(btn, row, col, alignment=Qt.AlignmentFlag.AlignCenter)
                self.buttons[num] = btn

        conn.close()

        # Table for occupied slots
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Slot", "Name", "Date"])
        self.load_table()

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.addLayout(grid_layout)
        main_layout.addWidget(self.table)
        self.setLayout(main_layout)

    def toggle_status(self, btn, slot_id):
        current_style = btn.styleSheet()
        if "green" in current_style:
            name, ok1 = QInputDialog.getText(self, "Enter Name", "Name:")
            date, ok2 = QInputDialog.getText(self, "Enter Date", "Date:")
            if ok1 and ok2 and name and date:
                btn.setStyleSheet("background-color: red; color: white; font-weight: bold;")
                update_slot(slot_id, "not available", name, date)  # Update the slot with the data
        else:
            btn.setStyleSheet("background-color: green; color: white; font-weight: bold;")
            update_slot(slot_id, "available", "", "")  # Reset the slot to available
        self.load_table()  # Reload the table after update

    def load_table(self):
        conn = sqlite3.connect("storage.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, date FROM slots WHERE status = 'not available'")
        slots = cursor.fetchall()
        conn.close()

        # Ensure we have enough rows for the fetched data
        self.table.setRowCount(len(slots))

        # Insert the data into the table
        for row, (slot_id, name, date) in enumerate(slots):
            self.table.setItem(row, 0, QTableWidgetItem(str(slot_id)))  # Slot ID
            self.table.setItem(row, 1, QTableWidgetItem(name))          # Name
            self.table.setItem(row, 2, QTableWidgetItem(date))          # Date
