import config
from device import ch9329
import time
import mPosition
# 定义几个方向的变量,记录按键是否按下.为了避免冲突,我们在前面加一个 x 或者 y



# 移动方法
def yidong(juese_zuobiao, mubiao_zuobiao):
    # global x_left, x_right, y_up, y_down
    x_left = 0
    x_right = 0
    y_up = 0
    y_down = 0
    print(f'人物坐标:{juese_zuobiao}, 目标坐标：{mubiao_zuobiao}')
    # x 轴方向逻辑
    if abs(juese_zuobiao[0] - mubiao_zuobiao[0]) >= 10:
        if juese_zuobiao[0] - mubiao_zuobiao[0] > 0:
            if x_right == 1:
                time.sleep(0.01)
                ch9329.tanqi('RIGHT')
                x_right = 0
            if x_left == 1:
                pass
            elif x_left == 0:
                if abs(juese_zuobiao[0] - mubiao_zuobiao[0]) > 80:
                    time.sleep(0.01)
                    ch9329.press('LEFT')
                    time.sleep(0.05)
                    time.sleep(0.01)
                    ch9329.anxia('LEFT')
                    x_left = 1
        elif juese_zuobiao[0] - mubiao_zuobiao[0] < 0:
            if x_left == 1:
                time.sleep(0.01)
                ch9329.tanqi('LEFT')
                x_left = 0
            if x_right == 1:
                pass
            elif x_right == 0:
                if abs(juese_zuobiao[0] - mubiao_zuobiao[0]) > 80:
                    time.sleep(0.01)
                    ch9329.press('RIGHT')
                    time.sleep(0.05)
                    time.sleep(0.01)
                    ch9329.anxia('RIGHT')
                    x_right = 1
                else:
                    if x_right == 1:
                        time.sleep(0.01)
                        ch9329.tanqi('RIGHT')
                        x_right = 0
                    # caozuoduilie_d.append('弹起 d')
                    if x_left == 1:
                        time.sleep(0.01)
                        ch9329.tanqi('a')
                        x_left = 0
    # y 轴方向逻辑
    if abs(juese_zuobiao[1] - mubiao_zuobiao[1]) >= 5:
        if juese_zuobiao[1] - mubiao_zuobiao[1] > 0:
            if y_down == 1:
                time.sleep(0.01)
                ch9329.tanqi('UP')
                y_down = 0
            if y_up == 1:
                pass
            elif y_up == 0:
                time.sleep(0.01)
                ch9329.anxia('UP')
                y_up = 1
        elif juese_zuobiao[1] - mubiao_zuobiao[1] < 0:
            if y_up == 1:
                time.sleep(0.01)
                ch9329.tanqi('UP')
                y_up = 0
            if y_down == 1:
                pass
            elif y_down == 0:
                time.sleep(0.01)
                ch9329.anxia('DOWN')
                y_down = 1
    else:
        if y_down == 1:
            time.sleep(0.01)
            ch9329.tanqi('DOWN')
            y_down = 0
        if y_up == 1:
            time.sleep(0.01)
            ch9329.tanqi('UP')
            y_up = 0


def search_door(person, doors):
    if config.current_map_room == 'hbl01':
        print('门在上面')
        config.is_move_center = False
    elif config.current_map_room == 'hbl02':
        print('门在右边')
    elif config.current_map_room == 'hbl03':
        print('门在上边')
    elif config.current_map_room == 'hbl04':
        print('门在上边')
    elif config.current_map_room == 'hbl05':
        print('门在右边')
    elif config.current_map_room == 'hbl06':
        print('门在右边')
        target = None
        for temp in doors:
            if temp.name == 'BOSS门':
                target = temp
        if target is not None and person is not None:
            yidong(person.center, target.center)


# print(f'当前按键情况: 左{x_left}, 右{x_right}, 上{y_up}, 下{y_down}')
# 停止方法
def tingzhi():
    global x_left, x_right, y_up, y_down

    ch9329.fuwei()
    if x_left == 1:
        x_left = 0
    if x_right == 1:
        x_right = 0
    if y_up == 1:
        y_up = 0
    if y_down == 1:
        y_down = 0
