#!/home/shu/Applications/Envs/py3/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap, QImage, QPainter, QPen, QBrush, QColor
from PyQt5.QtCore import QRect, Qt
import cv2
import numpy as np
from config import cfg


class ImgLabel(QLabel):

    def __init__(self, *__args):
        super().__init__(*__args)

        self.enable_flag = False
        self.is_pressed = False
        self.is_marking = False
        self.horizon_modify_flag = False

        self.horizon_modified_idx = -1

        self.mode = 'Horizon'
        self.refer_lines_x = []
        self.obs_cls = 'Small Obstacle'

        self.horizon_point = ()
        self.horizon_data = []
        self.obs_rect = []
        self.obs_data = []

        self.history = []

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

    def initReferLineNumObj(self, ref_num_lbl):
        self.ref_num_lbl = ref_num_lbl

    def initHorizonModifyObj(self, horizon_modify_btn):
        self.horizon_modify_btn = horizon_modify_btn

    def initSLObsNumObjs(self, small_num_lbl, large_num_lbl):
        self.small_num_lbl = small_num_lbl
        self.large_num_lbl = large_num_lbl

    def setEnableImageFlag(self, flag):
        self.enable_flag = flag
        self.update()

    def setMode(self, mode):
        if self.mode == mode:
            return
        self.mode = mode
        self.horizon_point = ()
        self.obs_rect = []
        self.update()

    def setObsCls(self, cls):
        if self.obs_cls == cls:
            return
        self.obs_cls = cls
        self.horizon_point = ()
        self.obs_rect = []
        self.update()

    def setReferLines(self, flag):
        if flag:
            self.refer_lines_x = self.referLinesX
        else:
            self.refer_lines_x = []
        self.update()

    def setHorizonModifyFlag(self, flag):
        if flag and len(self.horizon_data) == 0:
            return -1
        self.horizon_modify_flag = flag
        return 0

    def reset(self):
        self.is_pressed = False
        self.is_marking = False

        self.horizon_modify_flag = False
        self.horizon_modify_btn.setChecked(False)

        self.horizon_modified_idx = -1

        self.horizon_point = ()
        self.horizon_data = []
        self.obs_rect = []
        self.obs_data = []

        self.history = []

        self.update()

    def undo(self):
        if len(self.obs_rect) != 0:
            self.obs_rect = []
            self.update()
            return 0

        if len(self.history) == 0:
            return -1

        cls = self.history.pop()
        if cls == 'Horizon':
            self.horizon_data.pop()
            self.ref_num_lbl.setText(str(int(self.ref_num_lbl.text()) - 1))
        elif cls == 'Obstacle':
            obs_dict = self.obs_data.pop()
            for obs_cls, obs_rect in obs_dict.items():
                if obs_cls == 'Small Obstacle':
                    self.small_num_lbl.setText(str(int(self.small_num_lbl.text()) - 1))
                elif obs_cls == 'Large Obstacle':
                    self.large_num_lbl.setText(str(int(self.large_num_lbl.text()) - 1))
        self.update()
        return 0

    def getData(self):
        return self.horizon_data, self.obs_data

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

        if not self.enable_flag:
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
            for idx, point in enumerate(self.horizon_data):
                if idx == self.horizon_modified_idx:  # modify marked point of horizon
                    continue
                self.pen.setWidth(2)
                self.pen.setColor(QColor(0, 0, 0))
                painter.setPen(self.pen)
                brush = QBrush(Qt.SolidPattern)
                brush.setColor(QColor(255, 255, 0))
                painter.setBrush(brush)
                painter.drawEllipse(point[0] - 5, point[1] - 5, 11, 11)
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
                painter.drawEllipse(self.horizon_point[0] - 5, self.horizon_point[1] - 5, 11, 11)

                if self.horizon_modified_idx != -1:  # modify marked point of horizon
                    self.pen.setWidth(3)
                    self.pen.setColor(QColor(255, 0, 0))
                    painter.setPen(self.pen)
                    painter.drawEllipse(self.horizon_point[0] - 8, self.horizon_point[1] - 8, 17, 17)

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

    def getShortestDistIdx(self, point):
        idx = -1
        dist_list = []
        for p in self.horizon_data:
            dist = np.sqrt(np.square(float(point[0] - p[0])) + np.square(float(point[1] - p[1])))
            dist_list.append(dist)
        if len(dist_list) == 0:
            return idx, -1

        idx = np.argmin(dist_list)
        dist = dist_list[idx]
        return idx, dist

    def mousePressEvent(self, event):
        if not self.enable_flag:
            return

        x = event.x()
        y = event.y()
        if x < 0 or x >= cfg.IMAGE_WIDTH or y < 0 or y >= cfg.IMAGE_HEIGHT:
            return
        self.x_box.setText(str(x))
        self.y_box.setText(str(y))

        self.is_pressed = True

        if self.mode == 'Horizon':
            self.horizon_point = ()
            if not self.horizon_modify_flag:
                if len(self.horizon_data) < cfg.REF_LINE_NUM:
                    self.horizon_point = (self.referLinesX[len(self.horizon_data)], y)
            else:  # modify marked point of horizon
                idx, dist = self.getShortestDistIdx((x, y))
                if idx < 0 or dist > 10:
                    return
                self.horizon_modified_idx = idx
                p_x = self.horizon_data[self.horizon_modified_idx][0]
                self.horizon_point = (p_x, y)

        elif self.mode == 'Obstacle':
            if not self.is_marking:
                self.is_marking = True
                self.setMouseTracking(True)
                self.obs_rect = []
                self.obs_rect.append((x, y))
                self.obs_rect.append((x, y))

        self.update()

    def mouseReleaseEvent(self, event):
        if not self.enable_flag:
            return

        x = event.x()
        y = event.y()
        if x < 0 or x >= cfg.IMAGE_WIDTH or y < 0 or y >= cfg.IMAGE_HEIGHT:
            return
        self.x_box.setText(str(x))
        self.y_box.setText(str(y))

        self.is_pressed = False

        if self.mode == 'Horizon':
            if not self.horizon_modify_flag:
                if len(self.horizon_data) < cfg.REF_LINE_NUM:
                    self.horizon_point = (self.referLinesX[len(self.horizon_data)], y)
                    self.horizon_data.append(self.horizon_point)
                    self.horizon_point = ()
                    self.history.append(self.mode)

                    self.ref_num_lbl.setText(str(int(self.ref_num_lbl.text()) + 1))
            else:  # modify marked point of horizon
                if self.horizon_modified_idx != -1:
                    p_x = self.horizon_data[self.horizon_modified_idx][0]
                    self.horizon_point = (p_x, y)
                    self.horizon_data[self.horizon_modified_idx] = self.horizon_point
                    self.horizon_point = ()
                    self.horizon_modified_idx = -1

        elif self.mode == 'Obstacle':
            if self.is_marking:
                if self.obs_rect[0] != self.obs_rect[1]:
                    self.is_marking = False
                    self.setMouseTracking(False)
                self.obs_rect[1] = (x, y)

        self.update()

    def mouseMoveEvent(self, event):
        if not self.enable_flag:
            return
        x = event.x()
        y = event.y()
        if x < 0 or x >= cfg.IMAGE_WIDTH or y < 0 or y >= cfg.IMAGE_HEIGHT:
            return
        self.x_box.setText(str(x))
        self.y_box.setText(str(y))

        if self.mode == 'Horizon':
            if self.is_pressed:
                if not self.horizon_modify_flag:
                    if len(self.horizon_data) < cfg.REF_LINE_NUM:
                        self.horizon_point = (self.referLinesX[len(self.horizon_data)], y)
                else:  # modify marked point of horizon
                    if self.horizon_modified_idx != -1:
                        p_x = self.horizon_data[self.horizon_modified_idx][0]
                        self.horizon_point = (p_x, y)
        elif self.mode == 'Obstacle':
            if self.is_marking:
                self.obs_rect[1] = (x, y)

        self.update()

    def keyPressEvent(self, event):
        super().keyPressEvent(event)
        if not self.enable_flag:
            return
        if self.mode == 'Obstacle':
            if event.key() == Qt.Key_Space:
                if len(self.obs_rect) == 2 and not self.is_marking:
                    self.obs_rect = [(min(self.obs_rect[0][0], self.obs_rect[1][0]),
                                      min(self.obs_rect[0][1], self.obs_rect[1][1])),
                                     (max(self.obs_rect[0][0], self.obs_rect[1][0]),
                                      max(self.obs_rect[0][1], self.obs_rect[1][1]))]
                    self.obs_data.append({self.obs_cls: self.obs_rect})
                    self.obs_rect = []
                    self.history.append(self.mode)

                    if self.obs_cls == 'Small Obstacle':
                        self.small_num_lbl.setText(str(int(self.small_num_lbl.text()) + 1))
                    elif self.obs_cls == 'Large Obstacle':
                        self.large_num_lbl.setText(str(int(self.large_num_lbl.text()) + 1))
        self.update()
