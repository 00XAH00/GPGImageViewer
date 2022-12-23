import zipfile
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QFileDialog, QMessageBox
# from settings.settings import Settings
from os import listdir, system, mkdir
from os.path import isfile, join
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
        self.get_pictures()

    def item_click(self):
        item = self.win.ui.pictures_list.currentItem().text()
        self.show_picture(item)
        self.gpg_file_open()

    def get_pictures(self):
        files = [f for f in listdir("pictures") if isfile(join("pictures", f)) and f[0] != '.']
        self.win.ui.pictures_list.addItems(files)
        self.win.ui.pictures_list.itemSelectionChanged.connect(self.item_click)

    def show_picture(self, picture_path):
        picture = QPixmap(f"pictures/{picture_path}")
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
        print(file_name)
        mkdir(".temp")
        result = system(f"gpg -d {file_name} > ./.temp/{'.'.join(file_name.split('/')[-1].split('.')[0:-1])}")
        print(result)
        if result == 512:
            QMessageBox.information(
                self.win,
                "Oh dear!",
                "Расшифровка отменена",
                buttons=QMessageBox.StandardButton.Ok
            )
        else:
            zip_file = zipfile.ZipFile(f"./.temp/{'.'.join(file_name.split('/')[-1].split('.')[0:-1])}", 'r')
            zip_file.extractall(path='.temp', members=None, pwd=None)
            system(f"rm -rf ./.temp/{'.'.join(file_name.split('/')[-1].split('.')[0:-1])} _MACOSX")

    def run(self):
        self.win.show()
        sys.exit(self.app.exec())


def main():
    app = App()
    app.run()


if __name__ == '__main__':
    main()
