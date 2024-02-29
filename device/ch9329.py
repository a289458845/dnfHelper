import serial  # 导入串口库
import time  # 导入 time 库 用于时间控制
from device import mouse

# 配置串口参数
ser = serial.Serial('COM3', baudrate=9600, timeout=0.2)
# 定义一个按键码, 用来字符和实际控制码的转换
anjianma = {
    'ESC': '29',
    'UP': '52',
    'DOWN': '51',
    'LEFT': '50',
    'RIGHT': '4F',
    'A': '04',
    'B': '05',
    'C': '06',
    'D': '07',
    'E': '08',
    'F': '09',
    'G': '0A',
    'H': '0B',
    'I': '0C',
    'J': '0D',
    'K': '0E',
    'L': '0F',
    'M': '10',
    'N': '11',
    'O': '12',
    'P': '13',
    'Q': '14',
    'R': '15',
    'S': '16',
    'T': '17',
    'U': '18',
    'V': '19',
    'W': '1A',
    'X': '1B',
    'Y': '1C',
    'Z': '1D',
    'F1': '3B',
    'F2': '3C',
    'F3': '3D',
    'F4': '3E',
    'F5': '3F',
    'F6': '40',
    'F7': '41',
    'F8': '42',
    'F9': '43',
    'F10': '44',
    'F11': '45',
    'F12': '46'
}
hex_dict = {"ST": b'\x02',
            "NU": b"\x00",
            "LE": b"\x01",  # 左键
            "RI": b"\x02",  # 右键
            "CE": b"\x04"  # 中键
            }
X_MAX = 1920
Y_MAX = 1080
mouse = mouse.DataComm(1920, 1080)  # 初始化鼠标相对屏幕分辨率


# 发送数据到串口
def fasong(data):
    data_str = ''.join(data)
    hex_data = bytes.fromhex(data_str)
    ser.write(hex_data)
    time.sleep(0.05)


# 定义一个计算效验码的函数
def jisuan_sum(datalist):
    total_sum = 0
    for data in datalist:
        total_sum += int(data, 16)
        sum = hex(total_sum)[-2:]
    return sum


# 定义一个按下的函数,用于按下某个按键, 我们这里没有控制键的需求,就不考虑这个了
def anxia(anjian):
    # 键盘命令的前缀,这部分不会发生变化
    datalist = ["57", "AB", "00", "02", "08", "00", "00"]
    # 组合按下的按键
    datalist.append(anjianma[anjian])
    datalist.append("00")
    datalist.append("00")
    datalist.append("00")
    datalist.append("00")
    datalist.append("00")
    # 计算效验码
    xiaoyanma = jisuan_sum(datalist)
    # 组合完整的命令
    datalist.append(xiaoyanma)
    # 发送
    fasong(datalist)
def press(anjian):
    # 键盘命令的前缀,这部分不会发生变化
    datalist = ["57", "AB", "00", "02", "08", "00", "00"]
    # 组合按下的按键
    datalist.append(anjianma[anjian])
    datalist.append("00")
    datalist.append("00")
    datalist.append("00")
    datalist.append("00")
    datalist.append("00")
    # 计算效验码
    xiaoyanma = jisuan_sum(datalist)
    # 组合完整的命令
    datalist.append(xiaoyanma)
    # 发送
    fasong(datalist)
    time.sleep(0.01)
    tanqi(anjian)


def move(x: int, y: int, ctrl: str = ''):
    # 将字符转写为数据包
    HEAD = b'\x57\xAB'  # 帧头
    ADDR = b'\x00'  # 地址
    CMD = b'\x04'  # 命令
    LEN = b'\x07'  # 数据长度
    DATA = bytearray(b'\x02')  # 数据

    # 鼠标按键
    if ctrl == '':
        DATA.append(0)
    elif isinstance(ctrl, int):
        DATA.append(ctrl)
    else:
        DATA += hex_dict[ctrl]

    # 坐标
    X_Cur = (4096 * x) // X_MAX
    Y_Cur = (4096 * y) // Y_MAX
    DATA += X_Cur.to_bytes(2, byteorder='little')
    DATA += Y_Cur.to_bytes(2, byteorder='little')

    if len(DATA) < 7:
        DATA += b'\x00' * (7 - len(DATA))
    else:
        DATA = DATA[:7]

    # 分离HEAD中的值，并计算和
    HEAD_hex_list = list(HEAD)
    HEAD_add_hex_list = sum(HEAD_hex_list)

    # 分离DATA中的值，并计算和
    DATA_hex_list = list(DATA)
    DATA_add_hex_list = sum(DATA_hex_list)

    try:
        SUM = sum([HEAD_add_hex_list, int.from_bytes(ADDR, byteorder='big'),
                   int.from_bytes(CMD, byteorder='big'), int.from_bytes(LEN, byteorder='big'),
                   DATA_add_hex_list]) % 256  # 校验和
    except OverflowError:
        print("int too big to convert")
        return False
    packet = HEAD + ADDR + CMD + LEN + DATA + bytes([SUM])  # 数据包
    ser.write(packet)
    time.sleep(0.1)
    return True
# 弹起按键
def tanqi(anjian):
    datalist = ["57", "AB", "00", "02", "08", "00", "00", "00", "00", "00",
                "00", "00", "00", "0C"]
    # 发送
    fasong(datalist)
def fuwei():
    tanqi()


if __name__ == '__main__':
    # for a in range(10):
    time.sleep(1)
    anxia('RIGHT')
    time.sleep(2)
    tanqi('RIGHT')
    # move(422,304,'LE')
    # move(0,0,'NU')
    # print('move ')
