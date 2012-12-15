#coding: UTF-8

from PyQt4 import QtGui
import str_analyser


class AnalyserWidget(QtGui.QWidget):

    def __init__(self):
        super(QtGui.QWidget, self).__init__()

        self.list     = QtGui.QListWidget()
        openFile      = QtGui.QPushButton('Add...')
        clear         = QtGui.QPushButton('Clear')
        self.caseSensitive = QtGui.QCheckBox('Case sensitive')
        analyse       = QtGui.QPushButton('Analyse')
        self.ignoredChars = QtGui.QLineEdit()
        self.result   = QtGui.QTextBrowser()

        self.result.setMaximumHeight(120)
        analyse.setMinimumHeight(40)
        self.setWindowTitle('String analyser')

        l1 = QtGui.QHBoxLayout()
        l1.addWidget(openFile)
        l1.addWidget(clear)
        l1.addStretch()

        l2 = QtGui.QHBoxLayout()
        l2.addWidget(analyse)
        l2.addStretch()
        l2.addWidget(self.caseSensitive)
        l2.addSpacing(20)
        l2.addWidget(QtGui.QLabel('Ignore chars:'))
        l2.addWidget(self.ignoredChars)

        layout = QtGui.QVBoxLayout(self)
        layout.addWidget(QtGui.QLabel('Open files to analyse:'))
        layout.addLayout(l1)
        layout.addWidget(self.list)
        layout.addLayout(l2)
        layout.addSpacing(10)
        layout.addWidget(QtGui.QLabel('Result:'))
        layout.addWidget(self.result)

        openFile.clicked.connect(self.openFileDialog)
        clear.clicked.connect(self.list.clear)
        analyse.clicked.connect(self.doAnalyse)
        self.ignoredChars.returnPressed.connect(self.doAnalyse)


    def openFileDialog(self):
        files = QtGui.QFileDialog.getOpenFileNames(caption='Open file')

        for file in files:
            self.list.addItem(file)


    def doAnalyse(self):
        self.result.clear()
        files = []
        for i in range(self.list.count()):
            files.append(unicode(self.list.item(i).text()))

        str_analyser.analyse(files,
                             caseSensitive=self.caseSensitive.isChecked(),
                             skip=unicode(self.ignoredChars.text()),
                             output=self)


    def write(self, string):                                  # метод для вывода минуя консоль
        self.result.setPlainText(self.result.toPlainText() + string)



if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    w = AnalyserWidget()
    w.resize(450,500)
    w.show()
    sys.exit(app.exec_())
