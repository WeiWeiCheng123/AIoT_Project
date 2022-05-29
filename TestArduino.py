import serial
from time import sleep

COM_PORT = 'COM9'
BAUD_RATES = 9600
s = serial.Serial(COM_PORT, BAUD_RATES)

if __name__ == '__main__':
    try:
        while True:
            choice = input()
            if choice == '1':
                s.write(b'LED_ON\n')
                sleep(0.5)
            if choice == '2':
                s.write(b'LED_OFF\n')
                sleep(0.5)
            else:
                pass
            while s.in_waiting:
                data = s.readline().decode()
                print(data)

    except KeyboardInterrupt:
        s.close()
