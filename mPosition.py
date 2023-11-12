
class mPosition:
    def __init__(self, x1, y1, x2, y2, name):
        """
        创建一个 mPosition 对象

        Args:
            x1 (int): 矩形左上角的 x 坐标
            y1 (int): 矩形左上角的 y 坐标
            x2 (int): 矩形右下角的 x 坐标
            y2 (int): 矩形右下角的 y 坐标
        """
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.center = ((x1 + x2) / 2, (y1 + y2) / 2)
        self.bottomCenter = ((x1 + x2) / 2, y2)
        self.name = name
        self.centerX = (x1 + x2) / 2
        self.centerY = (y1 + y2) / 2
        self.width = x2 - x1
        self.height = y2 - y1
