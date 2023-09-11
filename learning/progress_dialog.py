# progress_dialog.py

from PyQt5.QtWidgets import QDialog, QProgressBar, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt

class ProgressDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("进度对话框")
        
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setAlignment(Qt.AlignCenter)
        self.progress_bar.setRange(0, 100)
        
        self.progress_label = QLabel("", self)
        
        layout = QVBoxLayout()
        layout.addWidget(self.progress_label)
        layout.addWidget(self.progress_bar)
        self.setLayout(layout)
        
    def set_progress(self, value):
        self.progress_bar.setValue(value)
    
    def set_message(self, message):
        self.progress_label.setText(message)
