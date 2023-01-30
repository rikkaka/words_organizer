import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
import home, record, review, dict, wordsys

library = wordsys.WordsLibrary()


class HomeW(QMainWindow, home.Ui_MainWindow):
    def __init__(self):
        super(HomeW, self).__init__()
        self.setupUi(self)
        library.load_words()
        self.refresh()

    def refresh(self):
        self.textBrowser.setPlainText(str(library.get_total_nums()))
        self.textBrowser_2.setPlainText(str(library.get_recite_nums()))


class RecordW(QMainWindow, record.Ui_MainWindow):
    def __init__(self):
        super(RecordW, self).__init__()
        self.setupUi(self)
        self.textEdit.setPlainText('')
        self.textEdit_2.setPlainText('')
        self.pushButton.clicked.connect(self.search)
        self.pushButton_2.clicked.connect(self.record)

    def search(self):
        tr = dict.translate(self.textEdit.toPlainText())
        self.textEdit_2.setPlainText(tr)

    def record(self):
        word = self.textEdit.toPlainText()
        tr = self.textEdit_2.toPlainText()
        library.add_word(wordsys.Word(word, tr))
        library.save_words()


class ReviewW(QMainWindow, review.Ui_window_review):
    def __init__(self):
        super(ReviewW, self).__init__()
        self.setupUi(self)
        self.know = 0
        self.word_list = []
        self.word = ''
        self.stage = 0
        self.setup()
        self.pushButton.clicked.connect(self.worenshi)
        self.pushButton_2.clicked.connect(self.meixiangqilai)
        self.pushButton_3.clicked.connect(self.yizhangwo)

    def setup(self):
        self.word_list = library.get_recite_list()
        self.know = 0
        self.stage = 0
        try:
            self.word_list = library.get_recite_list()
            self.word = self.word_list[0]
            self.textBrowser.setPlainText(self.word.wordtext)
            self.textBrowser_2.setPlainText(self.word.translation)
        except:
            self.stage = 2
            self.textBrowser.setPlainText('已完成复习')
            self.textBrowser_2.setPlainText('')

    def open(self):
        self.setup()
        self.show()

    def next(self):
        switch = {0: self.word.back,
                  1: self.word.improve,
                  2: self.word.master,
                  }
        switch.get(self.know)()
        self.textBrowser_2.setPlainText('')
        self.pushButton.setText('我认识')
        self.pushButton_2.setText('没想起来')
        self.stage = 0
        if len(self.word_list) <= 1:
            self.word_list = library.get_recite_list()
            if len(self.word_list) <= 1:
                self.stage = 2
                self.textBrowser.setPlainText('已完成复习')
                self.textBrowser_2.setPlainText('')
                library.save_words()
                return
        else:
            self.word_list = self.word_list[1:]
        self.word = self.word_list[0]
        self.textBrowser.setPlainText(self.word.wordtext)
        self.textBrowser_2.setPlainText(self.word.translation)
        library.save_words()

    def worenshi(self):
        if self.stage == 0:
            self.know = 1
            self.textBrowser_2.setPlainText(self.word.translation)
            self.pushButton.setText('下一个')
            self.pushButton_2.setText('不认识')
            self.stage = 1
        elif self.stage == 1:
            self.next()

    def meixiangqilai(self):
        if self.stage == 0:
            self.know = 0
            self.textBrowser_2.setPlainText(self.word.translation)
            self.pushButton.setText('下一个')
            self.pushButton_2.setText('不认识')
            self.stage = 1
        elif self.stage == 1:
            self.know = 0
            self.next()

    def yizhangwo(self):
        if self.stage!=2:
            self.know = 2
            self.next()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    homew = HomeW()
    recordw = RecordW()
    revieww = ReviewW()
    homew.show()
    homew.pushButton.clicked.connect(recordw.show)
    homew.pushButton_2.clicked.connect(revieww.open)
    recordw.pushButton.clicked.connect(homew.refresh)
    recordw.pushButton_2.clicked.connect(homew.refresh)
    revieww.pushButton.clicked.connect(homew.refresh)
    revieww.pushButton_2.clicked.connect(homew.refresh)
    revieww.pushButton_3.clicked.connect(homew.refresh)
    sys.exit(app.exec_())
