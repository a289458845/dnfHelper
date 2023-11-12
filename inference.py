import onnx
import onnxruntime as ort
import cv2
import numpy as np
from nms import nms


class inference:
    def __init__(self, infer_mode: str, thread: int, model_path: str) -> None:
        self.infer_mode = infer_mode
        self.thread = thread
        self.model_path = model_path

        self.input_name = None
        self.out_name = None
        self.onnx_session = None
        self.mode = None

        self.__load_mode()
        self.__init_mode()

    def __load_mode(self):  # 加载模型
        self.mode = onnx.load(self.model_path)

    def __init_mode(self):  # 初始化处理
        session_option = ort.SessionOptions()

        provider = [
            'DmlExecutionProvider',
            'CPUExecutionProvider'
        ]
        self.onnx_session = ort.InferenceSession(
            self.mode.SerializePartialToString(),
            providers=provider,
            sess_options=session_option
        )

        self.input_name = self.onnx_session.get_inputs()[0].name
        self.out_name = self.onnx_session.get_outputs()[0].name
        print('加载成功')

    def __preprocess(self, img: np.ndarray) -> np.ndarray:  # 前处理
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # 处理图片重BGR 转到 RBG
        img = img.transpose(2, 0, 1)  # 图像维度转换 将原本通道维度(第三维度) 移动到第一维度
        img = img.astype(dtype=np.float32) / 255.0  # 将图像转换为float32的浮点类型，并将像素值归一到化到 0 - 1的范围
        img = np.expand_dims(img, axis=0)  # 图像数组的第0个维度上增加一个维度，为了将单张图像拓展为一个批次 输入
        return img

    def infer(self,
                img : np.ndarray) -> np.ndarray:  # 推理方法
        img = self.__preprocess(img)
        img = self.onnx_session.run(
            [self.out_name],
            {self.input_name: img}
        )[0]
        result = nms(img, 0.65, 0.5, 0.25) # bbox置信度 ， 距离惩罚系数，交并比
        return result


if __name__ == '__main__':
    infer = inference(
        infer_mode=None,
        thread=4,
        model_path='yolov5s_best.onnx'
    )


    img = cv2.imread('test.jpg')
    resizeImg = cv2.resize(img,(640,640))
    result = infer.infer(resizeImg)
    print(f'识别结果:{result}')
