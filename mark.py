#!/home/shu/Applications/Envs/py3/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QMessageBox, QFileDialog, QApplication
from PyQt5.QtGui import QColor
import os
import os.path as osp
import sys
from config import cfg
from ui import MainUI
from execute import Execute


class Mark(MainUI):

    def __init__(self):
        super().__init__()

        self.exe = Execute()
        self.img_lbl.initXYBoxObjs(self.x_box, self.y_box)
        self.img_lbl.initReferLineNumObj(self.ref_num_lbl)
        self.img_lbl.initHorizonModifyObj(self.horizon_modify_btn)
        self.img_lbl.initSLObsNumObjs(self.small_obs_num_lbl, self.large_obs_num_lbl)

        self.start_flag = False
        self.mode = 'Horizon'
        self.horizon_method = 'Manual'
        self.refer_lines_flag = False
        self.obs_cls = 'Small Obstacle'

    def srcBtnRespond(self):
        home_dir = osp.expanduser('~')
        dir_name = QFileDialog.getExistingDirectory(self, 'Select Directory', home_dir)
        self.src_show_box.setText(dir_name)
        self.exe.setSrcDir(dir_name)

    def dstBtnRespond(self):
        home_dir = osp.expanduser('~')
        dir_name = QFileDialog.getExistingDirectory(self, 'Select Directory', home_dir)
        self.dst_show_box.setText(dir_name)
        self.exe.setDstDir(dir_name)

    def modeRespond(self):
        source = self.sender()
        # print(source.text())
        if source.text() == 'Horizon':
            self.mode = 'Horizon'
            self.img_lbl.setMode(self.mode)
            self.h_square.setStyleSheet("QWidget { background-color: rgb(0, 255, 0); }")
            self.o_square.setStyleSheet("QWidget { background-color: rgb(180, 180, 180); }")
        else:
            self.mode = 'Obstacle'
            self.img_lbl.setMode(self.mode)
            self.h_square.setStyleSheet("QWidget { background-color: rgb(180, 180, 180); }")
            self.o_square.setStyleSheet("QWidget { background-color: rgb(0, 255, 0); }")

            self.img_lbl.setHorizonModifyFlag(False)
            self.horizon_modify_btn.setChecked(False)

    def horizonMethodRespond(self):
        source = self.sender()
        if source.text() == 'Manual':
            self.horizon_method = 'Manual'
        else:
            self.horizon_method = 'Auto'

    def referLinesBtnRespond(self, value):
        self.img_lbl.setReferLines(value)

    def horizonModifyBtnRespond(self, value):
        if not self.start_flag:
            QMessageBox.warning(self, 'warning', 'Please press [Start] or [Restore]!!!')
            self.horizon_modify_btn.setChecked(False)
            return

        if value:
            if self.mode != 'Horizon':
                QMessageBox.warning(self, 'warning', 'The [Mode] must be "Horizon" !!!')
                self.horizon_modify_btn.setChecked(False)
                return

            ret = self.img_lbl.setHorizonModifyFlag(value)
            if ret < 0:
                QMessageBox.warning(self, 'warning', 'The horizon has not been marked!!!')
                self.horizon_modify_btn.setChecked(False)
                return
        else:
            self.img_lbl.setHorizonModifyFlag(value)

    def obsClsBtnRespond(self):
        source = self.sender()
        if source.text() == 'Small Obstacle':
            self.obs_cls = 'Small Obstacle'
            self.img_lbl.setObsCls(self.obs_cls)
            obs_cls_col = QColor(*cfg.SMALL_OBS_COLOR)
            self.obs_cls_square.setStyleSheet("QWidget { background-color: %s }" % obs_cls_col.name())
        else:
            self.obs_cls = 'Large Obstacle'
            self.img_lbl.setObsCls(self.obs_cls)
            obs_cls_col = QColor(*cfg.LARGE_OBS_COLOR)
            self.obs_cls_square.setStyleSheet("QWidget { background-color: %s }" % obs_cls_col.name())
        # print(self.obs_cls)

    def startBtnRespond(self):
        if self.start_flag:
            reply = QMessageBox.question(self, 'warning', "Are you sure to restart?",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.No:
                return
            else:
                self.exe.reset()

        ret = self.exe.start()
        if ret == -1:
            QMessageBox.warning(self, 'warning', 'Please Select SRC Path!!!')
            return
        if ret == -2:
            QMessageBox.warning(self, 'warning', 'Please Select DST Path!!!')
            return
        if ret == -3:
            QMessageBox.warning(self, 'warning', 'No jpg or png images in SRC Path!!!')
            return

        self.display(isFinished=False)
        self.img_lbl.setEnableImageFlag(True)
        self.img_lbl.reset()

        self.start_flag = True

    def restoreBtnRespond(self):
        reply = QMessageBox.question(self, 'warning', "Are you sure to restore?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.No:
            return

        ret = self.exe.restore()
        if ret < 0:
            QMessageBox.warning(self, 'warning', 'Some problems exist, cannot restore!!!')
            return

        self.display(isFinished=False)
        self.img_lbl.setEnableImageFlag(True)
        self.img_lbl.reset()

        self.start_flag = True

    def undoBtnRespond(self):
        if not self.start_flag:
            QMessageBox.warning(self, 'warning', 'Please press [Start] or [Restore]!!!')
            return
        ret = self.img_lbl.undo()
        if ret == -1:
            QMessageBox.warning(self, 'warning', 'All marks are removed!!!')

    def nextBtnRespond(self):
        if not self.start_flag:
            QMessageBox.warning(self, 'warning', 'Please press [Start] or [Restore]!!!')
            return

        horizon_data, obs_data = self.img_lbl.getData()
        ret = self.exe.saveData(horizon_data, obs_data)
        if ret == -1:
            QMessageBox.warning(self, 'warning', 'Marking Horizon has not completed!!!')
            return
        if ret == -2:
            self.display(isFinished=True)
            reply = QMessageBox.question(self, 'warning',
                                         'All marking has completed!!!, Are you sure to finish?',
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if reply == QMessageBox.No:
                self.img_lbl.reset()
                return
            self.reset()
            return

        self.img_lbl.reset()
        self.display(isFinished=False)

    def reset(self):
        self.start_flag = False

        self.src_show_box.clear()
        self.dst_show_box.clear()

        self.img_lbl.clear()
        self.img_lbl.setEnableImageFlag(False)
        self.img_lbl.reset()

        self.cur_img_box.clear()
        self.no_box.clear()
        self.total_box.clear()
        self.pbar.reset()
        self.x_box.clear()
        self.y_box.clear()

        self.ref_num_lbl.clear()
        self.small_obs_num_lbl.clear()
        self.large_obs_num_lbl.clear()

        self.exe.setSrcDir('')
        self.exe.setDstDir('')
        self.exe.reset()
        self.exe.saveConfig()

    def display(self, isFinished):
        cur_image_name = self.exe.getCurrentImageName()
        cur_image_no = self.exe.getCurrentImageNo()
        total_image_num = self.exe.getTotalImageNum()

        src_dir = self.exe.getSrcDir()
        dst_dir = self.exe.getDstDir()
        self.src_show_box.setText(src_dir)
        self.dst_show_box.setText(dst_dir)
        self.cur_img_box.setText(cur_image_name)
        self.no_box.setText(str(cur_image_no + 1))
        self.total_box.setText(str(total_image_num))

        if isFinished:
            pb_val = int((float(cur_image_no + 1) / total_image_num) * 100)
        else:
            pb_val = int((float(cur_image_no) / total_image_num) * 100)
        self.pbar.setValue(pb_val)

        self.ref_num_lbl.setText(str(0))
        self.small_obs_num_lbl.setText(str(0))
        self.large_obs_num_lbl.setText(str(0))

        self.img_lbl.loadFromDisk(osp.join(cfg.SRC_DIR, cur_image_name))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    m = Mark()
    sys.exit(app.exec_())
