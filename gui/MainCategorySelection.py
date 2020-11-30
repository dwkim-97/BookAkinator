import sys
from PyQt5.QtWidgets import *


class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        val = self.setupUI()

    def novel_clicked(self):
        alert = QMessageBox()
        alert.setText('소설을 선택하셨습니다!')
        alert.exec_()

    def reference_clicked(self):
        alert = QMessageBox()
        alert.setText('참고서를 선택하셨습니다!')
        alert.exec_()

    def self_enlight_clicked(self):
        alert = QMessageBox()
        alert.setText('자기계발서를 선택하셨습니다!')
        alert.exec_()

    def setupUI(self):
        label1 = QLabel('대분류를 선택해주세요.')

        btn1 = QPushButton('소설')
        btn1.clicked.connect(self.novel_clicked)
        btn2 = QPushButton('참고서')
        btn2.clicked.connect(self.reference_clicked)
        btn3 = QPushButton('자기계발서')
        btn3.clicked.connect(self.self_enlight_clicked)

        hbox = QHBoxLayout()
        hbox.addWidget(label1)

        vbox = QVBoxLayout()
        vbox.addWidget(btn1)
        vbox.addWidget(btn2)
        vbox.addWidget(btn3)

        hbox.addLayout(vbox)

        self.setWindowTitle('Book Akinator')
        self.setLayout(hbox)
        self.setGeometry(100, 100, 500, 500)
        self.show()

        return 5


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    print(ex)

    sys.exit(app.exec_())
