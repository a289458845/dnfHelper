import cv2
import numpy as np

citys = ['sly', 'juesexuanze', 'chengzhen', 'hbl']

hbl = ['hbl01', 'hbl02', 'hbl03', 'hbl04', 'hbl05', 'hbl06']


def pic_compare(smal_img_path, big_img_gray):
    # 获取小图片
    xiaotupian = cv2.imread(smal_img_path)
    xiaotupian_huidu = cv2.cvtColor(xiaotupian, cv2.COLOR_BGR2GRAY)
    # 在大图片中查找小图片
    chazhaojieguo = cv2.matchTemplate(big_img_gray, xiaotupian_huidu,
                                      cv2.TM_CCOEFF_NORMED)
    # 筛选结果
    chazhaojieguo_shaixuan = np.where(chazhaojieguo >= 0.85)  # 用 np 筛
    # 选一下结果高于 0.85的
    chazhaojieguo_zuobiao_liebiao = list(zip(*chazhaojieguo_shaixuan[::-1]))  # 将结果再次处理一下,仅保留坐标 值

    return chazhaojieguo_zuobiao_liebiao


def get_hbl_room(img_name,big_map_gray):
    for i in hbl:
        spath = f'resource/dxc/hbl/{i}.png'
        small_map_location = pic_compare(spath, big_map_gray)
        # print('小地图坐标', small_map_location)
        if len(small_map_location) > 0:
            if img_name in 'hbl01':
                print('当前在第一个房间')
            elif img_name in 'hbl02':
                print('当前在第二个房间')
            elif img_name in 'hbl03':
                print('当前在第三个房间')
            elif img_name in 'hbl04':
                print('当前在第四个房间')
            elif img_name in 'hbl05':
                print('当前在第五个房间')
            elif img_name in 'hbl06':
                print('当前在第六个房间')
            else:
                pass
            break



def get_map(bigmap):
    datupian_huidu = cv2.cvtColor(bigmap, cv2.COLOR_BGR2GRAY)
    for img in citys:

        path = f'resource/cz/{img}.png'
        chazhaojieguo_zuobiao_liebiao = pic_compare(path, datupian_huidu)

        # 判断场景
        if len(chazhaojieguo_zuobiao_liebiao) > 0:
            if 'sly' in img:
                print('当前画面: 赛利亚房间', chazhaojieguo_zuobiao_liebiao)
            elif 'juesexuanze' in img:
                print('当前画面: 角色选择', chazhaojieguo_zuobiao_liebiao)
            elif 'chengzhen' in img:
                print('当前画面: 城镇', chazhaojieguo_zuobiao_liebiao)
            elif 'hbl' in img:
                # print('当前画面: 海伯伦研究所', chazhaojieguo_zuobiao_liebiao)
                # get_hbl_room(img, datupian_huidu)
                pass
            else:
                print('当前画面: 未知', chazhaojieguo_zuobiao_liebiao)
            break
    # else:
    # print('当前画面: 不知道')


if __name__ == '__main__':
    pass
