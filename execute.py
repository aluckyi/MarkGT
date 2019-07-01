#!/home/shu/Applications/Envs/py3/bin/python3
# -*- coding: utf-8 -*-

import os
import os.path as osp
import sys
from config import cfg, cfg_from_file, save_cfg


class Execute(object):

    def __init__(self):
        self.image_names = []
        self.cur_image_name = ''
        self.cur_image_no = 0

    def reset(self):
        self.image_names = []
        self.cur_image_name = ''
        self.cur_image_no = 0

    def getCurrentImageName(self):
        return self.cur_image_name

    def getCurrentImageNo(self):
        return self.cur_image_no

    def getTotalImageNum(self):
        return len(self.image_names)

    def setSrcDir(self, dir):
        cfg.SRC_DIR = dir

    def getSrcDir(self):
        return cfg.SRC_DIR

    def setDstDir(self, dir):
        cfg.DST_DIR = dir

    def getDstDir(self):
        return cfg.DST_DIR

    def saveConfig(self):
        cfg.IMAGE_NAME = self.cur_image_name
        save_cfg()

    def saveData(self, data):
        pass

    def start(self):
        if not osp.exists(cfg.SRC_DIR):
            return -1
        if not osp.exists(cfg.DST_DIR):
            return -2

        image_names = [x for x in os.listdir(cfg.SRC_DIR) if x.endswith('.png')]
        image_names += [x for x in os.listdir(cfg.SRC_DIR) if x.endswith('.jpg')]
        image_names = sorted(image_names)
        if len(image_names) == 0:
            return -3

        self.image_names = image_names
        self.saveConfig()

        self.cur_image_no = 0
        self.cur_image_name = self.image_names[self.cur_image_no]

        return 0

    def restore(self):
        pass


