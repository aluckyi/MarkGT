#!/home/shu/Applications/Envs/py3/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap, QImage
import os.path as osp
import cv2
from config import cfg


class ImgLabel(QLabel):

    def __init__(self, *__args):
        super().__init__(*__args)

        self.enableFlag = False
        self.ispressed = False

    def loadFromDisk(self, path):
        # pixmap = QPixmap(path)
        image = cv2.imread(path)
        if image.shape[0] != cfg.IMAGE_HEIGHT or image.shape[1] != cfg.IMAGE_WIDTH:
            image = cv2.resize(image, (cfg.IMAGE_WIDTH, cfg.IMAGE_HEIGHT), interpolation=cv2.INTER_CUBIC)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        pixmap = QImage(image.data, image.shape[1], image.shape[0], QImage.Format_RGB888)
        self.setPixmap(QPixmap.fromImage(pixmap))






