from rx_indexer import RxIndexer
from tx_indexer import TxIndexer
from tx_weg import TxWeg
from rx_weg import RxWeg
import sys
import serial.tools.list_ports

from PyQt5 import QtWidgets, uic
pyQTfileName = "window.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(pyQTfileName)

class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.btnStart.clicked.connect(self.start_reading)
        self.btnStop.clicked.connect(self.close_ports)

        listPorts = self.com_ports()
        self.box_idx_rx.clear()
        self.box_idx_rx.addItems(listPorts)
        self.box_idx_tx.clear()
        self.box_idx_tx.addItems(listPorts)
        self.box_weg_rx.clear()
        self.box_weg_rx.addItems(listPorts)
        self.box_weg_tx.clear()
        self.box_weg_tx.addItems(listPorts)
        self.rx_idx = None
        self.rx_weg = None
        self.tx_idx = None
        self.tx_weg = None
        self.status = False
    
    def com_ports(self):
        """load comports"""
        listP = serial.tools.list_ports.comports()
        connected = [""]
        for element in listP:
            connected.append(element.device)
        return(connected)

    def close_ports(self):
        self.status = False
        if self.rx_idx:
            self.rx_idx.close_port()
        if self.rx_weg:
            self.rx_weg.close_port()
        if self.tx_idx:
            self.tx_idx.close_port()
        if self.tx_weg:
            self.tx_weg.close_port()
        self.label_status.setStyleSheet("background-color: indianred")

    def start_reading(self):
        self.status = True
        """O Arquivo txt gerado deve ser aberto usando notepad++
        para facilitar a visualização de caracteres epesciais, i.i, ACK, EOF, etc"""
        if "COM" in self.box_idx_rx.currentText():
            self.rx_idx = RxIndexer(self.box_idx_rx.currentText())
        if "COM" in self.box_idx_tx.currentText():
            self.tx_idx = TxIndexer(self.box_idx_tx.currentText())
        if "COM" in self.box_weg_tx.currentText():
            self.tx_weg = TxWeg(self.box_weg_tx.currentText())
        if "COM" in self.box_weg_rx.currentText():
            self.rx_weg = RxWeg(self.box_weg_rx.currentText())
        self.label_status.setStyleSheet("background-color: lightgreen")
    
    def closeEvent(self, event):
        """Close application"""
        if self.status:
            self.close_ports()
        event.accept()        
    
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    
    window.show()
    sys.exit(app.exec_())
