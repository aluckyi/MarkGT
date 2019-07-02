#!/home/shu/Applications/Envs/py3/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap, QImage, QPainter, QPen, QBrush, QColor
from PyQt5.QtCore import QRect, Qt
import cv2
from config import cfg


class ImgLabel(QLabel):

    def __init__(self, *__args):
        super().__init__(*__args)

        self.enableFlag = False
        self.ispressed = False
        self.isMarking = False

        self.mode = 'Horizon'
        self.refer_lines_x = []
        self.horizon_point = ()
        self.horizon_data = []
        self.obs_cls = 'Small Obstacle'
        self.obs_rect = []
        self.obs_data = []

        self.referLinesX = []
        ref_line_num = cfg.REF_LINE_NUM
        image_width = cfg.IMAGE_WIDTH
        interval = image_width // (ref_line_num - 1)
        for x in range(ref_line_num - 1):
            self.referLinesX.append(x * interval)
        self.referLinesX.append(image_width - 1)

        self.pen = QPen()

    def initXYBoxObjs(self, x_box, y_box):
        self.x_box = x_box
        self.y_box = y_box

    def initSLObsNumObjs(self, small_num_lbl, large_num_lbl):
        self.small_num_lbl = small_num_lbl
        self.large_num_lbl = large_num_lbl

    def setEnableImageFlag(self, flag):
        self.enableFlag = flag

    def setMode(self, mode):
        self.mode = mode

    def setObsCls(self, cls):
        self.obs_cls = cls

    def setReferLinesFlag(self, flag):
        if flag:
            self.refer_lines_x = self.referLinesX
        else:
            self.refer_lines_x = []
        self.update()

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

        # previous display
        # display reference lines
        self.pen.setWidth(2)
        self.pen.setColor(QColor(255, 255, 255))
        painter.setPen(self.pen)
        image_height = cfg.IMAGE_HEIGHT
        for x in self.refer_lines_x:
            painter.drawLine(x, 0, x, image_height - 1)
        # display key points of horizon
        if len(self.horizon_data) > 0:
            for point in self.horizon_data:
                self.pen.setWidth(2)
                self.pen.setColor(QColor(0, 0, 0))
                painter.setPen(self.pen)
                brush = QBrush(Qt.SolidPattern)
                brush.setColor(QColor(255, 255, 0))
                painter.setBrush(brush)
                painter.drawEllipse(point[0] - 5, point[1] - 5, 10, 10)
        # display obstacles
        if len(self.obs_data) > 0:
            self.pen.setWidth(cfg.LINE_WIDTH)
            brush = QBrush(Qt.BDiagPattern)  # FDiagPattern, BDiagPattern
            brush.setColor(QColor(0, 255, 0))
            painter.setBrush(brush)
            for obs_dict in self.obs_data:
                for obs_cls, obs_rect in obs_dict.items():
                    if obs_cls == 'Small Obstacle':
                        self.pen.setColor(QColor(*cfg.SMALL_OBS_COLOR))
                    elif obs_cls == 'Large Obstacle':
                        self.pen.setColor(QColor(*cfg.LARGE_OBS_COLOR))
                    painter.setPen(self.pen)
                    rect = QRect(min(obs_rect[0][0], obs_rect[1][0]),
                                 min(obs_rect[0][1], obs_rect[1][1]),
                                 abs(obs_rect[1][0] - obs_rect[0][0]) + 1,
                                 abs(obs_rect[1][1] - obs_rect[0][1]) + 1)
                    painter.drawRect(rect.x(), rect.y(), rect.width(), rect.height())

        # temporate display
        if self.mode == 'Horizon':
            if self.horizon_point is not ():
                self.pen.setWidth(2)
                self.pen.setColor(QColor(0, 0, 0))
                painter.setPen(self.pen)
                brush = QBrush(Qt.SolidPattern)
                brush.setColor(QColor(255, 255, 0))
                painter.setBrush(brush)
                painter.drawEllipse(self.horizon_point[0]-5, self.horizon_point[1]-5, 10, 10)
        elif self.mode == 'Obstacle':
            if len(self.obs_rect) == 2:
                self.pen.setWidth(cfg.LINE_WIDTH)
                if self.obs_cls == 'Small Obstacle':
                    self.pen.setColor(QColor(*cfg.SMALL_OBS_COLOR))
                elif self.obs_cls == 'Large Obstacle':
                    self.pen.setColor(QColor(*cfg.LARGE_OBS_COLOR))
                painter.setPen(self.pen)
                brush = QBrush(Qt.BDiagPattern)  # FDiagPattern, BDiagPattern
                brush.setColor(QColor(0, 0, 255))
                painter.setBrush(brush)
                rect = QRect(min(self.obs_rect[0][0], self.obs_rect[1][0]),
                             min(self.obs_rect[0][1], self.obs_rect[1][1]),
                             abs(self.obs_rect[1][0] - self.obs_rect[0][0]) + 1,
                             abs(self.obs_rect[1][1] - self.obs_rect[0][1]) + 1)
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

        if self.mode == 'Horizon':
            self.horizon_point = ()
            if len(self.horizon_data) < cfg.REF_LINE_NUM:
                self.horizon_point = (self.referLinesX[len(self.horizon_data)], y)
        elif self.mode == 'Obstacle':
            if not self.isMarking:
                self.isMarking = True
                self.setMouseTracking(True)
                self.obs_rect = []
                self.obs_rect.append((x, y))
                self.obs_rect.append((x, y))

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

        if self.mode == 'Horizon':
            if len(self.horizon_data) < cfg.REF_LINE_NUM:
                self.horizon_point = (self.referLinesX[len(self.horizon_data)], y)
                self.horizon_data.append(self.horizon_point)
                self.horizon_point = ()
        elif self.mode == 'Obstacle':
            if self.isMarking:
                if self.obs_rect[0] != self.obs_rect[1]:
                    self.isMarking = False
                    self.setMouseTracking(False)
                self.obs_rect[1] = (x, y)

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

        if self.mode == 'Horizon':
            if self.ispressed:
                if len(self.horizon_data) < cfg.REF_LINE_NUM:
                    self.horizon_point = (self.referLinesX[len(self.horizon_data)], y)
        elif self.mode == 'Obstacle':
            if self.isMarking:
                self.obs_rect[1] = (x, y)

        self.update()

    def keyPressEvent(self, event):
        super().keyPressEvent(event)
        if not self.enableFlag:
            return
        if self.mode == 'Obstacle':
            if event.key() == Qt.Key_Space:
                if len(self.obs_rect) == 2 and not self.isMarking:
                    self.obs_rect = [(min(self.obs_rect[0][0], self.obs_rect[1][0]),
                                      min(self.obs_rect[0][1], self.obs_rect[1][1])),
                                     (max(self.obs_rect[0][0], self.obs_rect[1][0]),
                                      max(self.obs_rect[0][1], self.obs_rect[1][1]))]
                    self.obs_data.append({self.obs_cls: self.obs_rect})
                    self.obs_rect = []

                    if self.obs_cls == 'Small Obstacle':
                        self.small_num_lbl.setText(str(int(self.small_num_lbl.text()) + 1))
                    elif self.obs_cls == 'Large Obstacle':
                        self.large_num_lbl.setText(str(int(self.large_num_lbl.text()) + 1))
        self.update()
