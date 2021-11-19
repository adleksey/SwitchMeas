from PyQt6 import QtWidgets, uic
import sys
import pyvisa
import pyqtgraph as pg

class VNA():
    def __init__(self):
        self.rm = pyvisa.ResourceManager('@py')
    
    def connect(self, visa_name):
        try:
            self.device = self.rm.open_resource(visa_name)
            self.device.read_termination = '\n'
            self.device.write_termination = '\n'
            self.device.query('SYST:FPRESET;*OPC?')
        except:
            return False
        else:
            return True
            
    def setMeasParam(self):
        self.device.write('DISP:WIND1:STAT ON')
        self.device.write('DISP:WIND2:STAT ON')
        self.device.write("CALC1:PAR:DEF 'S11', S11")
        self.device.write("CALC1:PAR:DEF 'S21', S21")
        self.device.write("DISP:WIND1:TRAC1:FEED 'S11'")
        self.device.write("DISP:WIND2:TRAC1:FEED 'S21'")
        self.device.write('SENS1:FREQ:STAR ' + str(20) + ' MHz')
        self.device.write('SENS1:FREQ:STOP ' + str(40) + ' GHz')
        self.device.write('SENS1:SWE:POIN 401')
        self.device.write('SENS1:BWID 1 KHz')
        # CALC1:MARK1:STAT ON
        # CALC1:MARK1:X 10 GHz
        # CALC1:MARK1:X?
        # CALC1:MARK1:Y?
        # INITiate1;*OPC?
        # CALC1:PAR:SEL 'S21'
        # FORM ASCII
        # CALC1:DATA? FDATA
        #self.device.write('*RST;*CLS')
        #self.device.write("SYST:DISP:UPD ON")
        #self.device.write("FREQ:CONV:DEV:NAME 'NONE'")
        #self.device.write("SENS1:FREQ:STAR " + freq_start)
        #self.device.write("SENS1:FREQ:STOP " + freq_stop)
        #self.device.write("SENS1:SWE:STEP " + freq_step)
        #self.device.write("SENS1:BAND 100 HZ")
        #self.device.write("CALC1:PARAMETER:SDEFINE 'Trc1', 'S11'")
        #self.device.write("DISPLAY:WINDOW1:TRACE1:FEED 'Trc1'")
        #self.device.write(":INITIATE:CONTINUOUS OFF")

    def measureSParam(self, result):
        self.device.write(':INITIATE:IMMEDIATE')
        #self.device.query("*OPC?")
        #asc = self.device.query_ascii_values("CALC1:DATA? SDAT")
        #stm = self.device.query_ascii_values("CALC1:DATA:STIM?")
        #self.device.write("DISP:WINDOW1:TRACE1:Y:AUTO ONCE")
        #reSparam = asc[::2]
        #imSparam = asc[1::2]
        #result['freq'] = rf.Frequency(stm[0], stm[-1], len(stm), 'hz')
        #result['Sparam'] = [x + y*1j for x, y in zip(reSparam, imSparam)]
    def getIDN(self):
        return self.device.query('*IDN?')

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("swmeas_main.ui", self)
        self.vna = VNA()
        self.btn_VNA_connect.clicked.connect(self.btn_VNA_connectf)
    
    def btn_VNA_connectf(self):
        if self.vna.connect(self.txt_VISA_resource.toPlainText()):
            self.label.setText("VNA: " + self.vna.getIDN())
        else:
            self.label.setText("VNA: conection error")
    
    def btn_VNA_presetf(self):
        vna.setMeasParam()

def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()