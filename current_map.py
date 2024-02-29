import time

import cv2
import numpy as np
import screenShot
import config
import mPosition

from device import ch9329
grab_size = 640
screen_x = 1920
screen_y = 1080
sc = screenShot.grab_screen(
    grab_size,
    screen_x,
    screen_y
)
citys = ['sly', 'juesexuanze', 'chengzhen', 'hbl', 'jjc_xzdt']

hbl = ['hbl01', 'hbl02', 'hbl03', 'hbl04', 'hbl05', 'hbl06']

currentRoom = 0

def pic_compare(smal_img_path, big_img_gray):
    # 获取小图片
    xiaotupian = cv2.imread(smal_img_path)
    xiaotupian_huidu = cv2.cvtColor(xiaotupian, cv2.COLOR_BGR2GRAY)
    # 在大图片中查找小图片
    chazhaojieguo = cv2.matchTemplate(big_img_gray, xiaotupian_huidu,
                                      cv2.TM_CCOEFF_NORMED)
    # 筛选结果
    chazhaojieguo_shaixuan = np.where(chazhaojieguo >= 0.8)  # 用 np 筛
    # 选一下结果高于 0.85的
    chazhaojieguo_zuobiao_liebiao = list(zip(*chazhaojieguo_shaixuan[::-1]))  # 将结果再次处理一下,仅保留坐标 值

    return chazhaojieguo_zuobiao_liebiao


def get_hbl_room(img_name,big_map_gray):
    for i in hbl:
        spath = f'resource/dxc/hbl/{i}.png'
        small_map_location = pic_compare(spath, big_map_gray)
        config.current_map_next_point = None

        # print('小地图坐标', small_map_location)
        if len(small_map_location) > 0:
            config.current_map_room = i
            if i == 'hbl01':
                print('当前在第一个房间', i)
                rpath = f'resource/dxc/hblroom/room0.png'
                target_point = pic_compare(rpath, big_map_gray)
                if len(target_point) > 0:
                    config.current_map_next_point = target_point[0]
                break
            elif i == 'hbl02':
                rpath = f'resource/dxc/hblroom/room1.png'
                target_point = pic_compare(rpath, big_map_gray)
                if len(target_point) > 0:
                    config.current_map_next_point = target_point[0]
                break
                print('当前在第二个房间', i)
                break
            elif i == 'hbl03':
                print('当前在第三个房间', i)
                break
            elif i == 'hbl04':
                print('当前在第四个房间', i)
                break
            elif i == 'hbl05':
                print('当前在第五个房间', i)
                break
            elif i == 'hbl06':
                print('当前在第六个房间', i)
                break
            elif i == 'hbl_boss':
                print('当前在BOSS房间', i)
                break
            else:
                pass
            break



def get_room():
    pass

def get_map(bigmap):
    datupian_huidu = cv2.cvtColor(bigmap, cv2.COLOR_BGR2GRAY)
    for img in citys:

        path = f'resource/cz/{img}.png'
        chazhaojieguo_zuobiao_liebiao = pic_compare(path, datupian_huidu)

        # 判断场景
        if len(chazhaojieguo_zuobiao_liebiao) > 0:
            if 'sly' in img or 'move' in img:
                print('当前画面: 赛利亚房间', chazhaojieguo_zuobiao_liebiao)
                ch9329.anxia('RIGHT')
                time.sleep(2)
                ch9329.tanqi('RIGHT')
                time.sleep(0.5)
                # 移动到传送门
                if img == 'move':

                    ch9329.move(422, 304, 'LE') # 移动并且点击
                    ch9329.move(0, 0, 'NU') # 点击释放
            elif 'juesexuanze' in img:
                print('当前画面: 角色选择', chazhaojieguo_zuobiao_liebiao,time.time())
                x, y = chazhaojieguo_zuobiao_liebiao[0]
                ch9329.move(401, 568, 'LE')  # 移动并且点击
                ch9329.move(0, 0, 'NU')  # 点击释放
                ch9329.anxia('ESC')
                ch9329.tanqi('ESC')

            elif 'chengzhen' in img:
                print('当前画面: 城镇', chazhaojieguo_zuobiao_liebiao, time.time())
            elif 'jjc_xzdt' in img:
                print('当前画面: 寂静城选择地图', chazhaojieguo_zuobiao_liebiao)
                # 选择地图、选择难度
            elif 'hbl' in img:
                config.current_map_name = '海伯伦研究所'
                # print('当前画面: 海伯伦研究所', chazhaojieguo_zuobiao_liebiao)
                get_hbl_room(img, datupian_huidu)
            else:
                print('当前画面: 未知', chazhaojieguo_zuobiao_liebiao)
            break
    # else:
    # print('当前画面: 不知道')
def move(mPosition):
    pass

if __name__ == '__main__':
    while True:
        img = sc.cap()  # 截取原始图片

        get_map(img)
        cv2.imshow('temp', img)

        cv2.waitKey(1)