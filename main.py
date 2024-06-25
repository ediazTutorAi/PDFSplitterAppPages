import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QFileDialog, QMessageBox, QComboBox, QAction)
from PyQt5.QtCore import Qt
from PyPDF2 import PdfReader, PdfWriter

class PDFSplitterApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDFSplitter")
        self.setGeometry(100, 100, 400, 200)
        
        self.init_ui()
        self.create_menu_bar()
    
    def init_ui(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.input_pdf_label = QLabel("Select PDF file:")
        self.layout.addWidget(self.input_pdf_label)

        self.input_pdf_path = QLineEdit()
        self.layout.addWidget(self.input_pdf_path)

        self.input_pdf_button = QPushButton("Browse...")
        self.input_pdf_button.clicked.connect(self.browse_input_pdf)
        self.layout.addWidget(self.input_pdf_button)

        self.output_dir_label = QLabel("Select Output Directory:")
        self.layout.addWidget(self.output_dir_label)

        self.output_dir_path = QLineEdit()
        self.layout.addWidget(self.output_dir_path)

        self.output_dir_button = QPushButton("Browse...")
        self.output_dir_button.clicked.connect(self.browse_output_dir)
        self.layout.addWidget(self.output_dir_button)

        self.split_by_label = QLabel("Split PDF by number of pages:")
        self.layout.addWidget(self.split_by_label)

        self.split_by_combobox = QComboBox()
        self.split_by_combobox.addItems(["1", "2", "3", "4", "5","6","7","8","9","10","11","12"])
        self.layout.addWidget(self.split_by_combobox)

        self.split_button = QPushButton("Split PDF")
        self.split_button.clicked.connect(self.split_pdf)
        self.layout.addWidget(self.split_button)

    def create_menu_bar(self):
        # Create the menubar
        menubar = self.menuBar()

        # Add a "File" menu
        file_menu = menubar.addMenu("File")

        # Add "Open" action
        open_action = QAction("Open PDF", self)
        open_action.triggered.connect(self.browse_input_pdf)
        file_menu.addAction(open_action)

        # Add "Save As" action
        save_as_action = QAction("Save As...", self)
        save_as_action.triggered.connect(self.browse_output_dir)
        file_menu.addAction(save_as_action)

        # Add "Exit" action
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Add a "Help" menu
        help_menu = menubar.addMenu("Help")

        # Add "About" action
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about_dialog)
        help_menu.addAction(about_action)

    def show_about_dialog(self):
        QMessageBox.about(self, "About PDFSplitter", "PDFSplitter\nVersion 1.0\nA simple tool to split PDFs into smaller parts.")

    def browse_input_pdf(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select PDF File", "", "PDF Files (*.pdf)")
        if file_path:
            self.input_pdf_path.setText(file_path)

    def browse_output_dir(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Output Directory")
        if directory:
            self.output_dir_path.setText(directory)

    def split_pdf(self):
        input_pdf = self.input_pdf_path.text()
        output_dir = self.output_dir_path.text()
        split_by = int(self.split_by_combobox.currentText())

        if not input_pdf or not output_dir:
            QMessageBox.warning(self, "Error", "Please specify both input PDF and output directory.")
            return

        if not os.path.isfile(input_pdf):
            QMessageBox.warning(self, "Error", "The specified input PDF does not exist.")
            return

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        try:
            self.perform_split_pdf(input_pdf, output_dir, split_by)
            QMessageBox.information(self, "Success", "PDF has been split successfully.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred while splitting the PDF: {e}")

    def perform_split_pdf(self, input_pdf, output_dir, split_by):
        pdf_reader = PdfReader(open(input_pdf, 'rb'))
        total_pages = len(pdf_reader.pages)

        step = split_by

        for i in range(0, total_pages, step):
            pdf_writer = PdfWriter()

            for j in range(step):
                if i + j < total_pages:
                    pdf_writer.add_page(pdf_reader.pages[i + j])

            folder_name = os.path.join(output_dir, f"folder_{i // step + 1}")
            if not os.path.exists(folder_name):
                os.makedirs(folder_name)

            output_pdf_path = os.path.join(folder_name, f"output_{i // step + 1}.pdf")
            with open(output_pdf_path, 'wb') as output_pdf:
                pdf_writer.write(output_pdf)

            print(f"Saved {output_pdf_path}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("PDFSplitter")  # Set the application name
    window = PDFSplitterApp()
    window.show()
    sys.exit(app.exec_())
