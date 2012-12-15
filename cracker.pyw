#coding: UTF-8

import os
import ConfigParser
import time
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import pyqtSlot
import encoding_detector
import vigenere_cracker


class Widget(QtGui.QMainWindow):

    presets = {}

    def __init__(self):
        super(QtGui.QMainWindow, self).__init__()

        self.setupCipherGroup()
        self.setupOptionsGroup()
        self.setupMoreOptionsGroup()
        self.setupResultsGroup()

        w1 = QtGui.QWidget()
        l1 = QtGui.QVBoxLayout(w1)
        l1.setMargin(0)
        l1.addWidget(self.cipherGroup)
        l1.addWidget(self.optionsGroup)

        s1 = QtGui.QSplitter()
        s1.addWidget(w1)
        s1.addWidget(self.tabs)

        self.setCentralWidget(s1)
        self.setWindowTitle("Vigenere cipher cracker")

        self.loadPresets()
        self.toggleMoreOptions(1)


    def setupResultsGroup(self):
        self.gammaTable         = QtGui.QTreeWidget()
        self.output             = QtGui.QPlainTextEdit()
        gamma                   = QtGui.QLineEdit()
        encodedText             = QtGui.QPlainTextEdit()
        resultsMenu             = QtGui.QMenu()
        copyGamma               = QtGui.QAction('Gamma to clipboard', self)
        copyText                = QtGui.QAction('Text to clipboard', self)
        decode                  = QtGui.QPushButton('Decode')
        decodeOrder             = QtGui.QCheckBox('Inverse')
        
        resultsMenu.addActions((copyGamma, copyText))
        encodedText.setReadOnly(True)
        self.output.setTabStopWidth(30)
        self.output.setReadOnly(True)
        self.output.setWordWrapMode(QtGui.QTextOption.NoWrap)
        self.gammaTable.setColumnCount(2)
        self.gammaTable.setHeaderLabels(('Gamma', 'Text'))
        self.gammaTable.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)

        
        l = QtGui.QHBoxLayout()
        l.addWidget(QtGui.QLabel('Selected gamma:'))
        l.addWidget(gamma)
        l.addWidget(decode)
        l.addWidget(decodeOrder)
                
        w1 = QtGui.QWidget()
        l1 = QtGui.QVBoxLayout(w1)
        l1.addWidget(self.gammaTable)
        l1.addLayout(l)
        l1.addWidget(encodedText)
        
        self.tabs = QtGui.QTabWidget()
        self.tabs.addTab(w1, 'Result')
        self.tabs.addTab(self.output, 'Output')
        
        

        def copyGammaResult():
	    items = self.gammaTable.selectedItems()
            gamma = items[0].text(0)
            QtGui.QApplication.clipboard().setText(gamma)

        def copyTextResult():
            items = self.gammaTable.selectedItems()
            gamma = items[0].text(1)
            QtGui.QApplication.clipboard().setText(text)

        def showDecodedText():
	    items = self.gammaTable.selectedItems()
            if not len(items):
               return

            gamma.setText(items[0].text(0))
            encodedText.setPlainText(items[0].text(1))
            
        def showResultContextMenu(point):
            if not len(self.gammaTable.selectedItems()):
               return

            point = self.sender().mapToGlobal(point)
            point.setY(point.y() + self.gammaTable.header().height())
            resultsMenu.exec_(point)
            
        def applyGamma():
	    cipher   = unicode(self.cipher.toPlainText())
	    alphabet = unicode(self.alphabet.text())
	    g        = unicode(gamma.text())
	    order    = not decodeOrder.isChecked()
	    
	    text = vigenere_cracker.applyGamma(cipher, g, alphabet, order)
	    encodedText.setPlainText(text)
	    

            
        copyGamma.triggered.connect(copyGammaResult)
        copyText.triggered.connect(copyTextResult)
        gamma.returnPressed.connect(applyGamma)
        decode.clicked.connect(applyGamma)
        self.gammaTable.customContextMenuRequested.connect(showResultContextMenu)
        self.gammaTable.itemSelectionChanged.connect(showDecodedText)


    def setupCipherGroup(self):
        self.cipherGroup    = QtGui.QGroupBox('Cipher')
        self.openCipher     = QtGui.QPushButton('Open...')
        self.clearCipher    = QtGui.QPushButton('Clear')
        self.cipher         = QtGui.QPlainTextEdit()

        self.cipher.setPlainText(u' фьбтущщахуцясотанаюудюгудщ')

        lay = QtGui.QHBoxLayout()
        lay.addWidget(self.openCipher)
        lay.addWidget(self.clearCipher)
        lay.addStretch()

        layout = QtGui.QVBoxLayout(self.cipherGroup)
        layout.addLayout(lay)
        layout.addWidget(self.cipher)

        def openCipherFile():
            path = QtGui.QFileDialog.getOpenFileName(caption='Open cipher file')

            if not path.isEmpty():
                text = open(path).read()
                encoding = encoding_detector.get_codepage(text)
                if len(encoding): text = text.decode(encoding)
                self.cipher.setPlainText(text)

        self.openCipher.clicked.connect(openCipherFile)
        self.clearCipher.clicked.connect(self.cipher.clear)


    def setupOptionsGroup(self):
        self.optionsGroup   = QtGui.QGroupBox('Encoded data parameters')
        self.preset         = QtGui.QComboBox()
        self.crack          = QtGui.QPushButton('Crack')
        self.more           = QtGui.QPushButton('...')

        self.more.setToolTip('Show more options')
        self.more.setMaximumWidth(32)

        lay = QtGui.QHBoxLayout()
        lay.addWidget(self.crack)
        lay.addStretch()

        lay2 = QtGui.QHBoxLayout()
        lay2.addWidget(self.preset)
        lay2.addWidget(self.more)

        layout = QtGui.QVBoxLayout(self.optionsGroup)
        layout.addLayout(lay2)
        layout.addLayout(lay)

        self.crack.clicked.connect(self.crackIt)
        self.more.clicked.connect(self.toggleMoreOptions)


    def setupMoreOptionsGroup(self):
        self.moreGroup      = QtGui.QGroupBox()        # Custom parameters
        self.resetOptions   = QtGui.QPushButton('Reset by default')
        self.applyOptions   = QtGui.QPushButton('Crack')
        self.alphabet       = QtGui.QLineEdit()
        self.frequencyList  = QtGui.QLineEdit()
        self.coincidenceVal = QtGui.QDoubleSpinBox()

        self.coincidenceVal.setMaximum(1)
        self.coincidenceVal.setSingleStep(0.01)
        self.coincidenceVal.setDecimals(4)
        self.coincidenceVal.setMaximumWidth(70)
        self.moreGroup.setWindowFlags(QtCore.Qt.Drawer | QtCore.Qt.WindowStaysOnTopHint)
        self.moreGroup.resize(450,50)

        lay = QtGui.QHBoxLayout()
        lay.addStretch()
        lay.addWidget(self.resetOptions)
        lay.addWidget(self.applyOptions)
        lay.addStretch()

        layout = QtGui.QFormLayout(self.moreGroup)
        layout.addRow('Alphabet:', self.alphabet)
        layout.addRow('Frequency list:', self.frequencyList)
        layout.addRow('Min. index of coincidence:', self.coincidenceVal)
        layout.addRow(lay)

        self.applyOptions.clicked.connect(self.crackIt)
        self.preset.currentIndexChanged.connect(self.presetChanged)
        self.resetOptions.clicked.connect(self.presetChanged)


    def loadPresets(self):
        self.presets.clear()
        dir = 'data/presets/'
        config = ConfigParser.ConfigParser()

        for file in os.listdir(dir):
            config.read(dir + file)
            name = file
            if '.' in name:
		name = name[:name.rindex('.')]
            self.presets[name] = dict([(key, val.decode("UTF-8").strip('\"')) for key, val in config.items('Preset')])

        self.preset.addItems(self.presets.keys())


    @pyqtSlot(str)
    def presetChanged(self, name):
        name = unicode(self.preset.currentText())
        d = self.presets[name]

        self.alphabet.setText(d['alphabet'])
        self.frequencyList.setText(d['freqlist'])
        self.coincidenceVal.setValue(float(d['coincidence']))
        self.moreGroup.setWindowTitle(name + ' - options')


    def toggleMoreOptions(self, expand):
        if expand:
            expand = False
        else:
            expand = not self.moreGroup.isVisible()

        self.moreGroup.setVisible(expand)


    def crackIt(self):
        self.output.clear()
        self.gammaTable.clear()

        cipher = unicode(self.cipher.toPlainText())
        alphabet = unicode(self.alphabet.text())
        start  = time.clock()
        result = vigenere_cracker.crack(cipher,
                                        alphabet,
                                        frequencyTable = unicode(self.frequencyList.text()),
                                        minCoincidence = self.coincidenceVal.value(),
                                        variants       = 8,
                                        output         = self)

        for r in result:
            strings = (r, vigenere_cracker.applyGamma(cipher, r, alphabet, True))
            item = QtGui.QTreeWidgetItem(strings)
            self.gammaTable.addTopLevelItem(item)

        #self.outputGroup.setWindowTitle('Output (done for%5.2fs)' % (time.clock() - start))

        
    def write(self, string):                                  # метод для вывода минуя консоль
        self.output.setPlainText(self.output.toPlainText() + string)



if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    #QtCore.QDir.setCurrent(app.applicationDirPath())
    app.setStyleSheet(open('style/style.css').read())
    widget = Widget()
    widget.resize(760,480)
    widget.show()
    sys.exit(app.exec_())
