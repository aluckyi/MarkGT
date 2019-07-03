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

    def saveData(self, horizon_data, obs_data):
        import yaml

        if len(horizon_data) != cfg.REF_LINE_NUM:
            return -1
        # ============== save data to yml file ================
        data = dict()
        data.update({'width': cfg.IMAGE_WIDTH, 'height': cfg.IMAGE_HEIGHT,
                     'horizon': [], 'obs': {'small': [], 'large': []}})
        data['horizon'] = horizon_data
        for obs_dict in obs_data:
            for obs_cls, obs_rect in obs_dict.items():
                if obs_cls == 'Small Obstacle':
                    data['obs']['small'].append(obs_rect)
                elif obs_cls == 'Large Obstacle':
                    data['obs']['large'].append(obs_rect)

        name = self.cur_image_name.split('.')[0]
        save_path = osp.join(cfg.DST_DIR, name + '.xml')
        with open(save_path, 'w') as f:
            yaml.dump(data, f)
            # data1 = yaml.load(f, Loader=yaml.FullLoader)
        # ============== save data to yml file ================

        self.saveConfig()

        if (self.cur_image_no + 1) >= self.getTotalImageNum():
            return -2

        self.cur_image_no += 1
        self.cur_image_name = self.image_names[self.cur_image_no]

        return 0

    def start(self):
        if not osp.exists(cfg.SRC_DIR):
            return -1
        if not osp.exists(cfg.DST_DIR):
            return -2

        image_names = self.getImageNamesFromDisk(cfg.SRC_DIR)
        if len(image_names) == 0:
            return -3

        self.image_names = image_names
        self.saveConfig()

        self.cur_image_no = 0
        self.cur_image_name = self.image_names[self.cur_image_no]

        return 0

    def restore(self):
        if not cfg_from_file():
            return -1

        if not osp.exists(cfg.SRC_DIR) or not osp.exists(cfg.DST_DIR):
            return -2

        image_names = self.getImageNamesFromDisk(cfg.SRC_DIR)
        if len(image_names) == 0:
            return -3

        self.image_names = image_names
        if cfg.IMAGE_NAME == '':
            self.cur_image_no = 0
            self.cur_image_name = self.image_names[self.cur_image_no]
        else:
            try:
                self.cur_image_no = self.image_names.index(cfg.IMAGE_NAME) + 1
            except ValueError:
                return -4
            if self.cur_image_no >= self.getTotalImageNum():
                return -5
            self.cur_image_name = self.image_names[self.cur_image_no]
        return 0

    @staticmethod
    def getImageNamesFromDisk(path):
        image_names = [x for x in os.listdir(path) if x.endswith('.png')]
        image_names += [x for x in os.listdir(path) if x.endswith('.jpg')]
        image_names = sorted(image_names)
        return image_names



