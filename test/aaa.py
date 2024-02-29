import serial
import time

class CH9239MouseController:
    def __init__(self, port='COM3', baudrate=9600):
        self.serial = serial.Serial(port, baudrate)
        time.sleep(2)  # 等待串口初始化完成


def send_data_absolute(self, x: int, y: int, ctrl: str = '', port: serial = serial) -> bool:
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
        DATA += self.hex_dict[ctrl]

    # 坐标
    X_Cur = (4096 * x) // 1920
    Y_Cur = (4096 * y) // 1080
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
    port.ser.write(packet)  # 将命令代码写入串口
    return True  # 如果成功，则返回True，否则引发异常

if __name__ == "__main__":
    try:
        mouse_controller = CH9239MouseController()

        # 移动鼠标，delta_x 和 delta_y 可以是负值
        mouse_controller.move_mouse(delta_x=422, delta_y=304)

        # 鼠标点击
        mouse_controller.click_mouse()

        # 在这里添加其他需要执行的操作

    finally:
        print('bb')
        # mouse_controller.release_mouse()  # 确保鼠标释放
        # mouse_controller.move_mouse(0, 0)  # 确保鼠标回到原始位置
        # mouse_controller.close()
