#!/home/shu/Applications/Envs/py3/bin/python3
# -*- coding: utf-8 -*-

import os
import os.path as osp
import sys


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


