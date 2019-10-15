import matplotlib.pyplot as plt
import numpy as np


class PostProcess():
    def __init__(self, class_names, pred_threshold=0.9):
        self.pred_threshold = pred_threshold
        self.class_names = class_names

    def set_top_score(self, pred_result):
        # Parse the outputs.
        det_label = pred_result[0][:, 0]
        det_conf = pred_result[0][:, 1]

        # get top score result
        self.top_indices = [i for i, conf in enumerate(
            det_conf) if conf >= self.pred_threshold]
        self.top_conf = det_conf[self.top_indices]
        self.top_label_indices = det_label[self.top_indices].tolist()

    def get_list_pi(self):
        list_label = []
        for i in range(self.top_conf.shape[0]):
            label = int(self.top_label_indices[i])
            label_name = self.class_names[label]
            list_label.append(label_name)

        return list_label

    def save_image(self, img, pred_result, savepath):
        colors = plt.cm.hsv(np.linspace(0, 1, 35)).tolist()
        plt.tick_params(labelbottom=False,
                        labelleft=False,
                        labelright=False,
                        labeltop=False)
        plt.tick_params(bottom=False,
                        left=False,
                        right=False,
                        top=False)

        plt.imshow(img / 255.)
        currentAxis = plt.gca()

        det_xmin = pred_result[0][:, 2]
        det_ymin = pred_result[0][:, 3]
        det_xmax = pred_result[0][:, 4]
        det_ymax = pred_result[0][:, 5]

        top_xmin = det_xmin[self.top_indices]
        top_ymin = det_ymin[self.top_indices]
        top_xmax = det_xmax[self.top_indices]
        top_ymax = det_ymax[self.top_indices]

        for i in range(self.top_conf.shape[0]):
            xmin = int(round(top_xmin[i] * img.shape[1]))
            ymin = int(round(top_ymin[i] * img.shape[0]))
            xmax = int(round(top_xmax[i] * img.shape[1]))
            ymax = int(round(top_ymax[i] * img.shape[0]))

            label = int(self.top_label_indices[i])
            score = self.top_conf[i]
            label_name = self.class_names[label]
            display_txt = '{:0.2f}, {}'.format(score, label_name)
            coords = (xmin, ymin), xmax - xmin + 1, ymax - ymin + 1
            color = colors[label]

            currentAxis.add_patch(plt.Rectangle(
                *coords, fill=False, edgecolor=color, linewidth=2))
            currentAxis.text(xmin, ymin, display_txt, bbox={
                             'facecolor': color, 'alpha': 1.0})

        plt.savefig(savepath)
