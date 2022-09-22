import serial
import serial.tools.list_ports
import threading
import os, datetime

class RxWeg(threading.Thread):
    def __init__(self, porta):   
        threading.Thread.__init__(self)        
        self.ser = serial.Serial(
            port=porta,
            baudrate=9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.SEVENBITS,
            timeout=2)
        self.ser.close()
        if self.ser.is_open == False:
            try:
                print("Openning RX-WEG port")
                self.ser.open()
                self.ser.reset_input_buffer()
                self.ser.reset_output_buffer()
            except Exception as e:
                print(e)
            self.t_thread = threading.Thread(target = self.read)
            self.t_thread.start()
    
    def read(self):
        print("Reading RXWEG")
        while (True):            
            resp = self.ser.in_waiting
            if (resp > 0):
                data_str = self.ser.readline().decode('UTF-8')
                hours = datetime.datetime.now().strftime("%H")
                minute = datetime.datetime.now().strftime("%M")
                seconds = datetime.datetime.now().strftime("%S")
                time_log = str(hours) + ":" + str(minute) + ":" + str(seconds)
                with open('WEG_RX.txt', 'a+') as datafile:
                    datafile.write(time_log+' - '+data_str)
                    datafile.write("\n")
    
    def close_port(self):
        self.ser.reset_input_buffer()
        self.ser.reset_output_buffer()
        self.ser.close()
        self.t_thread.join()

