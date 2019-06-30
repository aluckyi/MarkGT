#!/home/shu/Applications/Envs/py3/bin/python3
# -*- coding: utf-8 -*-


from PyQt5.QtWidgets import QFileDialog, QApplication
import os
import os.path as osp
import sys
from ImgLabel import ImgLabel
from config import cfg
from UI import MainUI


class Mark(MainUI):

    def __init__(self):
        super().__init__()

    def srcBtnRespond(self):
        home_dir = osp.expanduser('~')
        dir_name = QFileDialog.getExistingDirectory(self, 'Select Directory', home_dir)
        self.src_show_box.setText(dir_name)
        # self.bg_app.setSrcDir(dir_name)

    def dstBtnRespond(self):
        home_dir = osp.expanduser('~')
        dir_name = QFileDialog.getExistingDirectory(self, 'Select Directory', home_dir)
        self.dst_show_box.setText(dir_name)
        # self.bg_app.setDstDir(dir_name)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    m = Mark()
    sys.exit(app.exec_())
