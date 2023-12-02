import cv2
import time
import numpy as np
import screenShot
import inference
from time import perf_counter as tp
from mPosition import mPosition
import directkeys
from directkeys import ReleaseKey
from direction_move import move
import current_map

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
    thread=4,
    model_path='yolov5s_best.onnx'
)
names = ['怪物', '人物', '材料', '金币', '通关', '门', 'BOSS门', '领主', '装备', '修理']
tagert = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
fs = 4  # 几帧识别一次
frame = 0  # 帧
while True:
    img = sc.cap() # 截取原始图片
    n_img = sc.img_process(img) # 处理图片为640 640
    pass
    frame += 1
    if frame % 4 == 0:
        if n_img is not None:
            # current_map.get_map(img)
            t1 = tp()
            res = det.infer(n_img)
            t2 = tp()
            # print(f'单次推理耗时: {round(((t2 - t1) * 1000), 6)}ms')
            img_object = []
            cls_object = []
            other = []

            # 游戏
            thx = 30  # 捡东西时，x方向的阈值
            thy = 30  # 捡东西时，y方向的阈值
            attx = 150  # 攻击时，x方向的阈值
            atty = 50  # 攻击时，y方向的阈值
            monster_box = None
            if res is not None:  # 遍历推理结果
                show_window(res)  # 显示对象框
                for box in res:
                    x1, y1, x2, y2, _, cls = box
                    cls = int(cls)
                    obj = mPosition(x1, y1, x2, y2, names[cls])
                    cls_object.append(names[cls])
                    img_object.append(obj)
                    if cls == 1:
                        person = mPosition(x1, y1, x2, y2, names[cls])

            if '人物' in cls_object:
                # print(f'人物当前坐标{(int(person.x1 + person.x2) / 2), int(person.y2)} \n')
                for model in img_object:  # 绘制人物到对象的坐标
                    cv2.line(n_img,
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
                    if abs(person.centerX - monster_box.centerX) < attx and abs(person.centerY - monster_box.y1) < atty:
                        directkeys.key_press('A')
                        # if "领主" in cls_object:
                        #     directkeys.key_press("A")

                        # skill_name = skill_char[int(np.random.randint(len(skill_char), size=1)[0])]
                        # while True:
                        # if skill_rec(skill_name, img):
                        #     directkeys.key_press(skill_name)
                        #     directkeys.key_press(skill_name)
                        #     directkeys.key_press(skill_name)
                        #     break
                        # else:
                        #     skill_name = skill_char[int(np.random.randint(len(skill_char), size=1)[0])]
                        # else:
                        # skill_name = skill_char[int(np.random.randint(len(skill_char), size=1)[0])]
                        # while True:
                        # if skill_rec(skill_name, img0):
                        #     directkeys.key_press(skill_name)
                        #     directkeys.key_press(skill_name)
                        #     directkeys.key_press(skill_name)
                        #     break
                        # else:
                        #     skill_name = skill_char[int(np.random.randint(len(skill_char), size=1)[0])]

                        print('怪物处于攻击距离')
                        if not action_cache:
                            pass
                        elif action_cache not in ["LEFT", "RIGHT", "UP", "DOWN"]:
                            ReleaseKey(direct_dic[action_cache.strip().split("_")[0]])
                            ReleaseKey(direct_dic[action_cache.strip().split("_")[1]])
                            action_cache = None
                        elif action_cache:
                            ReleaseKey(direct_dic[action_cache])
                            action_cache = None
                        # 怪物在英雄右上  ， 左上     左下   右下
                    elif monster_box.centerY - person.centerY < 0 and monster_box.centerX - person.centerX > 0:  # 左下
                        # y方向 小于攻击距离
                        if abs(monster_box.centerY - person.centerY) < thy:
                            action_cache = move(direct="RIGHT", material=True, action_cache=action_cache,
                                                press_delay=press_delay,
                                                release_delay=release_delay)
                            # break
                        #
                        elif person.centerY - monster_box.centerY < monster_box.centerX - person.centerX:
                            action_cache = move(direct="RIGHT_UP", material=True, action_cache=action_cache,
                                                press_delay=press_delay,
                                                release_delay=release_delay)
                            # break
                        elif person.centerY - monster_box.centerY >= monster_box.centerX - person.centerX:
                            action_cache = move(direct="UP", material=True, action_cache=action_cache,
                                                press_delay=press_delay,
                                                release_delay=release_delay)
                            # break
                        print('怪物在右上')
                    elif monster_box.centerY - person.centerY < 0 and monster_box.centerX - person.centerX < 0:
                        if abs(monster_box.centerY - person.centerY) < thy:
                            action_cache = move(direct="LEFT", material=True, action_cache=action_cache,
                                                press_delay=press_delay,
                                                release_delay=release_delay)
                            # break
                        elif person.centerY - monster_box.centerY < person.centerX - monster_box.centerX:
                            action_cache = move(direct="LEFT_UP", material=True, action_cache=action_cache,
                                                press_delay=press_delay,
                                                release_delay=release_delay)
                            # break
                        elif person.centerY - monster_box.centerY >= person.centerX - monster_box.centerX:
                            action_cache = move(direct="UP", material=True, action_cache=action_cache,
                                                press_delay=press_delay,
                                                release_delay=release_delay)
                            # break
                        print('怪物在左上')
                    elif monster_box.centerY - person.centerY > 0 and monster_box.centerX - person.centerX < 0:
                        if abs(monster_box.centerY - person.centerY) < thy:
                            action_cache = move(direct="LEFT", material=True, action_cache=action_cache,
                                                press_delay=press_delay,
                                                release_delay=release_delay)
                            # break
                        elif monster_box.centerY - person.centerY < person.centerX - monster_box.centerX:
                            action_cache = move(direct="LEFT_DOWN", material=True, action_cache=action_cache,
                                                press_delay=press_delay,
                                                release_delay=release_delay)
                            # break
                        elif monster_box.centerY - person.centerY >= person.centerX - monster_box.centerX:
                            action_cache = move(direct="DOWN", material=True, action_cache=action_cache,
                                                press_delay=press_delay,
                                                release_delay=release_delay)
                            # break
                        print('怪物在左下')
                    elif monster_box.centerY - person.centerY > 0 and monster_box.centerX - person.centerX > 0:
                        if abs(monster_box.centerY - person.centerY) < thy:
                            action_cache = move(direct="RIGHT", material=True, action_cache=action_cache,
                                                press_delay=press_delay,
                                                release_delay=release_delay)
                            # break
                        elif monster_box.centerY - person.centerY < monster_box.centerX - person.centerX:
                            action_cache = move(direct="RIGHT_DOWN", material=True, action_cache=action_cache,
                                                press_delay=press_delay,
                                                release_delay=release_delay)
                            # break
                        elif monster_box.centerY - person.centerY >= monster_box.centerX - person.centerX:
                            action_cache = move(direct="DOWN", material=True, action_cache=action_cache,
                                                press_delay=press_delay,
                                                release_delay=release_delay)
                            # break
                        print('怪物在右下')

            if '材料' in cls_object or '金币' in cls_object or '装备' in cls_object:
                pass
                # print(f'物品坐标')
                # min_distance = float("inf")
                # person.centerY = person.centerY + (person.width // 2) * 0.8
                # thx = thx / 2
                # thy = thy / 2
                # for idx, (c, box) in enumerate(zip(cls_object, img_object)):
                #     if box.name == '材料' or box.name == "金币":
                #         dis = ((person.centerX - box.centerX) ** 2 + (person.centerY - box.centerY) ** 2) ** 0.5
                #         if dis < min_distance:
                #             material_box = box
                #             material_index = idx
                #             min_distance = dis
                # if abs(material_box.centerY - person.centerY) < thy and abs(
                #         material_box.centerX - person.centerX) < thx:
                #     if not action_cache:
                #         pass
                #     elif action_cache not in ["LEFT", "RIGHT", "UP", "DOWN"]:
                #         ReleaseKey(direct_dic[action_cache.strip().split("_")[0]])
                #         ReleaseKey(direct_dic[action_cache.strip().split("_")[1]])
                #         action_cache = None
                #     else:
                #         ReleaseKey(direct_dic[action_cache])
                #         action_cache = None
                #     time.sleep(1)
                #     directkeys.key_press("X")
                #     print("捡东西")
                #     # break
                #
                # elif material_box.centerY - person.centerY < 0 and material_box.centerX - person.centerX > 0:
                #
                #     if abs(material_box.centerY - person.centerY) < thy:
                #         action_cache = move(direct="RIGHT", material=True, action_cache=action_cache,
                #                             press_delay=press_delay,
                #                             release_delay=release_delay)
                #         # break
                #     elif person.centerY - material_box.centerY < material_box.centerX - person.centerX:
                #         action_cache = move(direct="RIGHT_UP", material=True, action_cache=action_cache,
                #                             press_delay=press_delay,
                #                             release_delay=release_delay)
                #         # break
                #     elif person.centerY - material_box.centerY >= material_box.centerX - person.centerX:
                #         action_cache = move(direct="UP", material=True, action_cache=action_cache,
                #                             press_delay=press_delay,
                #                             release_delay=release_delay)
                #         # break
                # elif material_box.centerY - person.centerY < 0 and material_box.centerX - person.centerX < 0:
                #     if abs(material_box.centerY - person.centerY) < thy:
                #         action_cache = move(direct="LEFT", material=True, action_cache=action_cache,
                #                             press_delay=press_delay,
                #                             release_delay=release_delay)
                #         # break
                #     elif person.centerY - material_box.centerY < person.centerX - material_box.centerX:
                #         action_cache = move(direct="LEFT_UP", material=True, action_cache=action_cache,
                #                             press_delay=press_delay,
                #                             release_delay=release_delay)
                #         # break
                #     elif person.centerY - material_box.centerY >= person.centerX - material_box.centerX:
                #         action_cache = move(direct="UP", material=True, action_cache=action_cache,
                #                             press_delay=press_delay,
                #                             release_delay=release_delay)
                #         # break
                # elif material_box.centerY - person.centerY > 0 and material_box.centerX - person.centerX < 0:
                #     if abs(material_box.centerY - person.centerY) < thy:
                #         action_cache = move(direct="LEFT", material=True, action_cache=action_cache,
                #                             press_delay=press_delay,
                #                             release_delay=release_delay)
                #         # break
                #     elif material_box.centerY - person.centerY < person.centerX - material_box.centerX:
                #         action_cache = move(direct="LEFT_DOWN", material=True, action_cache=action_cache,
                #                             press_delay=press_delay,
                #                             release_delay=release_delay)
                #         # break
                #     elif material_box.centerY - person.centerY >= person.centerX - material_box.centerX:
                #         action_cache = move(direct="DOWN", material=True, action_cache=action_cache,
                #                             press_delay=press_delay,
                #                             release_delay=release_delay)
                #         # break
                # elif material_box.centerY - person.centerY > 0 and material_box.centerX - person.centerX > 0:
                #     if abs(material_box.centerY - person.centerY) < thy:
                #         action_cache = move(direct="RIGHT", material=True, action_cache=action_cache,
                #                             press_delay=press_delay,
                #                             release_delay=release_delay)
                #         # break
                #     elif material_box.centerY - person.centerY < material_box.centerX - person.centerX:
                #         action_cache = move(direct="RIGHT_DOWN", material=True, action_cache=action_cache,
                #                             press_delay=press_delay,
                #                             release_delay=release_delay)
                #         # break
                #     elif material_box.centerY - person.centerY >= material_box.centerX - person.centerX:
                #         action_cache = move(direct="DOWN", material=True, action_cache=action_cache,
                #                             press_delay=press_delay,
                #                             release_delay=release_delay)
                #         # break

            if '门' in cls_object:
                pass
            # print(f'当前操作指令{action_cache}')
            # ReleaseKey(direct_dic["RIGHT"])
            # ReleaseKey(direct_dic["LEFT"])
            # ReleaseKey(direct_dic["UP"])
            # ReleaseKey(direct_dic["DOWN"])

            # 重新开始
            time_option = -20
            if '通关' in cls_object:
                if not action_cache:
                    pass
                elif action_cache not in ["LEFT", "RIGHT", "UP", "DOWN"]:
                    ReleaseKey(direct_dic[action_cache.strip().split("_")[0]])
                    ReleaseKey(direct_dic[action_cache.strip().split("_")[1]])
                    action_cache = None
                else:
                    ReleaseKey(direct_dic[action_cache])
                    action_cache = None
                if time.time() - time_option > 10:
                    directkeys.key_press("V")
                    print("移动物品到脚下")
                    directkeys.key_press("X")
                    time_option = time.time()
                directkeys.key_press("F10")
                print("通关 - 重新开始F10")

            cv2.imshow('temp',
                       n_img)

            cv2.waitKey(1)
