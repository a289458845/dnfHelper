import numpy as np

def nms(
          
        inference : np.ndarray,
        conf_thres : float,
        sigma : float,
        iou_thres : float

    ) -> np.ndarray:
        """
        soft - nms
        """
        pred = np.squeeze(inference)
        conf = pred[..., 4] > conf_thres

        box = pred[conf == True]
        cls_cinf = box[..., 5:]

        cls = []
        for i in range(len(cls_cinf)):
            cls.append(int(np.argmax(cls_cinf[i])))
        all_cls = list(set(cls))

        output = []
        for i in range(len(all_cls)):
            curr_cls = all_cls[i]
            curr_cls_box = []
            curr_out_box = []
            for j in range(len(cls)):
                if cls[j] == curr_cls:
                    box[j][5] = curr_cls
                    curr_cls_box.append(box[j][:6])
            curr_cls_box = np.array(curr_cls_box)

            y = np.copy(curr_cls_box)
            y[:, 0] = curr_cls_box[:, 0] - curr_cls_box[:, 2] / 2
            y[:, 1] = curr_cls_box[:, 1] - curr_cls_box[:, 3] / 2
            y[:, 2] = curr_cls_box[:, 0] + curr_cls_box[:, 2] / 2
            y[:, 3] = curr_cls_box[:, 1] + curr_cls_box[:, 3] / 2

            curr_cls_box = y

            x1 = curr_cls_box[:, 0]
            y1 = curr_cls_box[:, 1]
            x2 = curr_cls_box[:, 2]
            y2 = curr_cls_box[:, 3]

            scores = curr_cls_box[:, 4] 
            areas = (x2 - x1 + 1) * (y2 - y1 + 1)
            order = scores.argsort()[::-1]
            keep = []

            while order.size > 0:
                i = order[0]
                keep.append(i)
                xx1 = np.maximum(x1[i], x1[order[1:]])
                yy1 = np.maximum(y1[i], y1[order[1:]])
                xx2 = np.minimum(x2[i], x2[order[1:]])
                yy2 = np.minimum(y2[i], y2[order[1:]])
                w = np.maximum(0.0, xx2 - xx1 + 1)
                h = np.maximum(0.0, yy2 - yy1 + 1)
                inter = w * h
                eps = np.finfo(areas.dtype).eps 
                ovr = inter / np.maximum(eps, areas[i] + areas[order[1:]] - inter)
                weight = np.exp(-ovr*ovr/sigma)
                scores[order[1:]] *= weight
                score_order = scores[order[1:]].argsort()[::-1] + 1
                order = order[score_order]
                keep_ids = np.where(scores[order]>iou_thres)[0]
                order = order[keep_ids]
                curr_out_box = keep

            for k in curr_out_box:
                output.append(curr_cls_box[k])

        outbox = np.array(output)
        result = None if len(outbox) == 0 else outbox

        return result