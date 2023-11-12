from mss import mss
import numpy as np
import cv2


class grab_screen:
    """
    屏幕截图
    grab_size 截图的尺寸
    screen_x 屏幕的宽度
    screen_y 屏幕的高度
    """

    def __init__(self,
                 grab_size: int,
                 screen_x: int,
                 screen_y: int
                 ) -> None:
        self.grab_area = {
            'left': 0,
            'top': 0,
            'width': 800,
            'height': 600
        }
        self.sct = mss()

    def cap(self) -> np.ndarray:
        img = self.sct.grab(self.grab_area)
        img = np.array(img)
        # 获取原始图像的尺寸
        height, width = img.shape[:2]

        # 计算缩放比例
        scale_percent = min(640 / width, 640 / height)

        # 计算调整后的尺寸
        new_width = int(width * scale_percent)
        new_height = int(height * scale_percent)

        # 调整图像尺寸
        resized_img = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_AREA)
        # 创建一个空白的640x640画布
        canvas = np.zeros((640, 640, 3), dtype=np.uint8)

        # 计算填充的位置
        top = (640 - resized_img.shape[0]) // 2
        bottom = 640 - resized_img.shape[0] - top
        left = (640 - resized_img.shape[1]) // 2
        right = 640 - resized_img.shape[1] - left

        # 在画布上添加填充
        padded_img = cv2.copyMakeBorder(resized_img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=(0, 0, 0))
        return padded_img


if __name__ == '__main__':
    sc = grab_screen(640, 1920, 1080)
    from time import perf_counter as tp

    while True:
        t1 = tp()

        img = sc.cap()

        print(f'单次截图耗时: {(tp() - t1) * 100}ms')
        cv2.imshow(
            'temp',
            img
        )

        cv2.waitKey(1)
