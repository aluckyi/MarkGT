#!/home/shu/Applications/Envs/py3/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import (QWidget, QDesktopWidget, QLabel, QPushButton, QProgressBar,
                             QRadioButton, QButtonGroup, QFrame, QHBoxLayout, QVBoxLayout)
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtCore import Qt
from ImgLabel import ImgLabel
from config import cfg


class MainUI(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # initialize basic UI widget
        self.initFilePathModule()
        self.initImageModule()
        self.initStatusModule()
        self.initModeModule()
        self.initHorizonModule()
        self.initObstacleModule()
        self.initSequentialOperationModule()

        # set layout
        br_vbox = QVBoxLayout()
        br_vbox.addLayout(self.status_vbox)
        br_vbox.addStretch(2)
        br_vbox.addLayout(self.mode_hbox)
        br_vbox.addStretch(2)
        br_vbox.addLayout(self.horizon_vbox)
        br_vbox.addStretch(2)
        br_vbox.addLayout(self.obs_vbox)
        br_vbox.addStretch(2)
        br_vbox.addLayout(self.sq_vbox)
        br_vbox.addStretch(30)

        b_hbox = QHBoxLayout()
        b_hbox.addStretch(1)
        b_hbox.addWidget(self.img_lbl)
        b_hbox.addStretch(2)
        b_hbox.addLayout(br_vbox)
        b_hbox.addStretch(1)

        m_vbox = QVBoxLayout()
        m_vbox.addStretch(1)
        m_vbox.addLayout(self.fp_vbox)
        m_vbox.addStretch(2)
        m_vbox.addLayout(b_hbox)
        m_vbox.addStretch(1)

        self.setLayout(m_vbox)

        # set basic properties of main UI
        self.setFixedSize(1150, 920)
        self.center()
        self.setWindowTitle('MarkGT')
        self.setWindowIcon(QIcon('./resources/icon.png'))
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def initFilePathModule(self):
        src_lbl = QLabel(self)
        src_lbl.setText('SRC Path:')
        src_lbl.setFixedSize(66, 22)
        self.src_show_box = QLabel(self)
        self.src_show_box.setStyleSheet("QLabel{border:1px solid rgb(180, 180, 180); background-color: white;}")
        self.src_show_box.setFixedSize(1000, 22)
        self.src_btn = QPushButton('...', self)
        self.src_btn.setFixedSize(30, 22)
        self.src_btn.clicked.connect(self.srcBtnRespond)
        src_hbox = QHBoxLayout()
        src_hbox.addStretch(1)
        src_hbox.addWidget(src_lbl)
        src_hbox.addWidget(self.src_show_box)
        src_hbox.addWidget(self.src_btn)
        src_hbox.addStretch(1)

        dst_lbl = QLabel(self)
        dst_lbl.setText('DST Path:')
        dst_lbl.setFixedSize(66, 22)
        self.dst_show_box = QLabel(self)
        self.dst_show_box.setStyleSheet("QLabel{border:1px solid rgb(180, 180, 180); background-color: white;}")
        self.dst_show_box.setFixedSize(1000, 22)
        self.dst_btn = QPushButton('...', self)
        self.dst_btn.setFixedSize(30, 22)
        self.dst_btn.clicked.connect(self.dstBtnRespond)
        dst_hbox = QHBoxLayout()
        dst_hbox.addStretch(1)
        dst_hbox.addWidget(dst_lbl)
        dst_hbox.addWidget(self.dst_show_box)
        dst_hbox.addWidget(self.dst_btn)
        dst_hbox.addStretch(1)

        self.fp_vbox = QVBoxLayout()
        self.fp_vbox.addStretch(1)
        self.fp_vbox.addLayout(src_hbox)
        self.fp_vbox.addLayout(dst_hbox)
        self.fp_vbox.addStretch(1)

    def initImageModule(self):
        self.img_lbl = ImgLabel(self)
        self.img_lbl.setFixedSize(800, 800)
        self.img_lbl.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.img_lbl.setStyleSheet("QLabel{background-color: gray;}")

    def initStatusModule(self):
        cur_img_lbl = QLabel('Image:', self)
        cur_img_lbl.setFixedSize(45, 22)
        self.cur_img_box = QLabel(self)
        self.cur_img_box.setFixedSize(232, 22)
        self.cur_img_box.setStyleSheet("QLabel{border:1px solid rgb(180, 180, 180); background-color: white;}")

        prog_lbl = QLabel('Progress:', self)
        prog_lbl.setFixedSize(65, 22)
        self.no_box = QLabel(self)
        self.no_box.setFixedSize(95, 22)
        self.no_box.setStyleSheet("QLabel{border:1px solid rgb(180, 180, 180); background-color: white;}")
        separate = QLabel('/', self)
        separate.setFixedSize(8, 22)
        self.total_box = QLabel(self)
        self.total_box.setFixedSize(95, 22)
        self.total_box.setStyleSheet("QLabel{border:1px solid rgb(180, 180, 180); background-color: white;}")

        pbar_lbl = QLabel('Finished:', self)
        self.pbar = QProgressBar(self)
        self.pbar.setFixedSize(210, 22)

        x_lbl = QLabel('X :', self)
        x_lbl.setFixedSize(16, 22)
        self.x_box = QLabel(self)
        self.x_box.setFixedSize(60, 22)
        self.x_box.setStyleSheet("QLabel{border:1px solid rgb(180, 180, 180); background-color: white;}")
        separate1 = QLabel(',', self)
        separate1.setFixedSize(16, 22)
        y_lbl = QLabel('Y :', self)
        y_lbl.setFixedSize(16, 22)
        self.y_box = QLabel(self)
        self.y_box.setFixedSize(60, 22)
        self.y_box.setStyleSheet("QLabel{border:1px solid rgb(180, 180, 180); background-color: white;}")

        cur_hbox = QHBoxLayout()
        cur_hbox.addWidget(cur_img_lbl)
        cur_hbox.addWidget(self.cur_img_box)

        prog_hbox = QHBoxLayout()
        prog_hbox.addWidget(prog_lbl)
        prog_hbox.addWidget(self.no_box)
        prog_hbox.addWidget(separate)
        prog_hbox.addWidget(self.total_box)

        bar_hbox = QHBoxLayout()
        bar_hbox.addWidget(pbar_lbl)
        bar_hbox.addWidget(self.pbar)

        xy_hbox = QHBoxLayout()
        xy_hbox.addWidget(x_lbl)
        xy_hbox.addWidget(self.x_box)
        xy_hbox.addWidget(separate1)
        xy_hbox.addWidget(y_lbl)
        xy_hbox.addWidget(self.y_box)
        xy_hbox.addStretch(1)

        self.status_vbox = QVBoxLayout()
        self.status_vbox.addLayout(cur_hbox)
        self.status_vbox.addLayout(prog_hbox)
        self.status_vbox.addLayout(bar_hbox)
        self.status_vbox.addLayout(xy_hbox)

    def initModeModule(self):
        m_lbl = QLabel('Mode:', self)
        self.h_mode = QRadioButton('Horizon', self)
        self.h_mode.clicked.connect(self.modeRespond)
        self.o_mode = QRadioButton('Obstacle', self)
        self.o_mode.clicked.connect(self.modeRespond)

        self.h_mode.setChecked(True)

        m_btn_group = QButtonGroup(self)
        m_btn_group.addButton(self.h_mode)
        m_btn_group.addButton(self.o_mode)
        m_btn_group.setExclusive(True)

        self.mode_hbox = QHBoxLayout()
        self.mode_hbox.addWidget(m_lbl)
        self.mode_hbox.addStretch(1)
        self.mode_hbox.addWidget(self.h_mode)
        self.mode_hbox.addStretch(1)
        self.mode_hbox.addWidget(self.o_mode)
        self.mode_hbox.addStretch(1)

    def initHorizonModule(self):
        h_lbl = QLabel('Horizon:', self)

        self.h_square = QFrame(self)
        self.h_square.setFrameShape(QFrame.Box)
        self.h_square.setFixedSize(22, 22)
        self.h_square.setStyleSheet("QWidget { background-color: rgb(0, 255, 0); }")

        method_lbl = QLabel('Method:', self)
        self.manual_horizon_btn = QRadioButton('Manual', self)
        self.manual_horizon_btn.clicked.connect(self.horizonMethodRespond)
        self.auto_horizon_btn = QRadioButton('Auto', self)
        self.auto_horizon_btn.clicked.connect(self.horizonMethodRespond)

        self.manual_horizon_btn.setChecked(True)

        horizon_method_group = QButtonGroup(self)
        horizon_method_group.addButton(self.manual_horizon_btn)
        horizon_method_group.addButton(self.auto_horizon_btn)
        horizon_method_group.setExclusive(True)

        self.ref_lines_btn = QPushButton('Ref.  Lines', self)
        self.ref_lines_btn.setFixedSize(240, 26)
        self.ref_lines_btn.setCheckable(True)
        self.ref_lines_btn.clicked[bool].connect(self.referLinesBtnRespond)

        ref_num_lbl = QLabel(self)
        ref_num_lbl.setStyleSheet("QLabel{border:1px solid rgb(180, 180, 180); background-color: white}")
        ref_num_lbl.setFixedSize(40, 26)
        ref_num_lbl.setAlignment(Qt.AlignCenter)
        ref_num_lbl.setText(str(cfg.REF_LINE_NUM))

        hs_hbox = QHBoxLayout()
        hs_hbox.addWidget(h_lbl)
        hs_hbox.addStretch(1)
        hs_hbox.addWidget(self.h_square)
        hs_hbox.addStretch(10)

        hm_hbox = QHBoxLayout()
        hm_hbox.addWidget(method_lbl)
        hm_hbox.addStretch(2)
        hm_hbox.addWidget(self.manual_horizon_btn)
        hm_hbox.addStretch(5)
        hm_hbox.addWidget(self.auto_horizon_btn)
        hm_hbox.addStretch(10)

        hr_hbox = QHBoxLayout()
        # hm_hbox.addStretch(1)
        hr_hbox.addWidget(self.ref_lines_btn)
        hm_hbox.addStretch(1)
        hr_hbox.addWidget(ref_num_lbl)
        hm_hbox.addStretch(10)

        self.horizon_vbox = QVBoxLayout()
        self.horizon_vbox.addLayout(hs_hbox)
        self.horizon_vbox.addLayout(hm_hbox)
        self.horizon_vbox.addLayout(hr_hbox)

    def initObstacleModule(self):
        o_lbl = QLabel('Obstacle:', self)

        self.o_square = QFrame(self)
        self.o_square.setFrameShape(QFrame.Box)
        self.o_square.setFixedSize(22, 22)
        self.o_square.setStyleSheet("QWidget { background-color: rgb(180, 180, 180); }")

        self.small_obs_btn = QPushButton('Small Obstacle', self)
        self.small_obs_btn.setCheckable(True)
        self.small_obs_btn.clicked.connect(self.obsClsBtnRespond)

        self.large_obs_btn = QPushButton('Large Obstacle', self)
        self.large_obs_btn.setCheckable(True)
        self.large_obs_btn.clicked.connect(self.obsClsBtnRespond)

        self.small_obs_btn.setChecked(True)
        self.large_obs_btn.setChecked(False)
        # self.img_lbl.setObstacleClass('small')

        cls_btn_group = QButtonGroup(self)
        cls_btn_group.addButton(self.small_obs_btn)
        cls_btn_group.addButton(self.large_obs_btn)
        cls_btn_group.setExclusive(True)

        obs_cls_col = QColor(*cfg.SMALL_OBS_COLOR)
        self.obs_cls_square = QFrame(self)
        self.obs_cls_square.setFixedSize(55, 55)
        self.obs_cls_square.setStyleSheet("QWidget { background-color: %s }" % obs_cls_col.name())

        os_hbox = QHBoxLayout()
        os_hbox.addWidget(o_lbl)
        os_hbox.addStretch(1)
        os_hbox.addWidget(self.o_square)
        os_hbox.addStretch(15)

        cls_vbox = QVBoxLayout()
        cls_vbox.addWidget(self.small_obs_btn)
        cls_vbox.addWidget(self.large_obs_btn)

        obs_hbox = QHBoxLayout()
        obs_hbox.addLayout(cls_vbox)
        obs_hbox.addWidget(self.obs_cls_square)

        self.obs_vbox = QVBoxLayout()
        self.obs_vbox.addLayout(os_hbox)
        self.obs_vbox.addLayout(obs_hbox)

    def initSequentialOperationModule(self):
        sq_lbl = QLabel('Sequential Operation:', self)

        self.sq_btn_start = QPushButton('Start', self)
        self.sq_btn_start.clicked.connect(self.startBtnRespond)
        self.sq_btn_restore = QPushButton('Restore', self)
        self.sq_btn_restore.clicked.connect(self.restoreBtnRespond)

        self.sq_btn_undo = QPushButton('Undo', self)
        self.sq_btn_undo.clicked.connect(self.undoBtnRespond)
        self.sq_btn_next = QPushButton('Next', self)
        self.sq_btn_next.clicked.connect(self.nextBtnRespond)

        sq_hbox1 = QHBoxLayout()
        sq_hbox1.addWidget(self.sq_btn_start)
        sq_hbox1.addWidget(self.sq_btn_restore)

        sq_hbox2 = QHBoxLayout()
        sq_hbox2.addWidget(self.sq_btn_undo)
        sq_hbox2.addWidget(self.sq_btn_next)

        self.sq_vbox = QVBoxLayout()
        self.sq_vbox.addWidget(sq_lbl)
        self.sq_vbox.addLayout(sq_hbox1)
        self.sq_vbox.addLayout(sq_hbox2)