import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QTextEdit, QPushButton, QLabel)
from PyQt5.QtGui import QTextCursor, QTextCharFormat, QColor, QFont, QPalette

class RichTextFormatter(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Rich Text Code Formatter with Line Numbers (PyQt5)')
        self.setGeometry(100, 100, 1000, 700)

        # Main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Instructions
        self.label = QLabel("Paste your rich text code below, then click 'Process' to add white line numbers.")
        main_layout.addWidget(self.label)

        # Text boxes layout
        text_layout = QHBoxLayout()
        
        # Input Box
        self.input_box = QTextEdit()
        self.input_box.setPlaceholderText("Paste rich text code here...")
        self.input_box.setAcceptRichText(True)
        
        # Output Box
        self.output_box = QTextEdit()
        self.output_box.setPlaceholderText("Formatted code will appear here...")
        self.output_box.setReadOnly(True)
        
        # Set a dark background for the output to make white line numbers visible
        palette = self.output_box.palette()
        # In PyQt5, ColorRole is accessed via QPalette directly or QPalette.Base
        palette.setColor(QPalette.Base, QColor(30, 30, 30))
        palette.setColor(QPalette.Text, QColor(255, 255, 255))
        self.output_box.setPalette(palette)

        text_layout.addWidget(self.input_box)
        text_layout.addWidget(self.output_box)
        main_layout.addLayout(text_layout)

        # Buttons layout
        button_layout = QHBoxLayout()
        
        # Process Button
        self.process_btn = QPushButton("Process and Add Line Numbers")
        self.process_btn.clicked.connect(self.process_text)
        button_layout.addWidget(self.process_btn)
        
        # Copy Button
        self.copy_btn = QPushButton("Copy Result to Clipboard")
        self.copy_btn.clicked.connect(self.copy_to_clipboard)
        button_layout.addWidget(self.copy_btn)
        
        main_layout.addLayout(button_layout)

    def process_text(self):
        # Clear output
        self.output_box.clear()
        
        input_doc = self.input_box.document()
        output_cursor = self.output_box.textCursor()
        
        # Format for line numbers
        line_num_format = QTextCharFormat()
        line_num_format.setForeground(QColor("white"))
        line_num_format.setFont(QFont("Courier New", 10))

        block = input_doc.begin()
        line_count = 1
        
        while block.isValid():
            # 1. Insert line number
            output_cursor.setCharFormat(line_num_format)
            output_cursor.insertText("{:3}  ".format(line_count))
            
            # 2. Insert original block content with formatting
            it = block.begin()
            while not it.atEnd():
                fragment = it.fragment()
                if fragment.isValid():
                    output_cursor.setCharFormat(fragment.charFormat())
                    output_cursor.insertText(fragment.text())
                it += 1
            
            block = block.next()
            if block.isValid():
                output_cursor.insertBlock()
                line_count += 1

        # Move cursor to start of output
        self.output_box.moveCursor(QTextCursor.Start)

    def copy_to_clipboard(self):
        # Select all and copy
        self.output_box.selectAll()
        self.output_box.copy()
        # Deselect
        cursor = self.output_box.textCursor()
        cursor.clearSelection()
        self.output_box.setTextCursor(cursor)
        self.label.setText("Result copied to clipboard with rich text formatting!")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = RichTextFormatter()
    ex.show()
    sys.exit(app.exec_())
