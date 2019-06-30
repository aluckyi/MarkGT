#!/home/shu/Applications/Envs/py3/bin/python3
# -*- coding: utf-8 -*-

import os
import os.path as osp
import numpy as np
from easydict import EasyDict as edict


__C = edict()

cfg = __C

__C.SRC_DIR = ''
__C.DST_DIR = ''
__C.IMAGE_NAME = ''

__C.IMAGE_WIDTH = 800
__C.IMAGE_HEIGHT = 800
__C.SMALL_OBS_COLOR = (255, 0, 0)
__C.LARGE_OBS_COLOR = (0, 0, 255)
__C.LINE_WIDTH = 5


def _merge_a_into_b(a, b):
    """Merge config dictionary a into config dictionary b, clobbering the
    options in b whenever they are also specified in a.
    """
    if type(a) is not edict:
        return

    for k, v in a.items():
        # a must specify keys that are in b
        # if not b.has_key(k):
        if k not in b:
            raise KeyError('{} is not a valid config key'.format(k))

        # the types must match, too
        old_type = type(b[k])
        if old_type is not type(v):
            if isinstance(b[k], np.ndarray):
                v = np.array(v, dtype=b[k].dtype)
            else:
                raise ValueError(('Type mismatch ({} vs. {}) '
                                  'for config key: {}').format(type(b[k]),
                                                            type(v), k))

        # recursively merge dicts
        if type(v) is edict:
            try:
                _merge_a_into_b(a[k], b[k])
            except:
                print('Error under config key: {}'.format(k))
                raise
        else:
            b[k] = v


def cfg_from_file():
    """Load a config file and merge it into the default options."""
    import yaml
    if not osp.exists('./logs/cfg.yml'):
        return False
    with open('./logs/cfg.yml', 'r') as f:
        yaml_cfg = edict(yaml.load(f, Loader=yaml.FullLoader))

    _merge_a_into_b(yaml_cfg, __C)
    return True


def save_cfg():
    import yaml
    if not osp.exists('./logs'):
        os.makedirs('./logs')
    with open('./logs/cfg.yml', 'w') as f:
        yaml.dump(dict(__C), f, default_flow_style=False)


# if __name__ == '__main__':
#     # cfg.SRC_DIR = '/home/shu'
#     # cfg.DST_DIR = '/home/liu'
#     save_cfg()
#     print(cfg_from_file())
#     print(cfg)

# if __name__ == '__main__':
#     import yaml
#     # a = {'sky': [[(1, 2), (3, 4)], [(5, 6), (2, 1)]], 'sea': [[(5, 6), (7, 8)]], 'mid': []}
#     # with open('./data.yml', 'w') as f:
#     #     yaml.dump(a, f)
#     with open('./data.yml', 'r') as f:
#         a = yaml.load(f)
#     print(a)
