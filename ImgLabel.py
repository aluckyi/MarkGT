#!/home/shu/Applications/Envs/py3/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap, QImage, QPainter, QPen, QBrush, QColor
from PyQt5.QtCore import QRect, Qt

import os.path as osp
import cv2
from config import cfg


class ImgLabel(QLabel):

    def __init__(self, *__args):
        super().__init__(*__args)

        self.enableFlag = False
        self.ispressed = False
        self.isMarking = False
        self.rectPoints = []

        self.pen = QPen()

    def initXYBoxObjs(self, x_box, y_box):
        self.x_box = x_box
        self.y_box = y_box

    def setEnableImageFlag(self, flag):
        self.enableFlag = flag

    def reset(self):
        self.ispressed = False
        self.update()

    def loadFromDisk(self, path):
        # pixmap = QPixmap(path)
        image = cv2.imread(path)
        if image.shape[0] != cfg.IMAGE_HEIGHT or image.shape[1] != cfg.IMAGE_WIDTH:
            image = cv2.resize(image, (cfg.IMAGE_WIDTH, cfg.IMAGE_HEIGHT), interpolation=cv2.INTER_CUBIC)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        pixmap = QImage(image.data, image.shape[1], image.shape[0], QImage.Format_RGB888)
        self.setPixmap(QPixmap.fromImage(pixmap))

    def paintEvent(self, event):
        super().paintEvent(event)

        if not self.enableFlag:
            return
        painter = QPainter(self)
        self.pen.setWidth(cfg.LINE_WIDTH)
        self.pen.setColor(QColor(255, 0, 255))
        painter.setPen(self.pen)
        brush = QBrush(Qt.BDiagPattern)  # FDiagPattern, BDiagPattern
        brush.setColor(QColor(0, 0, 255))
        painter.setBrush(brush)
        if len(self.rectPoints) == 2:
            rect = QRect(min(self.rectPoints[0][0], self.rectPoints[1][0]),
                         min(self.rectPoints[0][1], self.rectPoints[1][1]),
                         abs(self.rectPoints[1][0] - self.rectPoints[0][0]),
                         abs(self.rectPoints[1][1] - self.rectPoints[0][1]))
            painter.drawRect(rect.x(), rect.y(), rect.width(), rect.height())

    def mousePressEvent(self, event):
        if not self.enableFlag:
            return

        x = event.x()
        y = event.y()
        if x < 0 or x >= cfg.IMAGE_WIDTH or y < 0 or y >= cfg.IMAGE_HEIGHT:
            return
        self.x_box.setText(str(x))
        self.y_box.setText(str(y))

        self.ispressed = True
        self.isMarking = not self.isMarking
        if self.isMarking:
            self.setMouseTracking(True)
            self.rectPoints = []
            self.rectPoints.append((x, y))
            self.rectPoints.append((x, y))
        else:
            self.setMouseTracking(False)
            if len(self.rectPoints) == 2:
                self.rectPoints[1] = (x, y)

        self.update()

    def mouseReleaseEvent(self, event):
        if not self.enableFlag:
            return

        x = event.x()
        y = event.y()
        if x < 0 or x >= cfg.IMAGE_WIDTH or y < 0 or y >= cfg.IMAGE_HEIGHT:
            return
        self.x_box.setText(str(x))
        self.y_box.setText(str(y))

        self.ispressed = False

        self.update()

    def mouseMoveEvent(self, event):
        if not self.enableFlag:
            return
        x = event.x()
        y = event.y()
        if x < 0 or x >= cfg.IMAGE_WIDTH or y < 0 or y >= cfg.IMAGE_HEIGHT:
            return
        self.x_box.setText(str(x))
        self.y_box.setText(str(y))

        if self.isMarking:
            self.rectPoints[1] = (x, y)

        self.update()







