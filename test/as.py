import time

import serial
import ch9329Comm
from keyboard import ch9329
serial.ser = serial.Serial('COM3', 9600)  # 开启串口

mouse = ch9329Comm.mouse.DataComm(1920,1080)
# mouse.move_to_basic(422, 304)
mouse.send_data_absolute(422, 304)
# mouse.move_to(422,304) # 生成路径并沿路径移动到(-230,-480)
# time.sleep(2)
mouse.click()

ch9329.anxia('w')
time.sleep(1)
ch9329.tanqi('w')