import os
import cv2

from detectron2.config import get_cfg
from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.utils.visualizer import Visualizer, ColorMode
from detectron2.data import MetadataCatalog

class Model():
    def __init__(self):
        self.classes = ["Blacky", "Niche"]

        # Configure model
        cfg = get_cfg()
        cfg.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"))
        cfg.DATASETS.TEST = ("cats_val")
        cfg.MODEL.WEIGHTS = os.path.join("model_final.pth")
        cfg.MODEL.ROI_HEADS.NUM_CLASSES = 2
        cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.7

        self.predictor = DefaultPredictor(cfg)
        self.isPredicting = False

    def detect(self, image):
        outputs = self.predictor(image)

        # pred_classes = (outputs["instances"].pred_classes).detach()
        # pred_scores = (outputs["instances"].scores).detach()

        # for c,s in zip(pred_classes, pred_scores):
        #     print(f"Class {self.classes[c]}, {s * 100:.2f}%")

        v = Visualizer(image[:, :, ::-1], 
            metadata = MetadataCatalog.get("cats_val").set(
                thing_classes=self.classes,
                thing_colors=[(177, 205, 223), (223, 205, 177)]),
            scale = 0.8,
            instance_mode = ColorMode.IMAGE_BW
        )
        v = v.draw_instance_predictions(outputs["instances"].to("cpu"))

        self.isPredicting = False

        #return pred_classes, pred_scores
        return v.get_image()[:, :, ::-1]

    