import cv2
import time
import numpy as np

import person_action
import screenShot
import inference
from time import perf_counter as tp
from mPosition import mPosition
import directkeys
from directkeys import ReleaseKey
from direction_move import move
import current_map
import config
from device import ch9329

grab_size = 640
screen_x = 1920
screen_y = 1080
action_cache = None  # 动作标记
press_delay = 1  # 按压时间
release_delay = 1  # 释放时间
skill_char = "XYHGXFAXDSWXETX"  # 技能按键，使用均匀分布随机抽取
direct_dic = {"UP": 0xC8, "DOWN": 0xD0, "LEFT": 0xCB, "RIGHT": 0xCD}  # 上下左右的键码


def show_window(result) -> None:
    """
    可视化推理结果绘制
    """
    for x1, y1, x2, y2, _, cls in result:
        cls = int(cls)
        if cls == 0:  # 怪物
            color = (0, 0, 255)
            name = names[cls]
            # position = mPosition(x1, y1, x2, y2)
            # monster.append(position)
        elif cls == 1:  # 人物
            color = (0, 255, 0)
            name = names[cls]
            # person = mPosition(x1, y1, x2, y2)
        else:  # 其他
            color = (255, 0, 0)
            name = names[cls]
        cv2.rectangle(
            img,
            (int(x1), int(y1)),
            (int(x2), int(y2)),
            color,
            1
        )
        # cv2.putText(img,
        #             name,
        #             (int(x1), int(y1)),
        #             cv2.FONT_HERSHEY_COMPLEX,
        #             0.6,
        #             color,
        #             1
        #             )


sc = screenShot.grab_screen(
    grab_size,
    screen_x,
    screen_y
)

det = inference.inference(
    infer_mode='gpu',
    thread=6,
    model_path='best.onnx'
)
names = ['怪物', '人物', '材料', '金币', '通关', '门', 'BOSS门', '领主', '装备', '修理', '异次元', '赛利亚房间', '传送门']
tagert = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
fs = 5  # 几帧识别一次
frame = 0  # 帧
while True:
    o_img = sc.cap()  # 截取原始图片
    img = sc.img_process(o_img)  # 处理图片为640 640

    # cv2.imshow('temp11',
    #            img)
    #
    # cv2.waitKey(1)
    # pass
    frame += 1
    if frame % fs == 0:
    # if True:
        if img is not None:
            # current_map.get_map(o_img)
            t1 = tp()
            res = det.infer(img)
            t2 = tp()
            print(f'单次推理耗时: {round(((t2 - t1) * 1000), 6)}ms')
            img_object = []
            cls_object = []
            other = []
            person = None
            # 游戏
            thx = 30  # 捡东西时，x方向的阈值
            thy = 30  # 捡东西时，y方向的阈值
            attx = 150  # 攻击时，x方向的阈值
            atty = 50  # 攻击时，y方向的阈值

            monster_box = None
            if res is not None:  # 遍历推理结果
                show_window(res)  # 显示对象框
                cv2.imshow('temp11',
                           img)

                cv2.waitKey(1)
                for box in res:
                    x1, y1, x2, y2, _, cls = box
                    cls = int(cls)
                    obj = mPosition(x1, y1, x2, y2, names[cls])
                    cls_object.append(names[cls])
                    img_object.append(obj)
                    if cls == 1:
                        person = mPosition(x1, y1, x2, y2, names[cls])
            #  如果目标不存在，先停下来 找目标or找门
            if '怪物' not in cls_object and '材料' not in cls_object and '金币' not in cls_object and '装备' not in cls_object:
                ch9329.tanqi('')
                if config.current_map_next_point and person:
                    person_action.yidong(person.center,config.current_map_next_point)

                print('门坐标', config.current_map_next_point)
                #如果没有目标找门,先移动到地图y轴中心
                # if abs(person.bottomCenter[1] - config.map_centerY) <= config.map_centerY_value:
                #     print("y 值在阈值范围内")
                    # door_list = []
                    # for door in img_object:
                    #     if door.name in '门' or door.name in 'BOSS门':
                    #         door_list.append(door)
                    # if len(door_list) > 0:
                    #     person_action.search_door(person, door_list)
                # else:
                #     if person.bottomCenter[1] > config.map_centerY:
                #         ch9329.anxia('UP')
                #         time.sleep(0.1)
                #         ch9329.tanqi('UP')
                #     else:
                #         ch9329.anxia('DOWN')
                #         time.sleep(0.1)
                #         ch9329.tanqi('DOWN')


            if '人物' in cls_object:
                print(
                    f'人物当前坐标: {(int(person.x1 + person.x2) / 2), int(person.y2)} 当前地图: {config.current_map_name} 当前房间: {config.current_map_room}')
                for model in img_object:  # 绘制人物到对象的坐标
                    cv2.line(img,
                             (int(person.centerX), int(person.y2)),
                             (int(model.centerX), int(model.y2)),
                             (255, 255, 255))
            else:
                continue
            # 打怪
            if '怪物' in cls_object or '领主' in cls_object:
                min_distance = float('inf')
                for idx, model in enumerate(img_object):
                    if model.name == '怪物' or model.name == '领主':
                        dis = ((person.centerX - model.centerX) ** 2 + (person.centerY - model.centerY) ** 2) ** 0.5
                        if dis < min_distance:
                            monster_box = model
                            monster_index = idx
                            min_distance = dis
                    # 处于攻击距离
                    if monster_box is None:
                        continue

                    person_action.yidong(person.center, monster_box.center)

            if '门' in cls_object:
                pass
            # print(f'当前操作指令{action_cache}')
            # ReleaseKey(direct_dic["RIGHT"])
            # ReleaseKey(direct_dic["LEFT"])
            # ReleaseKey(direct_dic["UP"])
            # ReleaseKey(direct_dic["DOWN"])

            # 重新开始
            # time_option = -20
            # if '通关' in cls_object:
            #     if not action_cache:
            #         pass
            #     elif action_cache not in ["LEFT", "RIGHT", "UP", "DOWN"]:
            #         ReleaseKey(direct_dic[action_cache.strip().split("_")[0]])
            #         ReleaseKey(direct_dic[action_cache.strip().split("_")[1]])
            #         action_cache = None
            #     else:
            #         ReleaseKey(direct_dic[action_cache])
            #         action_cache = None
            #     if time.time() - time_option > 10:
            #         directkeys.key_press("V")
            #         print("移动物品到脚下")
            #         directkeys.key_press("X")
            #         time_option = time.time()
            #     directkeys.key_press("F10")
            #     print("通关 - 重新开始F10")

            cv2.imshow('temp11',
                       img)

            cv2.waitKey(1)

