import data_set as ds
from PyQt6.QtWidgets import (
    QApplication,
    QComboBox,
    QLabel,
    QPushButton,
    QWidget,
    QFileDialog,
    QListWidget
)


class Absolute(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.setWindowTitle('Data set creator')
        self.setFixedSize(630, 380)

        # ------------------------------CLASS 1----------------------------------------
        self.label_1 = QLabel('CLASS 1', self)
        self.label_1.setFixedSize(100, 25)
        self.label_1.move(150, 20)

        self.list_1 = QListWidget(self)
        self.list_1.setFixedSize(250, 230)
        self.list_1.move(50, 50)

        self.add_1 = QPushButton('add', self)
        self.add_1.setFixedSize(60, 25)
        self.add_1.move(180, 280)
        self.add_1.clicked.connect(self.add_class_1)

        self.delete_1 = QPushButton('delete', self)
        self.delete_1.setFixedSize(60, 25)
        self.delete_1.move(240, 280)
        self.delete_1.clicked.connect(self.delete_class_1)

        # ------------------------------CLASS 2----------------------------------------
        self.label_2 = QLabel('CLASS 2', self)
        self.label_2.setFixedSize(100, 25)
        self.label_2.move(430, 20)

        self.list_2 = QListWidget(self)
        self.list_2.setFixedSize(250, 230)
        self.list_2.move(330, 50)

        self.add_2 = QPushButton('add', self)
        self.add_2.setFixedSize(60, 25)
        self.add_2.move(460, 280)
        self.add_2.clicked.connect(self.add_class_2)

        self.delete_2 = QPushButton('delete', self)
        self.delete_2.setFixedSize(60, 25)
        self.delete_2.move(520, 280)
        self.delete_2.clicked.connect(self.delete_class_2)
        # ---------------------------------------------------------------------------
        self.button_start = QPushButton('Create data', self)
        self.button_start.setFixedSize(100, 25)
        self.button_start.move(215, 330)
        self.button_start.clicked.connect(self.create_data)

        self.button_clear = QPushButton('Clear table', self)
        self.button_clear.setFixedSize(100, 25)
        self.button_clear.move(315, 330)
        self.button_clear.clicked.connect(self.clear)

        self.last_path = "D:/source x4/dataRGB/"
        self.dir_class_1 = list()
        self.dir_class_2 = list()

    def add_class_1(self):
        self.dir_class_1.append(QFileDialog.getExistingDirectory(self, "Open File", self.last_path))
        print("add class 1: " + self.dir_class_1[len(self.dir_class_1) - 1])
        self.last_path = (self.dir_class_1[len(self.dir_class_1) - 1]
        [:self.dir_class_1[len(self.dir_class_1) - 1].rfind("/")])
        self.list_1.addItem(self.dir_class_1[len(self.dir_class_1) - 1]
                            [self.dir_class_1[len(self.dir_class_1) - 1].rfind("/") + 1:])

    def add_class_2(self):
        self.dir_class_2.append(QFileDialog.getExistingDirectory(self, "Open File", self.last_path))
        print("add class 2: " + self.dir_class_2[len(self.dir_class_2) - 1])
        self.last_path = (self.dir_class_2[len(self.dir_class_2) - 1]
        [:self.dir_class_2[len(self.dir_class_2) - 1].rfind("/")])
        self.list_2.addItem(self.dir_class_2[len(self.dir_class_2) - 1]
                            [self.dir_class_2[len(self.dir_class_2) - 1].rfind("/") + 1:])

    def delete_class_1(self):
        if self.list_1.currentRow() < 0:
            return
        print("delete class 1: ")
        print(self.list_1.currentRow())
        self.dir_class_1.pop(self.list_1.currentRow())
        self.list_1.takeItem(self.list_1.currentRow())

    def delete_class_2(self):
        if self.list_2.currentRow() < 0:
            return
        print("delete class 2: ")
        print(self.list_2.currentRow())
        self.dir_class_2.pop(self.list_2.currentRow())
        self.list_2.takeItem(self.list_2.currentRow())

    def create_data(self):
        size_data = ds.calculation_size_data(self.dir_class_1, self.dir_class_2)

        df = ds.make_two_class(ds.make_dataset(self.dir_class_1, 0, size_data[0]),
                            ds.make_dataset(self.dir_class_2, 1, size_data[1]))
        ds.save_dataset(df)
        self.save_path()

    def save_path(self):
        ds.save_path("class_1.txt", self.dir_class_1)
        ds.save_path("class_2.txt", self.dir_class_2)

    def load_path(self):
        self.dir_class_1 = ds.load_path("class_1.txt")
        for path in self.dir_class_1:
            self.list_1.addItem(path[path.rfind("/") + 1:])

        self.dir_class_2 = ds.load_path("class_2.txt")
        for path in self.dir_class_2:
            self.list_2.addItem(path[path.rfind("/") + 1:])

    def clear(self):
        self.dir_class_1.clear()
        self.list_1.clear()
        self.dir_class_2.clear()
        self.list_2.clear()