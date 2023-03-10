import zipfile
from PyQt6.QtGui import QPixmap, QFileSystemModel
from PyQt6.QtWidgets import QFileDialog, QMessageBox, QAbstractItemView
# from settings.settings import Settings
from os import system, mkdir
from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt
from ui.ui import Ui_MainWindow
import sys


class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

    def closeEvent(self, event):
        system("rm -rf .temp")


class App:
    def __init__(self):
        # settings: Settings = Settings()
        self.app = QtWidgets.QApplication([])
        self.win = MyWindow()
        self.win.ui.actionOpen.triggered.connect(self.gpg_file_open)
        self.win.ui.pictures_list.clicked.connect(self.show_picture)
        # self.get_pictures()
        self.model = QFileSystemModel()

    def item_click(self):
        item = self.win.ui.pictures_list.currentItem().text()
        self.show_picture(item)
        self.gpg_file_open()

    def get_pictures(self):
        path = ".temp"
        self.model.setRootPath(path)
        self.win.ui.pictures_list.setModel(self.model)
        self.win.ui.pictures_list.setRootIndex(self.model.index(path))

    def show_picture(self, picture):
        picture_path = self.model.filePath(picture)
        picture = QPixmap(picture_path)
        picture = picture.scaled(
            self.win.ui.picture_box.width(),
            self.win.ui.picture_box.height(),
            Qt.AspectRatioMode.KeepAspectRatio)
        self.win.ui.picture_box.setPixmap(picture)

    def gpg_file_open(self):
        system("rm -rf .temp")
        file_name = QFileDialog.getOpenFileName(
            filter="*.gpg",
            directory="/Users/xah",
            caption="Open gpg file",
            parent=self.win)[0]
        if not file_name:
            return
        mkdir(".temp")
        result = system(f"gpg -d {file_name} > ./.temp/{'.'.join(file_name.split('/')[-1].split('.')[0:-1])}")
        if result == 512:
            QMessageBox.information(
                self.win,
                "Oh dear!",
                "?????????????????????? ????????????????",
                buttons=QMessageBox.StandardButton.Ok
            )
        else:
            zip_file = zipfile.ZipFile(f"./.temp/{'.'.join(file_name.split('/')[-1].split('.')[0:-1])}", 'r')
            zip_file.extractall(path='.temp', members=None, pwd=None)
            system(f"rm -rf ./.temp/{'.'.join(file_name.split('/')[-1].split('.')[0:-1])} ./.temp/__MACOSX")
            self.get_pictures()

    def run(self):
        self.win.show()
        sys.exit(self.app.exec())


def main():
    app = App()
    app.run()


if __name__ == '__main__':
    main()
